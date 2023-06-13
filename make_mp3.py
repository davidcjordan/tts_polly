#!/usr/bin/env python3
"""
This program reads a csv file that has columns: number,file name,words

For each row, it sends the 'words' text to Polly, gets a MP3 back, and names the MP3 file as per the file name column.

"""
try:
    from boto3 import Session
except:
   print("import boto3 failed: did you do?: source ./venv/bin/activate")
   exit(1)

from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import sys
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

phrases_file = "boomer_wav_files.csv"
output_dir = "/home/pi/repos/audio/"
# phrases_file = "demo_announcements.csv"
phrases_file = "restore_announcements.csv"
# output_dir = "/home/pi/audiofiles/test/"

# The following was for newscaster type voice - not used, slow was preferred:
# ssml_leading_tags= '<speak><amazon:domain name="news"><prosody rate="slow">'
# ssml_trailing_tags= '</prosody></amazon:domain></speak>'

ssml_leading_tags= '<speak><prosody rate="slow">'
ssml_trailing_tags= '</prosody></speak>'
selected_voice= "Stephen" #other choices: Matthew, Joanna

def make_mp3_file(filename, words):
    try:
        response = polly.synthesize_speech(Text=words, OutputFormat="mp3", 
                                            SampleRate="22050", Engine="neural",
                                            VoiceId=selected_voice, TextType="ssml")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = f"{output_dir}{filename[:-4]}.mp3"            

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

if __name__ == "__main__":
    import csv
    with open(phrases_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['file name'], row['words'])
            ssml= f'{ssml_leading_tags}{row["words"]}{ssml_trailing_tags}'
            make_mp3_file(filename=row['file name'], words=ssml)
