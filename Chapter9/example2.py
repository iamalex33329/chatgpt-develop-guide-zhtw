from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from os import path

import openai
import apikey


openai.api_key = apikey.OPENAI_API_KEY


def find_best_stream(url, is_audio=True):
    try:
        print("Fetching video information.......")
        yt = YouTube(url)
        if is_audio:
            return yt.streams.get_audio_only(None)
        else:
            return yt.streams.filter(progressive=True, file_extension='mp4') \
                .order_by('resolution') \
                .desc() \
                .first()
    except RegexMatchError:
        print("Invalid URL!")
        return None
    except VideoUnavailable:
        print("Video unavailable. This might require logging in to view.")
        return None


def download_file(stream):
    filename = path.basename(stream.get_file_path())

    print("Downloading file.....")
    stream.download(filename=filename)
    print("Download complete")
    return filename


def transcribe_audio_to_subtitles(audio_filename):
    print("Transcribing audio to subtitles....")
    with open(audio_filename, "rb") as f:
        caption = openai.Audio.transcribe('whisper-1',
                                          f,
                                          response_format='srt',
                                          prompt='')
    print("Transcription complete")
    print("Saving subtitles to file")
    srt_filename = path.splitext(audio_filename)[0] + ".srt"
    with open(srt_filename, "w") as f:
        f.write(caption)
    print("File saved")
    return caption


if __name__ == "__main__":
    source_type = input("Please enter the source of the audio (1 or 2)\n1. YouTube URL\n2. Local file\n：")
    if source_type == "1":
        url = input("Please enter the YouTube video URL: ")
        stream = find_best_stream(url, is_audio=True)
        if stream:
            audio_filename = download_file(stream)
    elif source_type == "2":
        audio_filename = input("Please enter the uploaded file name (including extension): ")
    else:
        print("Incorrect input. Please try again.")

    if audio_filename:
        print(f'{audio_filename}')
        transcribe_audio_to_subtitles(audio_filename)
