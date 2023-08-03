#!/bin/bash

if pgrep -fx "/bin/bash /home/greedierbutt/pullyesterdayscores.sh" >/dev/null
then
	exit
fi

cd ~/greedierbutt
./playerprofiles.py
