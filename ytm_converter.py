import sys
import os
import os.path
import shutil

import moviepy.editor as mp

PROGRAM_STATUS_SUCCESS = 0


class YouTubeMixConverter:
    def __init__(self, convert_folder_path):
        self.convert_folder_path = convert_folder_path

    def convert(self):
        video_files = os.listdir(self.convert_folder_path)
        for video_filename in video_files:
            full_video_path = os.path.join(self.convert_folder_path, video_filename)
            audio_filename = os.path.basename(video_filename) + ".mp3"
            full_audio_path = os.path.join(self.convert_folder_path, audio_filename)
            clip = mp.VideoFileClip(full_video_path)
            clip.audio.write_audiofile(full_audio_path)


def main():
    convert_folder_path = "Instrumental Mix"

    converter = YouTubeMixConverter(convert_folder_path)
    converter.convert()

    return PROGRAM_STATUS_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
