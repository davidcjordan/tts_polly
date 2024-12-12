#!/usr/bin/env python3
"""
This program parses the git diff to get rows changed in a CSV with columns: number,filename,text

It only uses filename and text fields.

It then calls make_mp3.py for each added or changed text entry.

Updating the WAV files on a Boomer is done by an incron (file watcher) job on the boomer than generates
a new WAV file for each new MP3.  (TBD: And deletes WAV files for deleted MP3s)

"""

import subprocess
from make_mp3 import make_mp3_file

if __name__ == "__main__":

    git_history_depth= -4
    # get list of changes from the last commit
    git_command = f'git log -p {git_history_depth} | grep -E "^\+|^\-" | grep -v "\-\-\-"'
    process = subprocess.Popen(git_command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        git_log = stdout.decode().splitlines()
    else:
        print(f'Error: {stderr.decode()}')

    updated_filename= ''
    process_csv_lines= False
    # print(f'{git_log}')
    for line in git_log:
        if line.startswith("+++"):
            updated_filename = line.split('/')[1]
            if updated_filename.endswith('.csv'):
                process_csv_lines= True
            else:
                process_csv_lines= False
                print(f'Skipping file: {updated_filename}')
        else:
            if process_csv_lines:
                fields = line.split(',')
                # print(f"{fields[1]} {fields[2]}")
                if line.startswith("-"):
                    print(f"will delete file '{fields[1]}' that was in '{updated_filename}'")
                elif line.startswith("+"):
                    #remove file extension (WAV)
                    base_filename= fields[1][:-4]
                    return_tuple= make_mp3_file(base_filename, fields[2])
                    if return_tuple[0]:
                        print(f"added file '{base_filename}.mp3' with tts for '{fields[2]}' from '{updated_filename}'")
                    else:
                        print(f"{return_tuple[1]}")

                else:
                    print(f"unexpected line '{line}' in '{updated_filename}'")
