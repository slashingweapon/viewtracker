import configparser
import urllib3
import datetime
import certifi
from bs4 import BeautifulSoup

httpPool = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

""" Scrape a fiction page for view and follower counts
    inputs:
        - page: the text of the page to parse
        - logger: logging function to use
    outputs:
        (viewCount, followerCount)
        values default to zero if they aren't found
"""
def scrapeFictionPage(page, logger):
    views = 0
    followers = 0
    soup = BeautifulSoup(page, "html.parser")
    stats = soup.find("div", attrs={"class": "stats-content"})
    if stats != None:
        stats = stats.find_all("div")[1]
        if stats != None:
            stats = stats.find_all("li")
            if stats != None:
                views = int(str.strip(stats[1].string).replace(',',''))
                followers = int(str.strip(stats[5].string).replace(',',''))
                logger("parse", f"views {views} / followers {followers}")
            else:
                logger("parse", "stats not found")
        else:
            logger("parse", "sub-div not found")
    else:
        logger("parse", ".stats-content not found")

    return(views, followers)


""" Collect and log basic information on a fiction
    Takes a config as input, but any dictionary-like item will do.
    Expected members:
        url - Fiction URL
        title - fiction title for statfile purposes
        logfile - runtime staus and/or debuging
        statfile - Where statistics are kept
    
    We visit the URL and, if it is a novel homepage, we collect the following data:
        Current followers
        number of page views
    These are added to the CSV statfile along with datetime and title.
"""
def collectData(config):
    with (
        open(config['logfile'],'a') as logfile, 
        open(config['statfile'],'a') as statfile,
    ):
        def log(stat, data):
            dt = datetime.datetime.now().strftime('%Y%m%d:%H%M%S')
            logfile.write(f"{dt} {config['title']} {stat} {data}\n")

        log("start", "")
        resp = httpPool.request("GET", config['url'])
        log(resp.status, 'fetch')

        if resp.status == 200:
            body = resp.data.decode('utf-8')
            views,followers = scrapeFictionPage(body, log)

            log("stat", "")
            dt = datetime.datetime.now().strftime('%Y%m%d:%H%M')
            statfile.write(f"{dt},{config['title']},{views},{followers}\n")

        log("done", "")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    for secname in config.sections():
        collectData(config[secname])
