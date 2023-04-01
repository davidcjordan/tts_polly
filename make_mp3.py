"""Getting Started Example for Python 2.7+/3.3+"""
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

def make_mp3_file(filename, words):
    try:
        response = polly.synthesize_speech(Text=words, OutputFormat="mp3", 
                                            SampleRate="22050", Engine="neural",
                                            VoiceId="Stephen")
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
                output = f"/home/pi/audiofiles/mp3/{filename[:-4]}.mp3"            

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
    with open('boomer_wav_files.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row['file name'], row['words'])
            make_mp3_file(filename=row['file name'], words=row['words'])
