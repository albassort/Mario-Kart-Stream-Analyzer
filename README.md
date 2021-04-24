# Mario-Kart-Stream-Analyzer
# By Caroline M, Albassort.
A program that watches twitch, records each Mario Kart 8 game given, and generates a graph of data over time.
# Dependencies:
`pip install stringcolor opencv-python pillow tesseract streamlink` or `./installdeps.sh`

additonally:

MKSA requires ImageMagick and JP2A
on Arch:
`pacman -S jp2a imagemagick `
On apt:
`sudo apt-get install imagemagick jp2a `
# How do i run it?
There are 4 scripts intended to be interfaced with by you from the terminal

`streamget.sh, todo.py, stats.py id.py`

# streamget.sh
Interfacing with streamget is very simple. 

`./streamget.sh https://www.twitch.tv/MyFavoriteTwitchStreamer`

streamget.sh works by connecting to MYFS and piping the frames into streamget.py. CV2 will then importt the frame and analyize

pixget.py is then caleld to do pixel checks. pixget pingpongs bettween streamget.py managing the states.

upon confirmed 'go', a channel, at ./MFTS/date/${digit} (digit is equal to (ls | wc -l )-1)

at 'end check' the folder is appended to todo.txt for later 'compilation'.

# todo.py

`./todo.py` ((takes no args))
todo.py manages compilation of the raw frames, first into cropped greyscale images,
and then into binary black and white images. This happens at /processed/${digit}.
It also extracts data from the original folder and moves it over into the new final generated folder at ./channel/out/

