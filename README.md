# Job Offer Scraping tool

### Note:
To modify the code in order to make it use a different URL (not tried yet), please modify the `driver.get("your url")` parameter. I suggest pasting the URL with already chosen requirements, such as Job Title, Localisation etc.

## Written in Python 3.10 using Selenium, Pandas and Spacy

This code is designed to scrape job offers from the website [pracuj.pl](https://www.pracuj.pl/) related to Python programming in Warsaw. It utilizes the Selenium WebDriver along with the Chrome browser to navigate the website and extract job details. Here's an overview of the code:

- The code begins by importing necessary modules: `os`, `webdriver` from Selenium, `BeautifulSoup` from bs4, `pandas`, `spacy`, and `Counter` from collections.

- The project directory path is obtained using `os.path.dirname()` and `os.path.abspath(__file__)`. This allows the code to locate the `chromedriver.exe` file within the project directory dynamically.

- Chrome options are set using `Options()` from the `selenium.webdriver.chrome.options` module. Two options, `--no-sandbox` and `--disable-dev-shm-usage`, are added to ensure a smooth execution.

- The Selenium WebDriver is set up using `Service()` and `webdriver.Chrome()`, passing the `chrome_driver_path` and `chrome_options`.

- The WebDriver navigates to the target URL "[pracuj.pl](https://www.pracuj.pl/praca/programista%20python;kw/warszawa;wp?rd=30&et=1%2C17)" and accepts the cookie consent by finding the corresponding button element using XPath.

- The code loads spaCy models for English and Polish language processing using `spacy.load()`.

- The `extract_requirements()` function takes a text parameter, uses spaCy to extract nouns and proper nouns, and returns a list of requirements.

- A list `job_offers_list` is created to store the scraped job offer data.

- The code finds all job offers on the page by locating elements using XPath.

- For each job offer, a new tab is opened using `driver.execute_script("window.open('');")` and switched to using `driver.switch_to.window()`.

- The offer's link is accessed, and the code tries to extract the job title and company name from the page. If the strings "O firmie" or "About the company" are present in the titles, they are removed.

- The code attempts to scrape the job requirements from the offer page. It uses `BeautifulSoup` to parse the HTML and find the requirements list. If found, it iterates over the requirements and appends them to the `requirements` list.

- If no requirements are found using the previous method, the code tries to extract them from the job description by calling the `extract_requirements()` function.

- The job offer data, including the link, job title, company name, and requirements, is stored in a dictionary and appended to the `job_offers_list`.

- After scraping all job offers, the current tab is closed, and the driver is switched back to the main window.

- The collected job offer data is converted into a pandas DataFrame and saved as an Excel file named "jobOffers.xlsx" using `df.to_excel()`.

- Finally, the driver is quit to ensure the browser window is closed.

- The `print_sorted_requirements()` function reads the Excel file, extracts the requirements column, combines them into a single list, counts the occurrences of each requirement using `Counter`, and prints the sorted requirements along with their counts.

**Note:** Make sure to update the URL and adjust the code if needed to match the target website structure or specific requirements.
