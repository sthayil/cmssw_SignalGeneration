# use condor to make miniAODs from signal .lhes
# usage: python lhe_to_miniaod.py -j ttPhiPS_M-500 -y 2018 -i /cms/thayil/pseudoaxions/CMSSW_10_6_19/src/ttPhiPS_M-500 -o /cms/thayil/pseudoaxions/pseudoaxions_files/miniAODs/ -f 100 -p 54

import os, glob, sys, argparse, socket
from datetime import datetime
options = argparse.ArgumentParser(description="Sets up a run to generate miniAODs from signal .lhe files")
options.add_argument("-j", "--jobName",          required=True, help="Descriptive jobname, used for filenames and directories")
options.add_argument("-y", "--year",             required=True, help="Used to select relevant config files", choices=['2016','2017','2018'])
options.add_argument("-i", "--inputLheLocation", required=True, help="Input LHE filepath (either a specific file or a directory containing multiple .lhe files)")
options.add_argument("-f", "--nJobFiles",        required=True, help="Number of files to split the input .lhe into",type=int)
options.add_argument("-o", "--outputDirectory",  required=True, help="Output base directory filepath for jobs. Should be an EOS area.")
options.add_argument("-p", "--pythiaHadronizer", required=True, help="Hadronizer to be used in GEN step", choices=['54','90000054', '54_twoprongdecay'])
options.add_argument("-n", "--nEvents",          nargs='?',     help="Number of events to run over for each split lhe (defaults to -1 (all))", const=-1, type=int, default=-1)
ops = options.parse_args()

inputlhes=[]
if os.path.isdir(ops.inputLheLocation):
    for file in os.listdir(ops.inputLheLocation):
        if file.endswith(".lhe"):
            inputlhes.append(os.path.join(ops.inputLheLocation, file))
    if len(inputlhes)==0: 
        print "ERROR: no .lhe files in supplied input directory"
        exit()
elif os.path.isfile(ops.inputLheLocation): 
    if (ops.inputLheLocation).endswith(".lhe"): inputlhes.append(ops.inputLheLocation)
    else: 
        print "ERROR: supplied input file is not a .lhe"
        exit()
else: 
    print "ERROR: supplied input is neither a .lhe nor a directory"
    exit()

basedir=os.getcwd()
totallhecnt=len(inputlhes)
for inputlhe in inputlhes:
    #make a directory named 'fulljobname' for each lhe file to contain the split lhe, condor logs etc
    fulljobname=ops.jobName
    if totallhecnt>1: fulljobname=ops.jobName+"_"+os.path.splitext(os.path.basename(inputlhe))[0]
    if not os.path.isdir(fulljobname): os.system('mkdir '+fulljobname)

    #make separate output directories for each input lhe
    hostname = socket.gethostname()
    prefix=""
    if "hexcms" in hostname: 
        if os.path.isdir(ops.outputDirectory):
            if not ( (ops.outputDirectory).startswith("/") ): prefix=os.getcwd()+"/"
        else:
            print "provided output directory does not exist, trying to create..."
            if not ( (ops.outputDirectory).startswith("/") ): prefix=os.getcwd()+"/"
            os.system('mkdir -p '+ops.outputDirectory)
            print "created directory: "+prefix+ops.outputDirectory
        #make dir for this specific job
        if os.path.isdir(ops.outputDirectory+'/'+fulljobname): print "WARNING: directory named "+ops.outputDirectory+'/'+fulljobname+" already exists, files will be overwritten"
        else: os.system('mkdir -p '+ops.outputDirectory+'/'+fulljobname)

    elif ".fnal.gov" in hostname: 
        if (ops.outputDirectory).startswith("/store/user/"): 
            os.system('eos root://cmseos.fnal.gov mkdir -p '+ops.outputDirectory+'/'+fulljobname)
        # elif (ops.outputDirectory).startswith("/eos/uscms/store/user/") : #this wont work with the prefix bit; fix---------------
        #     os.system('eos root://cmseos.fnal.gov mkdir -p '+ops.outputDirectory+'/'+fulljobname)
        else:
            #print "ERROR: for output directory, specify an EOS path starting in /store/user/ or /eos/uscms/store/user/"
            print "ERROR: for output directory, specify an EOS path starting in /store/user/"
            exit()
        prefix="root://cmseos.fnal.gov//" 
    outputDir=prefix+ops.outputDirectory+'/'+fulljobname

    #split lhe
    if not os.path.isdir(fulljobname+'/split_lhe'): os.system('mkdir '+fulljobname+'/split_lhe')
    os.system('cp splitLHE.py '+fulljobname)
    if len(os.listdir(fulljobname+'/split_lhe')) == ops.nJobFiles:
        print "Split files already present, using them"
    else:
        if len(os.listdir(fulljobname+'/split_lhe')) !=0: os.system('rm '+fulljobname+'/split_lhe/*')
        print "Splitting lhe..."
        os.system('python '+fulljobname+'/splitLHE.py '+inputlhe+' '+fulljobname+'/split_lhe/splitLHE_ '+str(ops.nJobFiles))
        if len(os.listdir(fulljobname+'/split_lhe')) == ops.nJobFiles: print "Splitting done"

    #set up other directories
    os.chdir(fulljobname)
    if not os.path.isdir('logs_from_condor'): os.system('mkdir logs_from_condor')
    if not os.path.isdir('jdl_files'): os.system('mkdir jdl_files')

    #modify jdl
    mytime=datetime.now()
    mytimestr=mytime.strftime("%y%m%d%H")
    with open('../condorsubmit_lhetominiaod.jdl', 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('00000000', fulljobname)
    filedata = filedata.replace('11111111', mytimestr)
    filedata = filedata.replace('22222222', ops.year)
    filedata = filedata.replace('33333333', ops.pythiaHadronizer)
    filedata = filedata.replace('44444444', str(ops.nEvents))
    filedata = filedata.replace('55555555', outputDir)
    filedata = filedata.replace('66666666', str(ops.nJobFiles))
    with open('condorsubmit_lhetominiaod_'+mytimestr+'.jdl', 'w') as file:
        file.write(filedata)
        
    #submit jobs
    os.system('cp ../condorsubmit_lhetominiaod.sh .')
    os.system('cp ../Premix_RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2.list .')
    os.system('cp ../GEN_'+ops.year+'_cfg.py .')
    os.system('cp ../SIM_'+ops.year+'_cfg.py .')
    os.system('cp ../DIGIPremix_'+ops.year+'_cfg.py .')
    os.system('cp ../HLT_'+ops.year+'_cfg.py .')
    os.system('cp ../RECO_'+ops.year+'_cfg.py .')
    os.system('cp ../MINIAOD_'+ops.year+'_cfg.py .')
    print "Submitting jobs with condor_submit condorsubmit_lhetominiaod_"+mytimestr+".jdl ..."
    os.system('condor_submit condorsubmit_lhetominiaod_'+mytimestr+'.jdl')
    os.system('mv condorsubmit_lhetominiaod_'+mytimestr+'.jdl jdl_files/')

    os.chdir(basedir)
    
