import os
import sys
from datetime import datetime
import subprocess
import re

def main(base_dir, job_numbers):
    # Ensure the base directory exists
    if not os.path.isdir(base_dir):
        print(f"Directory {base_dir} does not exist.")
        sys.exit(1)

    split_lhe_dir = os.path.join(base_dir, "split_lhe")
    jdl_dir = os.path.join(base_dir, "jdl_files")

    # Get the current timestamp in YYMMDDHH format
    current_time = datetime.now().strftime("%y%m%d%H")

    # Iterate over each job number
    for job_number in job_numbers:
        job_file = f"splitLHE_{job_number}.lhe"
        job_file_path = os.path.join(split_lhe_dir, job_file)

        if not os.path.exists(job_file_path):
            print(f"File {job_file_path} does not exist.")
            sys.exit(1)

    # If all .lhe files exist, proceed with JDL file processing
    newest_jdl_file = None
    newest_timestamp = "00000000"

    # Find the newest JDL file based on the timestamp
    for jdl_file in os.listdir(jdl_dir):
        if jdl_file.endswith(".jdl"):
            try:
                # Extract timestamp from filename
                old_timestamp = jdl_file.split('_')[-1].replace('.jdl', '')
                if old_timestamp.isdigit() and len(old_timestamp) == 8:
                    if old_timestamp > newest_timestamp:
                        newest_timestamp = old_timestamp
                        newest_jdl_file = jdl_file
            except Exception as e:
                print(f"Error processing {jdl_file}: {e}")

    if newest_jdl_file:
        old_jdl_path = os.path.join(jdl_dir, newest_jdl_file)
        new_jdl_file = f"condorsubmit_lhetominiaod_{current_time}.jdl"
        new_jdl_path = os.path.join(jdl_dir, new_jdl_file)

        # Copy and update the JDL file
        try:
            with open(old_jdl_path, 'r') as file:
                content = file.read()

            # Replace old timestamp with new timestamp
            updated_content = content.replace(newest_timestamp, current_time)

            # Replace queue <some value> with queue 1
            updated_content = re.sub(r'queue \d+', 'queue 1', updated_content)

            # Write the updated content to a new file
            with open(new_jdl_path, 'w') as file:
                file.write(updated_content)

            print(f"Created new JDL file: {new_jdl_path}")

            # Submit the job for each job number
            for job_number in job_numbers:
                # Replace $(Process) with the job number
                jdl_content_with_job = updated_content.replace('$(Process)', str(job_number))

                # Write the modified content to a temporary JDL file
                temp_jdl_path = os.path.join(jdl_dir, f"temp_{job_number}_{new_jdl_file}")
                with open(temp_jdl_path, 'w') as temp_file:
                    temp_file.write(jdl_content_with_job)

                # Submit the job
                try:
                    os.system('condor_submit '+temp_jdl_path)
                except Exception as e:
                    print(f"Error submitting job for {job_number}: {e}")

                # Optionally, remove the temporary JDL file after submission
                os.remove(temp_jdl_path)


            # # Submit the job for each job number
            # for job_number in job_numbers:
            #     # Replace $(Process) with the job number
            #     jdl_content_with_job = updated_content.replace('$(Process)', str(job_number))

            #     # Write the modified content to a temporary JDL file
            #     temp_jdl_path = os.path.join(jdl_dir, f"temp_{job_number}_{new_jdl_file}")
            #     with open(temp_jdl_path, 'w') as temp_file:
            #         temp_file.write(jdl_content_with_job)

            #     # Submit the job
            #     try:
            #         subprocess.run([condor_submit_path, temp_jdl_path], check=True)
            #         print(f"Submitted job for {job_number} with JDL file {temp_jdl_path}")
            #     except subprocess.CalledProcessError as e:
            #         print(f"Error submitting job for {job_number}: {e}")

            #     # Optionally, remove the temporary JDL file after submission
            #     os.remove(temp_jdl_path)

            # # Submit the job for each job number
            # for job_number in job_numbers:
            #     # Replace $(Process) with the job number
            #     jdl_content_with_job = updated_content.replace('$(Process)', str(job_number))

            #     # Write the modified content to a temporary JDL file
            #     temp_jdl_path = os.path.join(jdl_dir, f"temp_{job_number}_{new_jdl_file}")
            #     with open(temp_jdl_path, 'w') as temp_file:
            #         temp_file.write(jdl_content_with_job)

            #     # Submit the job
            #     try:
            #         subprocess.run(["condor_submit", temp_jdl_path], check=True)
            #         print(f"Submitted job for {job_number} with JDL file {temp_jdl_path}")
            #     except subprocess.CalledProcessError as e:
            #         print(f"Error submitting job for {job_number}: {e}")

            #     # Optionally, remove the temporary JDL file after submission
            #     os.remove(temp_jdl_path)
            
        except Exception as e:
            print(f"Error updating {old_jdl_path}: {e}")

    else:
        print("No valid JDL files found.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python resubmit_failed_jobs.py <base directory> <job numbers (comma separated)>")
        sys.exit(1)

    base_directory = sys.argv[1]
    job_numbers_str = sys.argv[2]
    job_numbers_list = job_numbers_str.split(',')

    main(base_directory, job_numbers_list)
