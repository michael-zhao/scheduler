# credits to rrc84 for providing guidance of implementation

import urllib.request as rq
import argparse
import json
from time import sleep

def download(url):
    """
    Opens a URL and loads a JSON file's data into a Python object (in this case, data). 
    If the status of data is not success, then retry after a 5s pause, else return the 
    appropriate data.
    """
    print(f"Fetching from: {url}")
    response = rq.urlopen(url)
    data = json.load(response)
    if data["status"] != "success":
        print("Download failed, retrying in 5 seconds")
        sleep(5.0)
        download(url)
    else:
        return data["data"]

# information from https://classes.cornell.edu/content/SP20/api-details
def json_courses(args):
    """
    Returns a list of courses using the Cornell Roster API. 
    """
    acc = []
    for sub in args.subjects:
        url = "https://classes.cornell.edu/api/2.0/search/classes.json?" + \
            "roster=" + args.semester + \
                "&subject=" + sub
        courses = download(url)
        print(f"Classes for {sub} downloaded successfully")
        acc.extend(courses["classes"])
    return acc

def json_subjects(args):
    """
    Returns the subjects from the Cornell Roster API.
    """
    url = "https://classes.cornell.edu/api/2.0/config/subjects.json?" + \
        "roster=" + args.semester
    subjects = download(url)
    return subjects["subjects"]

parser = argparse.ArgumentParser(
    prog="python get_roster_data.py",
    description="Fetches a JSON file from the Cornell Roster."
)
parser.add_argument('-o', '--output', metavar='FILE', default=None, \
    help="Specify a file to output to.")

subparser = parser.add_subparsers()
course_parser = subparser.add_parser("courses", \
    help="Get JSON that lists courses for the given subjects")
course_parser.add_argument('-s', '--semester', metavar="SEM", required=True, \
    help="Specify a semester [SP, SU, FA, WI] and last 2 digits of year")
    
