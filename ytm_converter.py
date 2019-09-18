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
        video_files = [filename for filename in os.listdir(self.convert_folder_path) if filename.endswith(".mp4")]
        errored_on_files = []
        for video_filename in video_files:
            full_video_path = os.path.join(self.convert_folder_path, video_filename)
            audio_filename = os.path.splitext(os.path.basename(video_filename))[0] + ".mp3"
            full_audio_path = os.path.join(self.convert_folder_path, audio_filename)
            # skip already-converted files
            if not os.path.exists(full_audio_path):
                try:
                    clip = mp.VideoFileClip(full_video_path)
                    clip.audio.write_audiofile(full_audio_path)
                    print("Converted file", full_video_path, "to", full_audio_path)
                except OSError:
                    print("Could not convert file", full_video_path)
                    errored_on_files.append(full_video_path)
        print("Converted {:d} of {:d} videos successfully.".format(len(video_files) - len(errored_on_files),
                                                               len(video_files)))
        print("Errored on: ")
        for errored_file in errored_on_files:
            print(errored_file)


def main():
    convert_folder_path = "Instrumental Mix"

    converter = YouTubeMixConverter(convert_folder_path)
    converter.convert()

    return PROGRAM_STATUS_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
