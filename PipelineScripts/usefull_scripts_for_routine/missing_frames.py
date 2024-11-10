# created it for listing missing frames for images sequence. It returns range of missing files.

import os


def find_missing_frames(directory):
    frames = []
    list_files(directory, frames)

    frames.sort()
    missing_ranges = []
    if frames:
        start = frames[0]
        end = frames[-1]

        all_frames = set(range(start, end + 1))
        existing_frames = set(frames)
        missing_frames = sorted(all_frames - existing_frames)

        if missing_frames:
            define_range(missing_frames, missing_ranges)

    if missing_ranges:
        print("Missing frames:", ", ".join(missing_ranges))
    else:
        print("No missing frames.")


def list_files(directory, frames):
    for filename in os.listdir(directory):
        if filename.endswith(".png") and filename[:-4].isdigit():
            frames.append(int(filename[:-4]))


def define_range(missing_frames, missing_ranges):
    range_start = missing_frames[0]
    for i in range(1, len(missing_frames)):
        if missing_frames[i] != missing_frames[i - 1] + 1:
            missing_ranges.append(f"{range_start}-{missing_frames[i - 1]}")
            range_start = missing_frames[i]
    missing_ranges.append(f"{range_start}-{missing_frames[-1]}")


if __name__ == "__main__":
    directory_path = input("Enter the directory path containing the frames: ")
    find_missing_frames(directory_path)
