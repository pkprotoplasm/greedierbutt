#!/bin/bash

cd ~/greedierbutt

# Scrape recent scores (this happens a bit over an hour after the daily ends to allow
# for steam CDN propagation). Rerank yesterday after pulling.
for I in "scoresr" "scoresabp" "scoresab"
do
	./scrapescores.py $I $(date -d "13 hours ago" +"%Y%m%d")
	./scrapescores.py $I $(date -d "37 hours ago" +"%Y%m%d")
	./scrapescores.py $I $(date -d "61 hours ago" +"%Y%m%d")
	./scrapescores.py $I $(date -d "85 hours ago" +"%Y%m%d")
	./scrapescores.py $I $(date -d "109 hours ago" +"%Y%m%d")
	./scrapescores.py $I $(date -d "133 hours ago" +"%Y%m%d")
done

# Full rerank for newly banned players.
./rerank.py

# Recalculate the leaderboards with new rankings.
./recalcleaders.py $(date -d "91 days ago" +"%Y%m%d")

# Update up to 200k random outdated player profiles
./playerprofiles.py all
