from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from time import sleep
import json

month = datetime.now().month
day = datetime.now().day
url = f"https://www.supersaas.com/schedule/jcbc?view=week&day={day}&month={month}"
slot = "Saturday 6:30pm"
slot_backup = "Sunday 6:30pm"

with open("credentials.json", encoding="utf-8") as credentials_file:
    credentials = json.load(credentials_file)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(3)
driver.get(url)

# log in and wait until 21:00 (wait for 0.5 sec in case the server isn't ready yet)
driver.find_element(By.CSS_SELECTOR, "li:nth-child(1)").click()
driver.find_element(By.ID, "name").send_keys(credentials["username"])
driver.find_element(By.ID, "password").send_keys(credentials["password"])
driver.find_element(By.CSS_SELECTOR, "button[name='button']").click()
print("Waiting for 9pm")
while True:
    if datetime.now().strftime("%H") >= "21":
        sleep(0.5)
        break

# party's up
print("Party's up")
driver.refresh()

try:
    driver.find_element(By.CSS_SELECTOR, f"div[title='{slot}']").click()
except NoSuchElementException:
    driver.find_element(By.CSS_SELECTOR, f"div[title='{slot_backup}']").click()
    print("Saturday's not open! Picked Sunday instead! =3=")

try:
    driver.find_element(By.ID, "bbox_new").click()
except ElementNotInteractableException:
    driver.find_element(By.ID, "bbox_wait").click()
    print("Too late! Got into waiting list! Q_Q")

driver.find_element(By.CSS_SELECTOR, "button[name='button']").click()

driver.find_element(By.ID, "form_7").send_keys(credentials["player1"])
driver.find_element(By.ID, "form_10").send_keys(credentials["player2"])
driver.find_element(By.ID, "form_13").send_keys(credentials["player3"])
driver.find_element(By.ID, "form_16").send_keys(credentials["player4"])
driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
print(f"Enjoy your day on {slot.split()[0]}! ;)")
