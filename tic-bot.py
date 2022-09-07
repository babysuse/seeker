from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import json

url = "https://www.supersaas.com/schedule/jcbc?view=week&day=6&month=9"
slot = "Saturday 6:30pm"

with open("credentials.json", encoding="utf-8") as credentials_file:
    credentials = json.load(credentials_file)

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(3)
driver.get(url)

# log in and wait until 21:00
driver.find_element(By.CSS_SELECTOR, "li:nth-child(1)").click()
driver.find_element(By.ID, "name").send_keys(credentials["username"])
driver.find_element(By.ID, "password").send_keys(credentials["password"])
driver.find_element(By.CSS_SELECTOR, "button[name='button']").click()
while False:
    if datetime.now().strftime("%H") == "21":
        break

# party's up
driver.refresh()
driver.find_element(By.CSS_SELECTOR, f"div[title='{slot}']").click()
driver.find_element(By.ID, "bbox_new").click()
driver.find_element(By.CSS_SELECTOR, "button[name='button']").click()

driver.find_element(By.ID, "form_7").send_keys(credentials["name"])
driver.find_element(By.ID, "form_10").send_keys(credentials["name"])
driver.find_element(By.ID, "form_13").send_keys(credentials["name"])
driver.find_element(By.ID, "form_16").send_keys(credentials["name"])
driver.find_element(By.CSS_SELECTOR, "input[value='Submit']").click()
print(f"Enjoy your day on {slot.split()[0]}! ;)")
