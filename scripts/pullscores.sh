#!/bin/bash

if pgrep -fx "/bin/bash /home/greedierbutt/pullyesterdayscores.sh" >/dev/null
then
	exit
fi

cd ~/greedierbutt
for I in "scoresr" "scoresabp" "scoresab"
do
	./scrapescores.py $I $(date -d "10 hours ago" +"%Y%m%d")
done
