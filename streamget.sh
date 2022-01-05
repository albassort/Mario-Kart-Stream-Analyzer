#!/bin/bash
killall streamlink
streamlink $1 360p30 --twitch-low-latency -O 2> /dev/null | python streamget.py pipe:0 $1 2>/dev/null
