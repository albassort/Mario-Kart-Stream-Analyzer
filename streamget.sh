killall streamlink
streamlink $1 360p --twitch-low-latency -O| python streamget.py pipe:0 $1