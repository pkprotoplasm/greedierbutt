# Greedierbutt
This is a repository containing all of the code of the greedierbutt.com website.

The frontend is written in python using the flask framework. The database is stored in MariaDB/MySQL. The backend is built with the celery job management framework, which will call APIs and update database rows asynchronously.

## How to use this repository
Check the files out to your local machine. While the code uses python, some of it assumes a Linux or other Unix-like machine is the host.

You should already have an HTTP server (e.g. Nginx or Apache) capable of reverse proxying or, ideally, serving WSGI applications. No sample configuration is provided for HTTP server setup at this time.

After pulling the repository to your machine, you'll need to take the following actions:

- Change to the repository directory, e.g. `cd ~/gbflask`
- Install venv for python: `pip install venv`
- Create a virtual environment: `python -m venv .venv`
- Activate the virtual environment: `. .venv/bin/activate` (be mindful of the dots)
- Install python dependencies: `pip install -r requirements.txt`
- If `npm` is not available on the machine, install it using `nodeenv --python-virtualenv`
- Install node dependencies: `npm install`
- Use mysqlrestore or another database schema ingestion tool to load `scripts/mysql-structure.sql`
- Use the `scrapescores.py` and `playerprofiles.py` tools in the `scripts` directory to "prime" your database.
- Copy the `greedierbutt.service` file to the user's systemd units directory `~/.config/systemd/user/`
- Enable the service: `systemctl --user enable greedierbutt.service`
- As root, enable linger for the greedierbutt user: `# loginctl enable-linger greedierbutt`

## Configuration
All configuration is done via the `.env` file. An example has been provided in `.env.example`.

## Please note
This code is not fully complete. A functional site is/was running on greedierbutt.com with this exact code, however additional features were planned and have not been implemented.

## What's missing
There is currently no administration console. All administration (such as unbanning users, adding/removing moderators, and removing any data from the database) must be done via SQL.

Moderator and admin privileges are controlled by the `profiles` table's `moderator` and `admin` boolean columns, respectively.

User bans are controlled by the `profiles` table's `blacklisted` column. Ban metadata is provided in the table's `blacklisted_by`, `blacklisted_reason`, and `blacklisted_date` columns. Banned users will have the values in the `scores` table's `scorerank` and `timerank` columns hardcoded to `999999`. This provides fast indexed identification of bans in queries. When unbanning a user, the admin should recalculate ranks on all dates the player had participated in.

## Job troubleshooting
Some jobs are dependent on external APIs that have rate limits that may appear to fluctuate at random depending on the upstream's traffic. If you are concerned about backend jobs being "stuck", review the job server's queue by visiting `http://a.b.c.d:5555/`. WARNING: Don't make this port publicly accessible! This interface allows visitors to terminate and revoke jobs!

## License
GNU General Public License version 3.

## Inspirations
- Greed Butt by europa
- IsaacScores by anonymous
- The Binding of Isaac: Afterbirth, Afterbirth+, and Repentance, by Edmund McMillen