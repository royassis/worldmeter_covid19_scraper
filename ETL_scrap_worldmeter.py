from functions import *
from selenium import webdriver

# create a new instance of Chrome
logger.info('>>Opening chromium in background')
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

# send a get request to the appropiate webpage
# (in this case the main archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
logger.info('>>Connecting to URL..waiting for response')
browser.get(WAYBACK_MACHINE_CORONA_URL)

f = link_factory(browser, WAYBACK_MACHINE_CORONA_URL)
# Handle a timeout
timeout_get_request(browser, 50)

# Get only new data
logger.info('>>Checking for new links in URL')
prev_urls = get_prev_urls()
all_urls = get_all_urls_matching_regex(browser, URL_REGEX_PATTERN)
new_urls = get_fresh_urls(all_urls,prev_urls)

logger.info('>>Quitting chromium')
browser.quit()

# Iterate over hrefs and download tables from site
if new_urls:
    logger.info('>>Downloading data from links')
    download_csv_from_all_urls(new_urls)
else:
    logger.info('>>No new links')

logger.info('>>End program')

