import sys
import os
import subprocess

# Usage: python missingfiles.py /eos/uscms/store/user/lpcrutgers/sthayil/pseudoaxions/ttPhiPS_M-250/eosdirtocheck NumOfExpectedFilesEg10

# Use subprocess to get the output and store it in a list
cmd = f"eos root://cmseos.fnal.gov ls {sys.argv[1]}"
filelist_output = subprocess.getoutput(cmd)

filenums = []
lines = filelist_output.splitlines()

for line in lines:
    # if line.startswith('NANOAOD'): # Uncomment to check for NANOAOD
    if line.startswith('miniAOD'):  # Check for miniAOD_*.root, for example
        # Extract digits from the filename
        filenum = int(''.join(filter(str.isdigit, line)))
        filenums.append(filenum)

# If filenums is not empty, get the largest filenum, else set it to 0
largest_filenum = max(filenums) if filenums else 0
expected_files = int(sys.argv[2])

# Use the largest filenum instead of expected_files if it's smaller
if largest_filenum > expected_files:
    print(f"Using largest file number ({largest_filenum}) instead of expected {expected_files}.")
    expected_files = largest_filenum

# Check for missing file numbers
missing_files = [str(i) for i in range(0, expected_files) if i not in filenums]

# Output missing file numbers as a comma-separated list
if missing_files:
    print(",".join(missing_files))
else:
    print("No missing files.")
