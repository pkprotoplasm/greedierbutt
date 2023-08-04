# Greedierbutt
This is a repository containing all of the code of the greedierbutt.com website.

The frontend is written in python using the flask framework. The database is stored in MariaDB/MySQL. The backend is a small collection of bash scripts run by cronjob, which will call python scripts to pull scores from Steam leaderboards, fetch player profiles from Steam API, and calculate ranks and leaderboards.

## How to use this repository
Check the files out to your local machine. While the code uses python, some of it assumes a Linux or other Unix-like machine is the host.

You should already have an HTTP server (e.g. Nginx or Apache) capable of reverse proxying or, ideally, serving WSGI applications. No sample configuration is provided for HTTP server setup at this time.

After pulling the repository to your machine, you'll need to take the following actions:

- Change to the repository directory, e.g. `cd ~/gbflask`
- Install venv for python: `pip install venv`
- Create a virtual environment: `python -m venv .venv`
- Activate the virtual environment: `. .venv/bin/active` (be mindful of the docs)
- Install python dependencies: `pip install -r requirements.txt`
- Use mysqlrestore or another database schema ingestion tool to load `scripts/mysql-structure.sql`
- Set up cron jobs to run the bash scripts (`*.sh`) in `scripts` on your desired schedule
- Copy the `greedierbutt.service` file to the user's systemd units directory `~/.config/systemd/user/`
- Enable the service: `systemctl --user enable greedierbutt.service`
- As root, enable linger for the greedierbutt user: `# loginctl enable-linger greedierbutt`

## Configuration
All configuration is done via the `.env` file. An example has been provided in `.env.example`.

It is *strongly recommended* that you set up a SQL user with reduced privileges for the web frontend. The backend scripts will do the heavy lifting on the scores table; the frontend only needs write access to certain limited fields. Using a reduced-privilege user for the frontend's access will help mitigate any potential future SQL injection vulnerabilities.

## Please note
This code is not fully complete. A functional site is/was running on greedierbutt.com with this exact code, however additional features were planned and have not been implemented.

## License
GNU General Public License version 3.