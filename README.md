# cmssw_SignalGeneration_Pseudoaxions

Get MINIAOD .root EDM files from MadGraph .lhes

Tested on hexcms and cmslpc. (Breaks on hexcms for reasons unclear, following up with Pieter Jacques.)

Currently only has config files to generate samples with 2018 conditions. 

First, 
```
voms-proxy-init --valid 192:00 -voms cms
git clone https://github.com/sthayil/cmssw_SignalGeneration_Pseudoaxions.git
cd cmssw_SignalGeneration_Pseudoaxions
```

Then, 
```
python lhe_to_miniaod.py [-h] -j JOBNAME -y {2016,2017,2018} -i INPUTLHELOCATION -f NJOBFILES -o OUTPUTDIRECTORY -p {54,90000054,54_twoprongdecay} [-n [NEVENTS]]
```

The arguments are:
-  -h (--help):                                   Show this help message and exit
-  -j JOBNAME (--jobName JOBNAME):                Descriptive jobname, used for filenames and directories
-  -y {2016,2017,2018} (--year {2016,2017,2018}): Used to select relevant config files
-  -i INPUTLHELOCATION (--inputLheLocation INPUTLHELOCATION): Input LHE filepath (either a specific file or a directory containing multiple .lhe files)
-  -f NJOBFILES (--nJobFiles NJOBFILES): Number of files to split the input .lhe into
-  -o OUTPUTDIRECTORY (--outputDirectory OUTPUTDIRECTORY): Output base directory filepath for jobs. Should be an EOS area.
-  -p {54,90000054} (--pythiaHadronizer {54,90000054}): Hadronizer to be used in GEN step (54 is Steffie's signal, 90000054 is Brandon's)
-  -n [NEVENTS] (--nEvents NEVENTS): Number of events to run over for each split lhe (optional, defaults to -1 (all))

For example, doing
```
python lhe_to_miniaod.py -j ttPhiPS_M-500 -y 2018 -i /cms/thayil/pseudoaxions/CMSSW_10_6_19/src/ttPhiPS_M-500 -o /cms/thayil/pseudoaxions/pseudoaxions_files/miniAODs/ -f 100 -p 54
```
will read the .lhe file(s) in /cms/thayil/pseudoaxions/CMSSW_10_6_19/src/ttPhiPS_M-500, process them as 2018 MC, and output 100 miniAODs to /cms/thayil/pseudoaxions/pseudoaxions_files/miniAODs/ttPhiPS_M-500/

Some utilities:

```python check_condor_logs.py <base directory>```
See if jobs failed or finished with non-0 exit codes

```python missingfiles_updated.py <eos dir> <#files expected>, eg: /eos/uscms/store/user/lpcrutgers/sthayil/pseudoaxions/mini/2018_ttPhiPS_M-3000/ 100```
See if any output files are missing (searches for up to provided number, or max filenumber found in the directory if that is higher).

```python resubmit_failed_jobs.py <base directory> <job numbers (comma separated)>```
Use to resubmit jobs that failed or are otherwise missing.