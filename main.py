import pandas as pd
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



option = webdriver.ChromeOptions()
option.add_argument('— incognito')

browser = webdriver.Chrome(executable_path=r"C:\Users\roy\Desktop\chromedriver.exe", chrome_options=option)

url = 'https://web.archive.org/web/20200101000000*/https://www.worldometers.info/coronavirus/'
browser.get(url)

timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class=’avatar width-full rounded-2']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

elems = browser.find_elements_by_xpath("//a[@href]")
refs = []
for elem in elems:
    ref = elem.get_attribute("href")
    pat = r'https://web.archive.org/web/\d+/https://www.worldometers.info/coronavirus/'
    match = re.search(pat,ref)
    if match:
        refs.append(match.group())


for ref in refs:
    data = pd.read_html(ref)
    df = data[2]