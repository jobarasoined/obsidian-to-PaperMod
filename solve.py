#!/usr/bin/env python3

import re
import os
import argparse
import logging
import time
import datetime
from functools import wraps

PATTERN_TO_DETECT = r'!\[\[(.*?)\]\]'
MARKDOWN_EXTENSION = '.md'
IMAGE_EXTENSIONS = ('.png', '.jpeg', '.jpg')

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def calc_time(func):
    """Decorator to calculate and print the time taken by a function to execute."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Job Done for {func.__name__} in: {elapsed_time:.4f} seconds")
        return result
    return wrapper


def process_directories(directories, function):
    """Process each directory using the specified function."""
    for directory in directories:
        logging.info(f"Processing directory: {directory}")
        function(directory)


def has_extension(filename, extensions):
    return filename.lower().endswith(extensions)


def list_files_recursively(path):
    """Returns a list of all files in the given directory and its sub-directories."""
    file_list = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            file_list.append(os.path.join(dirpath, filename))
    return file_list


def format_image_reference(match):
    """Replaces matched image reference with formatted text."""
    original_text = match.group(1)
    modified_text = original_text.replace(' ', '_')
    return f'![[{modified_text}]](/screenshots/{modified_text})'


@calc_time
def replace_content_in_markdown(directory):
    """Replaces image references in markdown files."""
    for filename in list_files_recursively(directory):
        if has_extension(filename, MARKDOWN_EXTENSION):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace the contents based on regex pattern
            new_content = re.sub(PATTERN_TO_DETECT, format_image_reference, content)
            if content != new_content:
                if not re.search(r'!\[\[.*?\]\]\(/screenshots/.*?\)', content):
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(new_content)
                    logging.info(f'Updated: {filename}')
                else:
                    logging.info(f'No changes for: {filename}')


@calc_time
def add_front_matter_to_markdown(directory):
    """Adds front matter to markdown files."""
    year = "1970"
    month = "11"
    day = "12"
    for filename in list_files_recursively(directory):
        if filename.lower().endswith(".md"):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            if content.strip().startswith("---"):
                logging.info(f"Front matter already exists. No changes made. {filename}")
                continue

            now = datetime.datetime.now()
            year, month, day = now.year, now.month, now.day
            date_str = "-".join(map(str, [year, month, day]))

            file_name = os.path.basename(filename)
            front_matter = "---" + "\n" "title: " + '"' + file_name[:-3] + '"' "\n" + "date: " + '"' + date_str + '"' + "\n" + "draft: false" + "\n" + "---" + "\n" + content

            if content != front_matter:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(front_matter)
                logging.info(f'Updated: {filename}')
            else:
                logging.info(f'No changes for: {filename}')


@calc_time
def rename_images_in_directory(directory):
    """Renames images by replacing spaces with underscores."""
    for filename in list_files_recursively(directory):
        if has_extension(filename, IMAGE_EXTENSIONS):  # Check for image extensions case-insensitively
            image_name = os.path.basename(filename)
            directory = os.path.dirname(filename)

            if " " in image_name:
                new_image_name = image_name.replace(" ", "_")
                old_image_path = os.path.join(directory, image_name)
                new_image_path = os.path.join(directory, new_image_name)

                try:
                    os.rename(old_image_path, new_image_path)
                    logging.info(f"Renamed {old_image_path} ---> {new_image_path}")
                except OSError as e:
                    logging.error(f"Failed to rename {old_image_path} --{e}-> {new_image_path}")


def main():
    """Main function to execute all processing steps."""
    print(""">>> Replacing image references in markdown files.""")
    process_directories(args.d, replace_content_in_markdown)
    print(""">>> Adding front matter to markdown files.""")
    process_directories(args.d, add_front_matter_to_markdown)
    print(""">>> Renaming images by replacing spaces with underscores.""")
    process_directories(args.d, rename_images_in_directory)
    print(">>> exit")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="use [-d path_1 path_2 ... ] to specify directory or --help to show help message", description='help you transfer obsidian images markdown to Hugo paper-mod theme markdown', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument("-d", default=None, required=False, nargs="*", help="to specify one or more directory", )
    args = parser.parse_args()
    if args.d is None:
        args.d = [os.getcwd()]
    print("-" * 50)
    print("-" * 50)
    print("""
  ___  ____ ____ ___ ____ ___    _    _   _   _____ ___  
 / _ \\| __ ) ___|_ _|  _ \\_ _|  / \\  | \\ | | |_   _/ _ \\ 
| | | |  _ \\___ \\| || | | | |  / _ \\ |  \\| |   | || | | |
| |_| | |_) |__) | || |_| | | / ___ \\| |\\  |   | || |_| |
 \\___/|____/____/___|____/___/_/   \\_\\_| \\_|   |_| \\___/ 
                                                         
 ____   _    ____  _____ ____  __  __  ___  ____  
|  _ \\ / \\  |  _ \\| ____|  _ \\|  \\/  |/ _ \\|  _ \\ 
| |_) / _ \\ | |_) |  _| | |_) | |\\/| | | | | | | |
|  __/ ___ \\|  __/| |___|  _ <| |  | | |_| | |_| |
|_| /_/   \\_\\_|   |_____|_| \\_\\_|  |_|\\___/|____/ 
                                             """)
    print("Author @jobarasoined")
    print("-" * 50)
    print("-" * 50)

    main()
