from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from os import path


def get_best_stream(yt, is_audio=True):
    if is_audio:
        return yt.streams.get_audio_only(None)
    else:
        return yt.streams.filter(progressive=True, file_extension='mp4') \
                         .order_by('resolution') \
                         .desc() \
                         .first()


def download_file(stream):
    filename = path.basename(stream.get_file_path())
    print("Downloading file.....")
    stream.download(filename=filename)
    print("Download complete")
    return filename


if __name__ == "__main__":
    url = input("Please enter the YouTube video URL: ")
    is_audio_str = input("Download audio only? (Y/N): ")
    is_audio = is_audio_str.lower() == "y"

    try:
        print("Getting video information.......")
        yt = YouTube(url)
        stream = get_best_stream(yt, is_audio)
        if stream:
            download_file(stream)
    except RegexMatchError:
        print("Invalid URL!")
    except VideoUnavailable:
        print("Video unavailable. This might require logging in to view.")
