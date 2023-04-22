from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

url = 'https://www.youtube.com/@JohnWatsonRooney/videos'
driver = webdriver.Chrome('/c/upwork/chromedriver.exe')
driver.get(url)

item = []
try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//div[@id="details"]'))
    )
    video_list = driver.find_elements('xpath', '//div[@id="details"]')
    for video in video_list[:10]:
        link = video.find_element('xpath', './/a[@id="video-title-link"]').get_attribute('href')
        title = video.find_element('xpath', './/a[@id="video-title-link"]').text
        views = video.find_element('xpath', './/div[@id="metadata-line"]/span[1]').text
        day_posted = video.find_element('xpath', './/div[@id="metadata-line"]/span[2]').text
        video_item = {
            'link': link,
            'title': title,
            'views': views.split()[0],
            'day_posted': day_posted
        }
        item.append(video_item)
finally:
    driver.quit()

df = pd.DataFrame(item)
print(df)