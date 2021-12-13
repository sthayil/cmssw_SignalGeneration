#!/bin/bash
#! /bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc7_amd64_gcc700

pwd

echo "\n"
echo "$1 : file number"
echo "$2 : year (2016/2017/2018)"
echo "$3 : hadronizer"
echo "$4 : numEvents to run over"
echo "$5 : outputDir to xrdcp to"

#GEN, SIM, DIGI
eval `scramv1 project CMSSW CMSSW_10_6_20`
cd CMSSW_10_6_20/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

echo "\nDoing LHE > GEN"
cmsRun GEN_$2_cfg.py inputFile=file:splitLHE_$1.lhe hadronizer=$3 numEvents=$4
ls

echo "\nDoing GEN > SIM"
cmsRun SIM_$2_cfg.py
ls
xrdcp SIM.root $5/gensim_$1.root

echo "\nDoing SIM > DIGI"
cmsRun DIGIPremix_$2_cfg.py
ls

#HLT
eval `scramv1 project CMSSW CMSSW_10_2_16_UL`
cd CMSSW_10_2_16_UL/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
pwd

echo "\nDoing DIGI > HLT"
cmsRun HLT_$2_cfg.py
ls

#RECO, MINI
cd CMSSW_10_6_20/src
eval `scramv1 runtime -sh`
cd ../..
pwd
cd ${_CONDOR_SCRATCH_DIR}
pwd

echo "\nDoing HLT > RECO"
cmsRun RECO_$2_cfg.py
ls

echo "\nDoing RECO > MINI"
cmsRun MINIAOD_$2_cfg.py outputFile=miniAOD_$1.root
ls

#Cleaning up
xrdcp miniAOD_$1.root $5 
rm splitLHE_$1.lhe GEN.root SIM.root DIGIPremix.root HLT.root RECO.root miniAOD_$1.root
