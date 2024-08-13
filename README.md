### Obsdian to PaperMod
this script aimed to help you transfer your writups/notes from obsidian markdown to hugo PaperMod markdown 
there is no huge difference except for how images/screenshots
are written 

i use flameshot to take screenshots and if i paste it (without saving) in obsidian

`![[Pasted image 20240813193651.png]]` notice that the date is added by obsidian and not flameshot (this if you copied the imaged only. if you saved the image usually flameshot format will be something like that) 
`![[2024-08-13_20-39-06.png]]` and if there text before the format that should be also fine `![[Screanshot 2024-08-13_20-39-06.png]]`


# Markdown Image Reference and Front Matter Processor

This script helps in transforming markdown files by replacing image references, adding front matter, and renaming images within specified directories.

## Features

- **Replace Image References:** The script finds image references in markdown files and replaces them with a formatted version that replaces spaces with underscores and links to a specified directory.
- **Add Front Matter:** It adds front matter to markdown files if it isn't already present, extracting date information from the image references.
- **Rename Images:** The script renames image files in the specified directories by replacing spaces with underscores.

## Requirements

- Python 3.x

## Usage

```bash
python script.py -d path_1 path_2 ...
````

### Arguments

- `-d` or `--directory`: Specify one or more directories to process. If not provided, **the current working directory will be used.**

### Example

`python script.py -d /path/to/markdowns /another/path`

This command will process all markdown files in the specified directories.

## Notes

- Ensure that you have backed up your markdown files before running this script, as it will modify the files in place.
- The script is designed to handle `.md` files and image formats like `.png`, `.jpeg`, and `.jpg`.
- move all the screenshots afterwards to your HUGOSITE/static/screenshots folder


Author: @jobarasoined