# Scripts in this directory
- Bash Scripts
  - pullscores.sh - Should be run periodically throughout the day (e.g. every 10 minutes if possible). Scrapes all three DLC leaderboards on Steam
  - pullprofiles.sh - Should be run once a day. Bulk download of Steam profile data for active players who have not recently had profiles updated in our database
  - pullyesterdayscores.sh - Should be run once a day. Pulls a final score list for the previous day and recalculates leaderboards
- Python files
  - scrapescores.py - Accepts date and dlc arguments. Pull the given DLC's steam leaderboard for the given date
  - playerprofiles.py - Pull Steam profile information from API for recently active players.
  - rerank.py - Recalculates score and time ranks (adjusting for banned players)
  - recalcleaders.py - Recalculates leaderboards, which are populated as tables & views in the database

Note: You will need to update various paths in the below files. The bash scripts were executed by cronjobs, and expected the python files to be in ~/greedierbutt. This may not match your desired environment.