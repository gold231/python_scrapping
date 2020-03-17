import requests
import bs4
import datetime
import os
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options



page_url = "https://www.disneyplus.com/login"
username = "dtest-1984@gmail.com"
password = "Test!234"

# open selenium chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")
current_path = os.getcwd()
driver_path = os.path.join(os.getcwd(), 'chromedriver')
# browser = webdriver.Chrome(driver_path, options=chrome_options)
browser = webdriver.Chrome(driver_path)

#check if an element with certain id exists
def check_exists_by_id(elmId):
    try:
        browser.find_element_by_id(elmId)
    except NoSuchElementException:
        return False
    return True
#check if a certain element exists by css selector
def check_exists_by_css(cssSelector):
    try:
        browser.find_element_by_css_selector(cssSelector)
    except NoSuchElementException:
        return False
    return True
# check if a button is clickable 
def check_button_clickable_css(cssSelector):
    try:
        browser.find_element_by_css_selector(cssSelector).click()
        return True
    except:
        return False

browser.get(page_url)

# input user name
while check_exists_by_id('email')==False:
    sleep(0.5)
input_user = browser.find_element_by_id("email")
input_user.clear()
input_user.send_keys(username)

# click continue button
while check_exists_by_id('dssLogin')==False:
    sleep(0.5)
username_form = browser.find_element_by_id("dssLogin")
username_form.submit()

# input password
while check_exists_by_id('password')==False:
    sleep(0.5)
input_pass = browser.find_element_by_id("password")
input_pass.clear()
input_pass.send_keys(password)

# login form submit
while check_exists_by_id('dssLogin')==False:
    sleep(0.5)
login_form = browser.find_element_by_id("dssLogin")
login_form.submit()

while check_exists_by_id('home-collection')==False:
    sleep(0.5)
all_rows = browser.find_elements_by_css_selector("div#home-collection>div")
data_all = {"sections" : []}
for row in all_rows:
    if all_rows.index(row)==0 or all_rows.index(row)==1:
        continue
    row_name = row.find_element_by_css_selector("div>h4").get_attribute('innerHTML').strip()
    row_data = {"Name": row_name, "items": []}
    items = row.find_elements_by_css_selector("div>div.slick-slider>div.slick-list>div.slick-track>div.slick-slide")
    for item in items:
        image = item.find_element_by_css_selector("div.image-container img")
        item_name = image.get_attribute('alt')
        item_image = image.get_attribute('src')
        image_anchor = item.find_element_by_css_selector("div>a")
        image_anchor.click()
        while check_exists_by_id('webAppScene')==False:
            sleep(0.5)
        item_url = browser.current_url
        item_data = {"Name": item_name, "Image": item_image, "URL": item_url}
        row_data["items"].append(item_data)
        browser.execute_script("window.history.go(-1)")
    data_all["sections"].append(row_data)

json_string = json.dumps(data_all)

file = open("result.txt", "w")
file.write(json_string)
file.close()






