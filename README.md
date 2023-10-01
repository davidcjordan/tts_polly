# tts-polly: using Amazon Polly to generate speech from text (text to speech)

The Amazon Polly service requires an Amazon account with its associated ~/.aws/credentials file.

Run ```make_mp3.py``` to read a csv file and generate an mp3 file for each row:
- The csv file has the following columns:
  - number: the speech file number - used as the first 3 digits in the filename
  - file name: the generated mp3 files will have this name.
  - words: the set of words is sent to the Amazon Polly service and the resulting mp3 is download
  - optional columns:
    - utils: a 'u' indicates its a utility speech, 'n' indicates its a number which are used in score annoucements.
    - game,drill: a 'g' indicates used in game mode, a 'd' indicated used in drill mode
    - used: this column indicated whether the announcement was played in the current software. Ironically the used column is no longer used and can be deleted.
- NOTE: before running make_mp3.py, then type ```source ./venv/bin/activate``` to activate the python virtual environment.
- The generated mp3 files will be put into the ~/repos/audio directory, which is also a github repository.

Currently make_mp3.py is hardcoded to read boomer_wav_files.csv; it can be editted to read a different CSV file instead.

After generating the MP3s:
  - the new files in the repos/audio repository should be committed to github
  - The repos/audio directory on each base should be updated using ```git pull origin```
  - after updating the mp3 files in the audio directory on the base then generate WAV files using the following commands
```
cd repos/audio
for f in *.mp3; do mpg123 -vm2 -w "/home/pi/boomer/audio/${f%.mp3}.WAV" "$f"; done
```
## Notes on AMZ Polly settings:
- Stephen was selected as the best sounding voice - casual and clear.
- the speech speed was set to slow to make it easier to understand.  very slow was too slow.
- The output frequency of 22050 was selected in order to make 22050 WAV files.  This frequency was required to make the ALSA software on linux operate correctly.

## cloning the repository
When cloning this repository in order to generate new mp3 files, a new virtual environment (venv) must be created and initialized as follows.  This is to install the AWS 'boto' python facility.
```
cd tts-polly
python3 -m virtualenv venv
source ./venv/bin/activate
pip install --upgrade pip
pip3 install boto3
```

The example.py file was included in this repository for reference - it is not used.
