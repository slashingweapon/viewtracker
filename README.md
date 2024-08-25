# View Tracker

I wrote this little guy to figure out when I should release new chapters of my fictions on Royal Road.

When you release a chapter, it briefly appears on the "Recently Active" list and people are slightly more likely to 
click on it. Also, if I know when people are most likely to tune in then I know when my best release times are. Why 
should I push myself to release a chapter in the morning if most of my readers show up in the afternoons?

The main tool I have for measuring page views is the "Total Views" number from the fiction's Statistics block. So I'll
scrape that periodically, take a reading, and create a log. I'm thinking every half-hour would be sufficient.

A second program will read the logs and perform whatever analysis we want.

## Installation

The steps are:
1. Check out viewtracker to whatever directory you like.
2. Set up a virtual environment.
3. Install the required python packages.
4. Deactive venv.
5. Add the cron job.

```bash
git clone git@github.com:slashingweapon/viewtracker.git
cd viewtracker

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate

crontab -e
```

The last line will bring up a `vi` editor so you can modify your crontab file.

If you want to run the collector every thirty minutes, the line you add to your crontab file should be like `30 * * * * /Users/myaccount/Projects/viewtracker/collector.sh`.

Do I need to tell you to use your own project path? Let's hope not.

# Configuration

Copy `example.ini` to `config.ini` and edit it to your needs. The file should be commented well enough to guide you.
