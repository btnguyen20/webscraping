from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url = 'https://www.youtube.com/@JohnWatsonRooney/videos'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('/c/upwork/chromedriver.exe', options=options)

driver.get(url)
time.sleep(5)
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
item = []
last_height = driver.execute_script('return document.documentElement.scrollHeight')

while True:
    driver.execute_script("window.scrollTo(0, " + str(last_height) + ");")
    time.sleep(10)
    new_height = driver.execute_script('return document.documentElement.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@id="details"]'))
    )
    video_list = driver.find_elements('xpath', '//div[@id="details"]')
    for video in video_list:
        # print(video.text)
        link = video.find_element('xpath', './/a[@id="video-title-link"]').get_attribute('href')
        title = video.find_element('xpath', './/a[@id="video-title-link"]').text
        # views = video.find_element('xpath', './/div[@id="metadata-line"]/span[1]').text
        views = video.find_element('css selector', '#metadata-line > span:nth-child(3)').text
        day_posted = video.find_element('xpath', './/div[@id="metadata-line"]/span[2]').text
        video_item = {
            'link': link,
            'title': title,
            'views': views.split()[0],
            'day_posted': day_posted
        }
        if video_item not in item:
            item.append(video_item)

df = pd.DataFrame(item)
pd.DataFrame.to_csv(df, 'result.csv')