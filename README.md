# tts-polly: using Amazon Polly to generate speech from text (text to speech)

The Amazon Polly service requires an Amazon account with its associated ~/.aws/credentials file.

## How add or delete announcements
- this assumes you've already opened the tts_polly repository with VS Code
- edit one of the following csv files:
  - boomer_wav_files.csv  <- this contains announcements used in games, drills and exceptions
  - demo_announcements.csv <- this contains annoucements used in the demo workout
  - each line has: number,file name,words
    - convention is the numbers are 3 digits.
    - Technically the numbers are not necessary, but help in terms of searches and uniqueness
    - there are a lot of gaps in the boomer_wav_files, since there are fewer than 200 announcements
    - currently the number is used as the first 3 digits of the file name
    - the file name should not have spaces; use underscore
- git commit the edited file(s)
- git push (sync in VS code) to push the committed changes to the remote repository (github)
- in the VScode terminal window type './update_mp3s.py'
  - it is important to run this within the VSCode terminal so that the environment variables are set correctly.
  - this script generates the MP3 files
  - and puts the generated files in the repos/audio repository, commits them, and pushes them to github
- when boomer reboots, it updates it's repositories if it's connected to the internet.
  - So the new MP3 files are downloaded on the next boot.
  - A file watcher (incron) creates WAV files for any new MP3.


## Notes on AMZ Polly settings:
- Stephen was selected as the best sounding voice - casual and clear.
- the speech speed was set to slow to make it easier to understand.  very slow was too slow.
- The output frequency of 22050 was selected in order to make 22050 WAV files.  This frequency was required to make the ALSA software on linux operate correctly.

## Cloning the repository
When cloning this repository in order to generate new mp3 files, a new virtual environment (venv) must be created and initialized as follows.  This is to install the AWS 'boto' python facility.
```
cd tts-polly
python3 -m virtualenv venv
source ./venv/bin/activate
pip install --upgrade pip
pip3 install boto3
```

The example.py file was included in this repository for reference - it is not used.


# OLD - before doing automation to detect differences in csv files after a commit
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