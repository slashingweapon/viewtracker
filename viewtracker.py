import configparser
import urllib3
import datetime
import certifi

httpPool = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

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

        resp = httpPool.request("GET", config['url'])
        log(resp.status, 'fetch')

        print(resp.data)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    for secname in config.sections():
        collectData(config[secname])
