# cmssw_SignalGeneration_Pseudoaxions

Get MINIAOD .root EDM files from MadGraph .lhes

Tested on hexcms, likely needs some tweaks for cmslpc

First, 
'''
voms-proxy-init --valid 192:00 -voms cms
git clone https://github.com/sthayil/cmssw_SignalGeneration_Pseudoaxions.git
cd cmssw_SignalGeneration_Pseudoaxions
'''

Then, 
'''
python lhe_to_miniaod.py [-h] -j JOBNAME -y {2016,2017,2018} -i INPUTLHELOCATION -f NJOBFILES -o OUTPUTDIRECTORY -p {54,90000054} [-n [NEVENTS]]
'''

The arguments are:
--  -h, --help            show this help message and exit
--  -j JOBNAME, --jobName JOBNAME
                          Descriptive jobname, used for filenames and
                          directories
--  -y {2016,2017,2018}, --year {2016,2017,2018}
                          Used to select relevant config files
--  -i INPUTLHELOCATION, --inputLheLocation INPUTLHELOCATION
                          Input LHE filepath (either a specific file or a
                          directory containing multiple .lhe files)
--  -f NJOBFILES, --nJobFiles NJOBFILES
                          Number of files to split the input .lhe into
--  -o OUTPUTDIRECTORY, --outputDirectory OUTPUTDIRECTORY
                          Output base directory filepath for jobs. Should be an
                          EOS area.
--  -p {54,90000054}, --pythiaHadronizer {54,90000054}
                          Hadronizer to be used in GEN step
--  -n [NEVENTS], --nEvents [NEVENTS]
                          Number of events to run over for each split lhe
                          (optional, defaults to -1 (all))