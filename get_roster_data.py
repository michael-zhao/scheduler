# credits to rrc84 for providing guidance of implementation

import urllib.request as rq
import argparse
import json
from time import sleep

def download(url):
    print(f"Fetching from: {url}")
    response = rq.urlopen(url)
    data = json.load(response)
    if data["status"] != "success":
        print("Download failed, retrying in 1 second")
        sleep(1.0)
        download(url)
    else:
        return data["data"]

# information from https://classes.cornell.edu/content/SP20/api-details
def json_courses(args):
    acc = []
    for sub in args.subjects:
        url = "https://classes.cornell.edu/api/2.0/search/classes.json?" + \
            "roster=" + args.semester + \
                "&subject=" + sub
        courses = download(url)
        print(f"Classes for {sub} downloaded successfully")