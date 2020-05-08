#!/usr/bin/python3
import sys
import os
import shutil
import argparse

import pytube

PROGRAM_STATUS_SUCCESS = 0


class YouTubeMixDownloader:

    def __init__(self, playlist_url, download_path):
        self.download_path = download_path
        self.playlist = pytube.Playlist(playlist_url)

    def download(self, mode):
        if mode == "overwrite":
            self.download_overwrite()
        elif mode == "resume":
            self.download_resume()
        else:
            raise ValueError("Unrecognized mode: {:s}".format(mode))

    def download_resume(self):
        if os.path.exists(self.download_path):
            existing_video_files = []
            for filename in os.listdir(self.download_path):
                existing_video_files.append(filename)
            self.playlist.populate_video_urls()
            for url in self.playlist.video_urls:
                video = pytube.YouTube(url)
                if not video.streams.first().default_filename in existing_video_files:
                    video.streams.first().download(self.download_path)

        else:
            self.download_overwrite()

    def download_overwrite(self):
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)
        os.mkdir(self.download_path)
        self.playlist.download_all(self.download_path)


def main():
    parser = argparse.ArgumentParser("A simple script that downloads an entire YouTube playlist as a set of mp4 video "
                                     "files.")
    parser.add_argument("--playlist_url", "-p", type=str, help="URL of playlist to download from",
                        default="https://www.youtube.com/playlist?list=PLoDNvK0-oocmKUJPaHxn-QuqYP3OWlVLU")
    parser.add_argument("--output_path", "-o", type=str, help="Path on disk where the downloaded files will be placed",
                        default="Instrumental Mix")
    parser.add_argument("--mode", "-m", type=str,
                        help="Defines program behavior. The 'resume' mode will not overwrite or try to download files "
                             "that are already there, 'overwrite' will overwrite them.",
                        default='resume')
    args = parser.parse_args()
    playlist_url = args.playlist_url
    download_path = args.output_path
    mode = args.mode

    downloader = YouTubeMixDownloader(playlist_url, download_path)
    downloader.download(mode)

    return PROGRAM_STATUS_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
