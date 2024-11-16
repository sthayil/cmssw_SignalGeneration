#!/bin/bash
#! /bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc7_amd64_gcc700

pwd

printf "\n\n"
printf "\n$1 : file number"
printf "\n$2 : year (2016/2016APV/2017/2018)"
printf "\n$3 : hadronizer"
printf "\n$4 : numEvents to run over"
printf "\n$5 : outputDir to xrdcp to\n"

#GEN, SIM, DIGI
eval `scramv1 project CMSSW CMSSW_10_6_20_patch1`
cd CMSSW_10_6_20_patch1/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

lhelocfile="splitLHE_$1.txt"
lheline=$(cat "$lhelocfile")
#xrdcp root://cmseos.fnal.gov//"$lheline" .
cp "$lheline" .

printf "\n\nDoing LHE > GEN\n"
date
cmsRun GEN_$2_cfg.py inputFile=file:splitLHE_$1.lhe hadronizer=$3 numEvents=$4
ls -lah 
rm splitLHE_$1.lhe

eval `scramv1 project CMSSW CMSSW_10_6_17_patch1`
cd CMSSW_10_6_17_patch1/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

printf "\n\nDoing GEN > SIM\n"
date
cmsRun SIM_$2_cfg.py
ls -lah 
rm GEN.root

# xrdcp SIM.root $5/gensim_$1.root
# xrdcp $5/gensim_$1.root SIM.root

printf "\n\nDoing SIM > DIGI\n"
date
cmsRun DIGIPremix_$2_cfg.py
ls -lah
rm SIM.root

#HLT
if [[ "$2" == "2018" ]]; then
    cmsswver="CMSSW_10_2_16_UL"
elif [[ "$2" == "2017" ]]; then
    cmsswver="CMSSW_9_4_14_UL_patch1"
elif [[ "$2" == "2016" || "$2" == "2016APV" ]]; then
    cmsswver="CMSSW_8_0_33_UL"
else
    printf "Unknown year! Exiting..."
    exit
fi

eval "scramv1 project CMSSW $cmsswver"
cd $cmsswver/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

printf "\n\nDoing DIGI > HLT\n"
date
cmsRun HLT_$2_cfg.py
ls -lah 
rm DIGIPremix.root

#RECO, MINI
cd CMSSW_10_6_17_patch1/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

printf "\n\nDoing HLT > RECO\n"
date
cmsRun RECO_$2_cfg.py
ls -lah
rm HLT.root

# xrdcp RECO.root $5/reco_$1.root
# xrdcp $5/reco_$1.root RECO.root

printf "\n\nDoing RECO > MINI\n"
date
cmsRun MINIAOD_$2_cfg.py outputFile=miniAOD_$1.root
ls -lah
rm RECO.root

#Cleaning up
xrdcp miniAOD_$1.root $5 #also works on hex
rm miniAOD_$1.root
#rm splitLHE_$1.lhe GEN.root SIM.root DIGIPremix.root HLT.root RECO.root miniAOD_$1.root
