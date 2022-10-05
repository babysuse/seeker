from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import argparse
import json
import random
import sys


chrome: webdriver.Chrome
quiet: bool = False
retry: int = 10  # refresh time before giving up

def setup_conn() -> None:
    global chrome
    month: int = datetime.now().month
    day: int = datetime.now().day
    url: str = f'https://www.supersaas.com/schedule/jcbc?view=week&day={day}&month={month}'

    service: Service = Service(executable_path=ChromeDriverManager().install())
    chrome = webdriver.Chrome(service=service)
    chrome.implicitly_wait(1)
    chrome.get(url)


def reserve(take_humiliation: bool, credentials: dict) -> None:
    """Fill in player's info and reserve the slot."""
    humiliation: bool = False
    try:
        chrome.find_element(By.ID, "bbox_new").click()
    except ElementNotInteractableException:
        if not take_humiliation:
            log('Too late! Try next time! >_<', file=sys.stderr)
            exit(1)
        chrome.find_element(By.ID, 'bbox_wait').click()
        humiliation: bool = True

    try:
        chrome.find_element(By.CSS_SELECTOR, 'button[name="button"]').click()

        chrome.find_element(By.ID, 'form_7').send_keys(credentials['player1'])
        chrome.find_element(By.ID, 'form_10').send_keys(credentials['player2'])
        chrome.find_element(By.ID, 'form_13').send_keys(credentials['player3'])
        chrome.find_element(By.ID, 'form_16').send_keys(credentials['player4'])
        chrome.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
    except:
        log('Not enough credit to create a new booking!', file=sys.stderr)

    if humiliation:
        log('Too late! Added to waiting list! Q_Q')
    else:
        log('Easy peasy lemon squeezy!')


def try_secondary(slot: str) -> str:
    """Get backup slot."""
    try:
        chrome.find_element(By.CSS_SELECTOR, f'div[title="{slot}"]').click()
    except NoSuchElementException:
        return ''
    return slot


def try_primary(slot: str, backup_slot: str) -> str:
    """Get primary slot."""
    try:
        chrome.find_element(By.CSS_SELECTOR, f'div[title="{slot}"]').click()
    except NoSuchElementException:
        return try_secondary(backup_slot)
    return slot


def get_slot(slot: str, slot_backup: str) -> str:
    """Refresh the page with random back off in case being banned for requesting too aggressive."""
    global retry
    log("Party's up")
    result: str = ''
    while retry > 0 and not result:
        chrome.refresh()
        result = try_primary(slot, slot_backup)
        retry -= 1
        sleep(random.random())
    return result


def login(credentials: dict):
    chrome.find_element(By.CSS_SELECTOR, 'li:nth-child(1)').click()
    chrome.find_element(By.ID, 'name').send_keys(credentials['username'])
    chrome.find_element(By.ID, 'password').send_keys(credentials['password'])
    chrome.find_element(By.CSS_SELECTOR, 'button[name="button"]').click()


def parse_args() -> argparse.Namespace:
    """Parse CLI options."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=
"""
A CLI tool to help reserve JCBC slot. Make sure to set the credentials.json properly before the executing tic-bot.py. Run it before 9pm and the program will do the rest when the starter pistol is fired.
""",
                                     epilog=
"""
Example usage:
    pipenv run python tic-bot --slot "Saturday 11am" --backup-slot "Friday 7:30pm"
"""
                                     )
    parser.add_argument('--slot',
                        default='Saturday 6:30pm',
                        choices=['Friday 6pm', 'Friday 7:30pm', 'Friday 9pm', 'Friday 10:30pm', 'Saturday 11am', 'Saturday 12:30pm', 'Saturday 2pm', 'Saturday 3:30pm', 'Saturday 5pm', 'Saturday 6:30pm', 'Saturday 8pm'],
                        help='Slot to be reserved. Valid options are "Friday 6pm", "Friday 7:30pm", "Friday 9pm", "Friday 10:30pm", "Saturday 11am", "Saturday 12:30pm", "Saturday 2pm", "Saturday 3:30pm", "Saturday 5pm", "Saturday 6:30pm", "Saturday 8pm". Default to "Saturday 6:30pm".')
    parser.add_argument('--backup-slot',
                        default='Sunday 6:30pm',
                        choices=['Friday 6pm', 'Friday 7:30pm', 'Friday 9pm', 'Friday 10:30pm', 'Sunday 11am', 'Sunday 12:30pm', 'Sunday 2pm', 'Sunday 3:30pm', 'Sunday 5pm', 'Sunday 6:30pm'],
                        help='Backup slot to be reserved in case it closes on Saturday. Slots on Sunday are "Sunday 11am", "Sunday 12:30pm", "Sunday 2pm", "Sunday 3:30pm", "Sunday 5pm", "Sunday 6:30pm".')
    parser.add_argument('--quiet',
                        action='store_true',
                        default=False,
                        help='If provided, suppress the STDOUT message.')
    parser.add_argument('--queue',
                        action='store_true',
                        default=False,
                        help='If provided, if failed to get a slot, join the queue.')
    return parser.parse_args()


def log(*args, **kwargs) -> None:
    if not quiet or kwargs.get('file', sys.stdout) != sys.stdout:
        print(*args, **kwargs)


def main() -> int:
    global quiet
    args: argparse.Namespace = parse_args()
    quiet = args.quiet

    with open('credentials.json', encoding='utf-8') as credentials_file:
        credentials: dict[str, str] = json.load(credentials_file)

    setup_conn()
    login(credentials)

    log("Waiting for 9pm")
    while True:
        if datetime.now().strftime("%H") >= "21":
            break

    slot: str = get_slot(args.slot, args.backup_slot)
    if not slot:
        log('The server is possibly down!', file=sys.stderr)
        exit(1)

    reserve(args.queue, credentials)
    log(f'Enjoy your day on {slot.split()[0]}! ;)')
    return 0

if __name__ == '__main__':
    exit(main())
