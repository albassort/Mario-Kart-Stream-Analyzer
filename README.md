# Mario-Kart-Stream-Analyzer
**By Caroline Marceano**

A python script that watches mario cart footage, and outputs rank data

# Version 2 notes:
    1. Todo.py was completely removed
    2. Ascii was completely removed; now individual pixel scanning. Though this is inefficient in python. If i am going to work on this again, a Nim+JS port is very likely.
    3. id.py was completely rewritten
    3. init.py was renamed to readwrite.py; for clarity of its purpose
    4. asciigen was removed, and almost completely rewritten, replaced with compile. And is no longer run separately from streamget, but rather run on a separate thread as they are ready to be processed
    5. streamget.py almost completely rewritten
    6. readwrite.py was touched up, comments added, slight code changes where code could be improved.
    7. Just an overall increase in code quality. The only unpolished code is in stats.py and pixget.py. However, the code in those is pretty simple and easy to follow.
    8. streamers were moved to /archive
    9. no more /streamers/streamer/out, the input is also the output dir. 
(all this data was generated using ```https://www.youtube.com/watch?v=1lDOgP-Kh3s```)
This has all translated to a technical speed increase of about 100000x if you include download times. Outside of download times, a test yielded a result of 216s vs 1587s (new vs old) or a 7.34x increase in speed. This was recorded on a i5-4570S on DDR3 1300Mhz ram. Ram and CPU threads will greatly improve performance.

Individual compile times are around 3.3s. As opposed to the old times of 30s +.

Additionally, excluding the massive speed increases. There is... a COLOSSAL space difference.
Previously. (384808 + 7692924) KB vs  147656 Kb, or a 54x space decrease. More can be done, smaller video sizes, etc. However I am happy with this result.


# Dependencies:
./installdeps
We currently only support Arch and Apt.
If you are not on a debian-like or if installdeps fails to read your arch-derivative:
You must install ffmpeg and tesseract-ocr via some means. I cannot help you.
pip dependencies:
``matplotlib==3.3.4, numpy==1.22.0, opencv_python==4.5.5.62, Pillow==9.0.0, pip==21.3.1 pytesseract==0.3.8``
``pytube==11.0.2, setuptools==58.2.0, string_color==1.2.1, thefuzz==0.19.0, wheel==0.34.2``

# id.py notes:
This project is possible via machine learning. id.py is the basis for this
In the folders id/digit, you place images, and id.py generates a list of coordinates where it is ALWAYS white.
compile.py them uses this to create a best guess.
MKSA comes pre-packages with ``id.tar.gz`` which contains a premade id/ folder.
In order to use MKSA you MUST extract it and run ``python id.py``.
This is done automatically in installdeps, so if you've run it this processes was already done for you.

Because of this method, the quality of the output is based entirely upon the reference images. 
If you wish to expand upon this reference, its best to extract the frames from the ``video.avi`` outputed from compilation; however you can can process any image the same way with the ``process` function in streamget.py

# How do i run it?
`streamget.sh, todo.py, stats.py id.py`
MKSA currently supports youtube and Twitch

# from a youtube video:
Be sure that your video is available in 360p30!
``python streamget.py youtubevideo``
It really is that simple. It will download it and it will automatically watch and write its output.
check archive/youtubechannel/update for the output.

# from a live twitch stream
``./streamget.sh https://twitch.tv/yourfavoritetwitchstreamer``
Same as stated above, be sure that a 360p30 stream is avalible

# Why am i getting no output?
Currently MKSA is not a very dynamic thing. 
This could be done at another time, if i decide to continue working on it.
You must be sure that the center and lower end of the stream is not obstructed with a hud of any kid

folder is appended to todo.txt for later 'compilation'.

# What does the future hold for MKSA?
Not much. Maybe a Nim-recode if I ever feel the need to continue this.
This is more of a precuser to a bigger project, I may or may not be able to do.
This has been a very relaxing break from a different project im doing. 
