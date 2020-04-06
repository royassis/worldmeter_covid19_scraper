from datetime import datetime
from settings import  *
import re
import glob

# Impored for scraping TheWaybackMachine
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def timeout_get_request(browser, timeout = 50):
    """Set timeout for response from site"""
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='calendar-day ']")))
    except TimeoutException:
        logger.info("Timed out waiting for page to load")
        browser.quit()


def download_csv_from_all_urls(new_refs):
    """downloads csv from all urls"""
    urls_len = len(new_refs)

    for i, ref in enumerate(new_refs):

        logger.debug(f'Downloading file {i + 1} from {urls_len}: {ref}')

        try:
            container = pd.read_html(ref, match='Country')
            df = container[-1]
            df['ref'] = ref

            date_str = re.search('\d{8}',ref).group()
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            df['date'] = date_obj

            date_repr_to_file = date_obj.strftime('%b-%d-%Y')

            outfile = date_repr_to_file + '.csv'
            outpath = os.path.join(DATA_DIR, outfile)
            df.to_csv(outpath)
        except:
            logger.error(f'There have been a problem with {ref}')


def get_all_urls_matching_regex(browser, url_pattern):
    """Scraps the wayback machine for coronavirus worldmeter and gets all urls"""
    refs = []
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        ref = elem.get_attribute("href")
        match = re.search(url_pattern, ref)
        if match:
            refs.append(match.group())
    return refs

def get_fresh_urls(all_urls, prev_urls):
    """Compare downloaded urls to all scraped urls"""
    new_refs = list(set(all_urls) - set(prev_urls))
    # rmemove today's main_url
    new_refs = new_refs[:-1]
    retval = new_refs

    if len(new_refs) > 0:
        retval = None

    return retval


def get_prev_urls():
    """Read all downloaded csv's and make a list of all old urls"""
    prev_urls=[]
    all_files = glob.glob(DATA_DIR + "/*.csv")
    for filename in all_files:
        df = pd.read_csv(filename)
        try:
            prev_urls = prev_urls + df.ref.to_list()
        except:
            pass
    return list(set(prev_urls))



# Unused functions
# ------------------------------------------
def log_errors_and_runtime(errors, delta, log_dir):

    errors = "\n".join(errors)
    date_str = datetime.today().strftime("%d%m%Y")
    outfile = date_str + '.txt'
    outpath = os.path.join(log_dir, outfile)

    with open(outpath, 'w+') as filehandle:
        filehandle.writelines(f"errors:{errors}")
        filehandle.writelines('\n---------------------\n')
        filehandle.writelines(f"time elapsed in seconds: {delta}")
        filehandle.writelines('\n---------------------\n')

def update_ref_log(hrefs,new_refs, hrefs_path):

    new_refs = pd.DataFrame(new_refs, columns=["href"])
    hrefs = pd.concat([hrefs,new_refs],axis = 0, ignore_index=True, sort=False)
    hrefs.to_csv(hrefs_path, index_label = 'id')


def verbose(i, arrsize, url):
    """Function that prints state of download"""
    print(f'Downloading file {i + 1} from {arrsize}: {url}')





class foo(object):
    def __init__(self, url=None, browser=None):

        self.browser = browser
        self.main_url = url
        self.all_links =[]
        self.filters=[]
        self.valid_urls =[]

    def get_all_urls(self):
        elems = self.browser.find_elements_by_xpath("//a[@href]")
        elems = [elem.get_attribute("href") for elem in elems]
        self.all_links = elems

    def add_filter(self, filter_arr):
        self.filters = self.filters + filter_arr

    def apply_all_filters(self, url):
        results = []
        for filter in self.filters:
            result = filter(url)
            results.append(result)
        return all(results)

    def filter_urls(self):
        for link in self.all_links:
            result = self.apply_all_filters(link)
            if result:
                self.valid_urls.append(result)

