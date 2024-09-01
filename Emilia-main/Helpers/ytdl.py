import pytube
from pytube import YouTube
import os

def delete_mp4_files():
  # Get list of all files in the current directory
  files = os.listdir(".")

  # Loop through all files
  for file in files:
      # Check if the file ends with '.mp4'
      if file.endswith('.mp4'):
          # Construct the full file path
          file_path = os.path.join(".", file)

          # Delete the file
          os.remove(file_path)
          print(f"Deleted {file_path}")

def video_dl(url, output_path='.'):
    """
    Downloads a YouTube video from the given URL.
    
    Parameters:
    - url (str): The URL of the YouTube video to download.
    - output_path (str): The directory where the video will be saved.
    """
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)
        print(f"Video downloaded successfully: {video_stream.title}")
        new_file = video_stream.title + '.mp4'
        return new_file,video_stream.title
    except Exception as e:
        print(f"An error occurred: {e}")

def music_dl(url, output_path='.'):
    """
    Downloads the audio of a YouTube video from the given URL.
    
    Parameters:
    - url (str): The URL of the YouTube video to extract audio from.
    - output_path (str): The directory where the audio file will be saved.
    """
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        out_file = audio_stream.download(output_path)
        
        # Convert the downloaded file to .mp3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        print(f"Audio downloaded and converted successfully: {new_file}")
        return new_file,out_file.title
    except Exception as e:
        print(f"An error occurred: {e}")



#download_youtube_music('https://youtu.be/JaFOV7wwmKs?si=j0abhenHnzGR4O6R', 'downloads')







