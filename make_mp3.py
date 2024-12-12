"""
This function sends the 'words' text to Polly, gets a MP3 back, 
and creates an MP3 file using filename.
The MP3 file is put in the default output directory: repos/audio
It returns a tuple: (True,None) or (False,string_about_err)
"""

def make_mp3_file(filename, words):

    try:
        from boto3 import Session
    except:
        return (False, "import boto3 failed: did you do?: source ./venv/bin/activate")

    from botocore.exceptions import BotoCoreError, ClientError
    from contextlib import closing

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="default")
    polly = session.client("polly")

    output_dir = "/home/pi/repos/audio/"

    #refer to ssml tags: https://docs.aws.amazon.com/polly/latest/dg/prosody-tag.html

    # The following was for newscaster type voice - not used, slow was preferred:
    # ssml_leading_tags= '<speak><amazon:domain name="news"><prosody rate="slow">'
    # ssml_trailing_tags= '</prosody></amazon:domain></speak>'

    ssml_leading_tags= '<speak><prosody rate="slow">'
    ssml_trailing_tags= '</prosody></speak>'
    selected_voice= "Stephen" #other choices: Matthew, Joanna

    ssml_string= ssml_leading_tags + words + ssml_trailing_tags
    try:
        response = polly.synthesize_speech(Text=ssml_string, OutputFormat="mp3", 
                                            SampleRate="22050", Engine="neural",
                                            VoiceId=selected_voice, TextType="ssml")
    except (BotoCoreError, ClientError) as error:
        return (False, f'{filename} returned error: {error}')

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = f"{output_dir}{filename}.mp3"            
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file
                    print(error)
                    return (False, f'writing {filename}.mp3 returned error: {error}')

    else:
        return (False, f'{filename} did not return with audio data')

    return (True, None)
