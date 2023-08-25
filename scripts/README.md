# Scripts in this directory
- Python files
  - scrapescores.py - Accepts date and dlc arguments. This can be run to pull scores for a specific date via CLI. It's recommended to use this to "prime" your database (pull score information) prior to going live.
  - playerprofiles.py - Pull Steam profile information from API for recently active players, or for up to 200k random profiles.
- SQL files
  - mysql-structure.sql - mysqldump file containing the structure of the database, including stored procedures and views.