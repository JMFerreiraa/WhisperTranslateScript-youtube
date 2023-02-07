import whisper
import hashlib
from pytube import YouTube
from datetime import timedelta
import os
import torch


def download_video(url):
    print("Start downloading", url)
    yt = YouTube(url)

    hash_file = hashlib.md5()
    hash_file.update(yt.title.encode())

    file_name = f'{hash_file.hexdigest()}.mp4'

    yt.streams.first().download("", file_name)
    print("Downloaded to", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }

def deletevideo(path):
    os.remove(path)

def transcribe_audio(path):

    # Initialize the device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisper.load_model("large", device=device) # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(path, task='translate', verbose=True)
    segments = transcribe['segments']
    srtFilename = "generated_subtitles.srt"
    with open(srtFilename, 'w', encoding='utf-8') as srtFile:
            srtFile.write("")

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    return srtFilename


if __name__ == '__main__':

    print("Welcome to Video/Audio translator by João Sá - Uses Whisper by OpenAI")
    print("What do you want to translate?")
    print("1 - Youtube Video")
    print("2 - Local file")
    option = int(input())
    if(option == 1):
        print("What is the Link for the video?")
        link = input()
        video = download_video(link)
        result = transcribe_audio(video['file_name'])
    elif(option == 2):
        print("Whats is the path for the file?")
        path = input()
        result = transcribe_audio(path)

    print("The subtitles file was created on: ", result)