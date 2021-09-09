# Mario-Kart-Stream-Analyzer
**By Caroline M, Albassort**


**Contact at retkid#9135 on discord**


**Listen to my music at abnormalaudio.com**


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


you can use vods or video files:


(make sure files are in 360p currently!


`python streamget.py videofile.mp4 outputname/`


you can also downloads videos from youtube or twitch


`python streamget.py videolink.com outputname`


this even works for playlists!
(just make sure everything is in 360p for now. 720p and 1080p coming at a later time)


in addition:

Half and quarter modes for offline!


streamget.sh works by connecting to MYFS and piping the frames into streamget.py. CV2 will then importt the frame and analyize
pixget.py is then caleld to do pixel checks. pixget pingpongs bettween streamget.py managing the states.

upon confirmed 'go', a channel, at ./MFTS/date/${digit} (digit is equal to (ls | wc -l )-1)

at 'end check' the folder is appended to todo.txt for later 'compilation'.

# todo.py

`python todo.py` ((takes no args))
todo.py manages compilation of the raw frames, first into cropped greyscale images,
and then into binary black and white images. This happens at /processed/${digit}.
It also extracts data from the original folder and moves it over into the new final generated folder at ./channel/out/digit

./channel/out/digit/html is where the final archive of the data is compiled to. The processed/0 and channel/date and can be deleted if you don't want any backups encase something goes wrong...

# stats.py
`python stats.py`

Used to explore your achives and doesn't need much explaining

# ID.py
`python id.py -regen or no arg.`

Generates a list of consistent elements of all images in id/ranknumbers. compiled to id/ranknumbershtml

to learn more, read id/README.md and the comments in id.py

# Roadmap 
V1 has some issues. My roadmap is as follows

-Add GUI (programmed in Nim)

-Recode pixget to be more efficent and use less pixel checks

-Add 1080p and 720p support because currnetly it only works on 360p streams.

-add more todo.py options, to remove all sources and reduce disk usage.

-Add item detection 

-Add the ability to scrape twitch bets ((BETA FEATURE, PLEASE CONTACT ME IF YOU ARE A PARTNER AND WANT TO HEL DEVEOPLENT!!!!!!!!!!!!!!!!!!!!!!!!!!!))

