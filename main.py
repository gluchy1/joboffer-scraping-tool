import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import spacy
from collections import Counter

'''
In order to make it more versatile, I've added lines of code that make program able to access the
"chromedriver.exe" without making it necessary to modify the path of the file for each unique user that
downloads this code from repo.
'''

project_dir = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = os.path.join(project_dir, "chromedriver.exe")

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()

driver.get("https://www.pracuj.pl/praca/programista%20python;kw/warszawa;wp?rd=30&et=1%2C17")
driver.switch_to.window(driver.window_handles[0])
driver.find_element(By.XPATH, "//button class[contains(., 'Akceptuj wszystkie')]").click()

nlp = spacy.load("en_core_web_sm")
nlp_pl = spacy.load("pl_core_news_sm")

def extract_requirements(text):
    doc = nlp(text)
    requirements = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                requirements.append(token.text)

    doc_pl = nlp_pl(text)
    for sent in doc_pl.sents:
        for token in sent:
            if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                requirements.append(token.text)

    return requirements

job_offers_list = []

job_offers = driver.find_elements(By.XPATH, "//a[@data-test='link-offer']")
for offer in job_offers:
    job_link_href = offer.get_attribute("href")

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(job_link_href)

    try:
        job_title_element = driver.find_element(By.XPATH, "//h1[@data-scroll-id='job-title']")
        job_title = job_title_element.text
        if "O firmie" in job_title:
            job_title = job_title.replace("O firmie", "").strip()
        elif "About the company" in job_title:
            job_title = job_title.replace("About the company", "").strip()
    except:
        job_title = "N/A"

    try:
        company_name_element = driver.find_element(By.XPATH, "//h2[@data-scroll-id='employer-name']")
        company_name = company_name_element.text.split("\n")[0]
        if "O firmie" in company_name:
            company_name = company_name.replace("O firmie", "").strip()
        elif "About the company" in company_name:
            company_name = company_name.replace("About the company", "").strip()
    except:
        company_name = "N/A"

    requirements = []
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        requirements_list = soup.find("ul", class_="offer-viewEX0Eq-")
        if requirements_list:
            requirements_items = requirements_list.find_all("p", class_="offer-viewU0gxPf")
            for item in requirements_items:
                requirements.append(item.text)
    except:
        pass

    if not requirements:
        try:
            job_description_element = driver.find_element(By.XPATH, "//div[@data-scroll-id='job-description']")
            job_description = job_description_element.text
            requirements = extract_requirements(job_description)
        except:
            pass

    job_offer_data = {
        'Link': job_link_href,
        'Job Title': job_title,
        'Company Name': company_name,
        'Requirements': requirements
    }
    job_offers_list.append(job_offer_data)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

df = pd.DataFrame(job_offers_list)
df.to_excel('jobOffers.xlsx', index=False)

driver.quit()

def print_sorted_requirements():
    df = pd.read_excel('jobOffers.xlsx')
    requirements_list = df['Requirements'].tolist()
    all_requirements = [req for reqs in requirements_list for req in eval(reqs)]
    requirements_count = Counter(all_requirements)
    sorted_requirements = sorted(requirements_count.items(), key=lambda x: x[1], reverse=True)

    for requirement, count in sorted_requirements:
        print(f'[{requirement}][Amount = {count}]')

print_sorted_requirements()
