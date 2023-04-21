#!/usr/bin/python3
import sys
import os
import shutil
import argparse
import re
from http.client import RemoteDisconnected, InvalidURL
from random import random
from time import sleep
from urllib.error import HTTPError
from xmlrpc.client import ProtocolError

import pytube
from pytube.exceptions import VideoUnavailable, AgeRestrictedError, VideoRegionBlocked, LiveStreamError, \
    RecordingUnavailable, MembersOnly, VideoPrivate

PROGRAM_STATUS_SUCCESS = 0


class YouTubeMixDownloader:

    def __init__(self, playlist_url: str, download_path: str, verbosity: int):
        self.download_path = download_path
        self.playlist = pytube.Playlist(playlist_url)
        self.verbosity = verbosity
        # self.playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    def download(self, mode):
        if self.verbosity > 0:
            print(f"Downloading in '{mode}' mode to directory {self.download_path}")
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
            for url in self.playlist.video_urls:
                video = pytube.YouTube(url)
                try:
                    if not video.streams.get_highest_resolution().default_filename in existing_video_files:
                        try:
                            video.streams.get_highest_resolution().download(self.download_path)
                        except (
                        VideoUnavailable, HTTPError, ConnectionError, RemoteDisconnected, InvalidURL, ProtocolError,
                        AgeRestrictedError, VideoRegionBlocked, LiveStreamError, RecordingUnavailable, MembersOnly,
                        VideoPrivate, Exception):
                            try:
                                video.streams.get_highest_resolution().download(self.download_path)
                            except (VideoUnavailable, HTTPError, ConnectionError, RemoteDisconnected, InvalidURL,
                                    ProtocolError, AgeRestrictedError, VideoRegionBlocked, LiveStreamError,
                                    RecordingUnavailable, MembersOnly, VideoPrivate, Exception) as exception:
                                f"Error while downloading {video.streams.get_highest_resolution().default_filename} (Skipping).\n " \
                                f"Exception: {exception}."
                        if self.verbosity > 0:
                            print(f"Downloaded {video.streams.get_highest_resolution().default_filename}.")
                        sleep(random() * 2 + 1)
                    else:
                        print(f"Skipping over {video.streams.get_highest_resolution().default_filename} (already in destination).")
                except KeyError as exception:
                    print(f"Skipping over video 'http://youtube.com/watch?v={video.video_id}'. Exception: {exception}. "
                          f"This may be caused by the video being age-restricted. Try downloading through other tools"
                          f" until corresponding PyTube package error is resolved (bug status:"
                          f" https://github.com/pytube/pytube/issues/1542).")
        else:
            self.download_overwrite()

    def download_overwrite(self):
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)
        os.mkdir(self.download_path)
        # self.playlist.download_all(self.download_path)
        for video in self.playlist.videos:
            video.streams.first().download(self.download_path)
            sleep(random() * 2 + 1)
            if self.verbosity > 0:
                print(f"Downloaded {video.streams.first().default_filename}.")


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
    parser.add_argument("--verbosity", "-v", type=int, default=0,
                        help="Level of output verbosity. Default is 0, meaning no output.")
    args = parser.parse_args()
    playlist_url = args.playlist_url
    download_path = args.output_path
    mode = args.mode

    downloader = YouTubeMixDownloader(playlist_url, download_path, args.verbosity)
    downloader.download(mode)

    return PROGRAM_STATUS_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
