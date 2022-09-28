from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import json
import sys


chrome: webdriver.Chrome = None
edge: webdriver.Edge = None
firefox: webdriver.Firefox = None
safari: webdriver.Safari = None
quiet: bool = False

def setup_conn() -> None:
    global chrome
    url: str = '...'

    service: Service = Service(executable_path=ChromeDriverManager().install())
    chrome: webdriver.Chrome = webdriver.Chrome(service=service)
    chrome.implicitly_wait(3)
    chrome.get(url)


def login(credentials: dict): pass


def parse_args() -> None:
    """Parse CLI options."""
    parser: argparse.Namespace = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=
"""
A CLI tool to help reserve JCBC slot. Make sure to set the credentials.json properly before the executing tic-bot.py. Run it before 9pm and the program will do the rest when the starter pistol is fired.
""",
                                     epilog=
"""
Example usage:
    pipenv run python tic-bot
"""
                                     )
    parser.add_argument('--quiet',
                        action='store_true',
                        default=False,
                        help='If provided, suppress the STDOUT message.')
    return parser.parse_args()


def log(*args, **kwargs) -> None:
    if not quiet or kwargs.get('file', sys.stdout) != sys.stdout:
        print(*args, **kwargs)


def main() -> int:
    global quiet
    args: argparse.Namespace = parse_args()
    quiet: bool = args.quiet

    with open('credentials.json', encoding='utf-8') as credentials_file:
        credentials: dict[str, str] = json.load(credentials_file)

    setup_conn()
    login(credentials)

    log("Waiting for ...")
    # do some work

    return 0

if __name__ == '__main__':
    exit(main())