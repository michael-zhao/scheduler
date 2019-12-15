# credits to rrc84 for providing guidance of implementation from CS 3110
# heavily inspired/drawn from his implementation here:
# https://github.coecis.cornell.edu/wm274/cs3110-a6/blob/master/get_json.py

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

def main():
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
    course_parser.add_argument('subjects', nargs='+', metavar='sub', help="the subject from the roster")
    course_parser.set_defaults(func=json_courses)

    subject_parser = subparser.add_parser("subjects", \
        help="Get JSON that lists available subjects for the semester")
    subject_parser.add_argument('-s', '--semester', metavar='SEM', required=True,
                                help="Specify a semester [SP, SU, FA, WI] and last 2 digits of year")
    subject_parser.set_defaults(func=json_subjects)

    args = parser.parse_args()

    if args.output is None:
        try:
            s = json.dumps(args.func(args), indent=2)
            print(s)
        except AttributeError:
            parser.error("too few arguments") # from https://bit.ly/2qSyjk8
    else:
        with open(args.output, 'w') as out:
            try:
                json.dump(args.func(args), out, indent=2)
            except AttributeError:
                parser.error("too few arguments")

if __name__ == "__main__":
    main()
