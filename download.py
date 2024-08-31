from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
import os
import re
from pathlib import Path


def get_video_type():
    """Takes user's input and validates it
        Types available:
            1) Mp4
            2) Mp3"""


    menu = "\n1.mp4\n2.mp3"

    # Type input validation
    while True:

        print(menu)
        video_type_input = input("\nEnter the video type (1 or 2): ").lower().strip()


        options_menu = {"1" : "mp4",
                        "2" : "mp3"}

        if not video_type_input in options_menu:
            print("\nPlease enter a valid choice (1 or 2)")
            continue


        return options_menu.get(video_type_input , "mp4") # mp4 as a default value



def get_url_input():
    """Takes user's url input and validates it"""

    # regular expression pattern (2 patterns look at "|")

    url_pattern = r"https://(www\.)?youtube\.com/watch\?v=[A-Za-z0-9-_]{11}|https://youtu\.be/[A-Za-z0-9-_]{11}"

    # url input validation

    while True:

        video_url_input = input("\nPlease enter the video url: ").strip()

        is_valid_url = re.fullmatch(url_pattern , video_url_input)

        if is_valid_url:

            return video_url_input

        print("\nInvalid url ,please enter again")



def on_progress(stream, chunk, bytes_remaining):

    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    total_size_MB = total_size // 1000000
    Megabytes_downloaded = bytes_downloaded // 1000000

    percentage_of_completion = (bytes_downloaded / total_size) * 100
    print(f"Download progress: {percentage_of_completion:.2f}% , MB Downloaded : {Megabytes_downloaded} MB out of {total_size_MB} MB")


def get_download_directory():
    """Get the default download directory path based on the operating system."""

    home_dir = Path.home()
    if os.name == 'nt':  # Windows
        downloads_dir = home_dir / "Downloads"

    else:  # Unix-like (Linux, macOS)
        downloads_dir = home_dir / "Downloads"

    if not downloads_dir.exists():
        downloads_dir.mkdir(parents=True, exist_ok=True)

    return downloads_dir



def download_audio(yt, directory):
    """Download the audio stream to the specified directory."""

    audio_stream = yt.streams.get_audio_only()

    if audio_stream:
        audio_stream.download(directory)
        print("Audio downloaded successfully.")

    else:
        print("Audio stream not available.")



def download_video(yt, directory):
    """Download the video stream to the specified directory."""

    video_stream = yt.streams.get_highest_resolution()

    if video_stream:
        video_stream.download(directory)
        print("Video downloaded successfully.")

    else:
        print("Video stream not available.")



def main():
    """Main function to handle the download process."""

    video_url = get_url_input()
    video_type = get_video_type()
    download_directory = get_download_directory()

    try:

        yt = YouTube(video_url)
        yt.register_on_progress_callback(on_progress)

        if video_type == "mp3":
            download_audio(yt, download_directory)

        else:
            download_video(yt, download_directory)

    except VideoUnavailable:
        print("Video is not available.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

