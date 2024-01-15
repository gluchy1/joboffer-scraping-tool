"""
Job Scraper

This script is designed to scrape job offer information from a given website.

It uses Selenium, BS4, Spacy and other libraries alongside MongoDB integration.

~ ~ keep updating chromedriver.exe if code doesn't run.

"""

import os
from collections import Counter
from typing import List

# NLP
import spacy

# BS
from bs4 import BeautifulSoup

# mongo
from pymongo import MongoClient

# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# .env
from dotenv import load_dotenv

# enviromental variable
load_dotenv(dotenv_path="config.env")


def scrape_page(driver: webdriver.Chrome, page_number: int):
    # Get scrape URL from environment variable
    base_url = os.getenv("SCRAPE_URL")
    url = f"{base_url}{page_number}"
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@data-test='link-offer']"))
    )


def get_job_details(driver: webdriver.Chrome) -> (str, str):
    try:
        job_title = driver.find_element(By.XPATH, "//h1[@data-scroll-id='job-title']").text
    except:
        job_title = "N/A"

    try:
        company_name_element = driver.find_element(By.XPATH, "//h2[@data-scroll-id='employer-name']")
        company_name = company_name_element.text.split("\n")[0]
        company_name = company_name.replace("About the company", "").replace("O firmie", "").strip()
    except:
        company_name = "N/A"

    return job_title, company_name


def get_webdriver() -> webdriver.Chrome:
    """Sets up and returns a Selenium WebDriver."""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    chrome_driver_path = os.path.join(project_dir, "chromedriver.exe")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(chrome_driver_path)

    return webdriver.Chrome(service=service, options=chrome_options)


class JobScraper:
    def __init__(self):
        self.nlp_pl = None
        self.nlp = None
        self.collection = None
        self.db = None
        self.client = None
        self.initialize_database()
        self.initialize_nlp()

    # used for connection to MongoDB
    def initialize_database(self):
        # Get MongoDB URL from environment variable
        mongo_url = os.getenv("MONGO_URL") # gets it from config.env
        try:
            self.client = MongoClient(mongo_url)
            self.db = self.client['job_offers_db'] # name of the DB
            self.collection = self.db['job_offers'] # name of the collection
        except Exception as e:
            print(f"Failed to connect to database. Error: {e}")

    # spaCy usage for nlp
    def initialize_nlp(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp_pl = spacy.load("pl_core_news_sm")

    # spaCy usage for nlp
    def extract_requirements(self, text: str) -> List[str]:
        # Extracts job requirements from given string using NLP.
        return self.extract_keywords(self.nlp, text) + self.extract_keywords(self.nlp_pl, text)

    # spaCy usage for nlp
    @staticmethod
    def extract_keywords(nlp_engine, text: str) -> List[str]:
        doc = nlp_engine(text)
        return [token.text for sent in doc.sents for token in sent if token.pos_ in ["NOUN", "PROPN"]]

    # used with process_offer
    def scrape_and_store(self):  # main fuction for scraping
        with get_webdriver() as driver:
            for page_number in range(1, 11):  # change the range as needed
                scrape_page(driver, page_number)
                offers = driver.find_elements(By.XPATH, "//a[@data-test='link-offer']")
                for offer in offers:
                    self.process_offer(driver, offer)


    # opens the new tab with a job offer, scrapes it and saves the data in the DB
    def process_offer(self, driver: webdriver.Chrome, offer):  # function for processing data to DB
        job_link_href = offer.get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(job_link_href)

        job_title, company_name = get_job_details(driver)
        requirements = self.get_requirements(driver)

        job_offer_data = {
            'Link': job_link_href,
            'Job Title': job_title,
            'Company Name': company_name,
            'Requirements': requirements
        }

        if not self.collection.find_one({'Link': job_link_href}):
            self.collection.insert_one(job_offer_data)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # gets requirements from the job offer
    # if it fails to get requirements from the list, it searches for it in the job desc.
    def get_requirements(self, driver: webdriver.Chrome) -> List[str]:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        requirements_list = soup.find("ul", class_="offer-viewEX0Eq-")
        requirements = [
            item.text for item in requirements_list.find_all("p", class_="offer-viewU0gxPf")
        ] if requirements_list else []

        if not requirements:
            try:
                job_description = driver.find_element(By.XPATH, "//div[@data-scroll-id='job-description']").text
            except:
                job_description = ""
            requirements = self.extract_requirements(job_description)

        return requirements

    # from the collected data, sorts and prints the requirements
    def print_sorted_requirements(self):
        all_requirements = [
            req for job_offer in self.collection.find({}, {'Requirements': 1, '_id': 0})
            for req in job_offer.get('Requirements', [])
        ]
        requirements_count = Counter(all_requirements)
        sorted_requirements = sorted(requirements_count.items(), key=lambda x: x[1], reverse=True)

        for requirement, count in sorted_requirements:
            print(f'[{requirement}][Amount = {count}]')


if __name__ == "__main__":
    scraper = JobScraper()
    scraper.scrape_and_store()
    scraper.print_sorted_requirements()
