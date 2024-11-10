# rename files at path. With specific name.

import os
import re


def rename_files(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        match = re.match(r"shot_v(\d+)\.png", filename)
        if match:
            number = int(match.group(1))
            new_filename = f"shot_v{number:04d}.png"

            if filename != new_filename:
                old_path = os.path.join(directory, filename)
                new_path = os.path.join(directory, new_filename)
                print(f"Renaming '{filename}' to '{new_filename}'")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    directory_path = input("Enter the directory path containing the files: ")
    rename_files(directory_path)
