#!/usr/bin/python3
import argparse
import sys

import pytubefix as pytube
from pytubefix.exceptions import VideoUnavailable, AgeRestrictedError, VideoRegionBlocked, LiveStreamError, \
    RecordingUnavailable, MembersOnly, VideoPrivate

PROGRAM_STATUS_SUCCESS = 0
PROGRAM_STATUS_FAILURE = 1


def download_single_video(video_url: str, mp4: bool, output_dir: str) -> bool:
    video = pytube.YouTube(video_url)
    stream = (video.streams
              .filter(file_extension="mp4", progressive=True)
              .order_by("resolution")
              .desc()
              .first()) if mp4 else (video.streams
              .order_by("resolution")
              .desc()
              .first())
    if stream is None:
        print("No progressive mp4 stream found for this video.")
        return False
    print(mp4)
    print("Downloading from selected stream: ", stream)
    stream.download(output_path=output_dir)
    print(f"Downloaded {stream.default_filename}.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        "Download a single YouTube video at the highest available MP4 resolution to the current directory."
    )
    parser.add_argument("url", type=str, help="YouTube video URL to download")
    parser.add_argument("--mp4", action='store_true', help="Download MP4 container only (when available)", default=False)
    parser.add_argument("--output-dir", "-o", type=str, default=".",
                        help="Directory to save the downloaded file (default: current directory)")
    args = parser.parse_args()

    try:
        success = download_single_video(args.url, args.mp4, args.output_dir)
    except (VideoUnavailable, AgeRestrictedError, VideoRegionBlocked, LiveStreamError,
            RecordingUnavailable, MembersOnly, VideoPrivate, Exception) as exception:
        print(f"Error while downloading video. Exception: {exception}.")
        return PROGRAM_STATUS_FAILURE

    return PROGRAM_STATUS_SUCCESS if success else PROGRAM_STATUS_FAILURE


if __name__ == "__main__":
    sys.exit(main())
