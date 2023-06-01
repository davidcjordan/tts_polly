# tts-polly: using Amazon Polly to generate speech from text (text to speech)

## Overview
Run ```make_mp3.py``` to read a csv file and generate an mp3 file for each row.

Currently make_mp3.py is coded to read boomer_wav_files.csv

make_mp3.py can be editted to read a different CSV file instead.

After generating the MP3s:
  - the new files in the repos/audio repository should be committed to github
  - The repos/audio directory on each base should be updated using ```git pull origin```
  - WAV files should be generated using:
```
cd repos/audio
for f in *.mp3; do mpg123 -q -vm2 -w "~/boomer/audio/${f%.mp3}.WAV" "$f"; done
```

The example.py file was included in this repository for reference - it is not used.

## cloning the repository
When cloning this repository, a new virtual environment (venv) must be created and initialized:
```
cd tts-polly
python3 -m virtualenv venv
source ./venv/bin/activate
pip install --upgrade pip
pip3 install boto3
```