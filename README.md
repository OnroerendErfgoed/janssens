# Janssens: your friendly neighbourhood duplicate image finder

Janssens is a simple script to search a file system folder for duplicate images. Janssens does not compare filenames, but the images themselves by calculating the dhash for every image and comparing them.

## Installation

- Clone this repo
- Install the requirements: *pip install -r requirements.txt*
- Configure the *janssens.py* file and change the FOLDER variable to your image folder. A folder of testdata is included. It contains some examples of duplication Janssens can detect.
- Janssens calculates the overlap between two dhashes. The higher the overlap, the more likely two images are identical or similar. You can control the THRESHOLD that reports a match. Any similarities lower than this threshold will not be reported. Experience suggests that matches above 90% are a good match while between 85 and 90 is often a match but has more false postives and below 85 generally has too many false positives.
- Run the script: *python janssens.py*
