# Job Offer Scraping tool + MongoDB integration

Manually job hunting on websites may sometimes be boring. Data scraping comes with help.


I wrote this code because I'm having a tough time landing a job myself. Fingers crossed, this will make things a bit easier down the road.

![scraper](https://github.com/gluchy1/joboffer-scraping-tool/assets/70800019/f0d990bf-899c-4c87-9af2-442c52d627e7)

### Note:
To modify the code in order to make it use a different URL just edit config.env, but it is strongly adapted for pracuj.pl site. I suggest pasting the URL with already chosen requirements, such as Job Title, Localisation etc. -> not to over deliver useless data

## Written in Python 3.10 using Selenium, Pandas and Spacy

This is a Python script that automates the task of collecting job offers from a specific website (in this case [pracuj.pl](https://www.pracuj.pl/)). It not only grabs basic details like job titles and company names but also extracts job requirements. All collected information is stored in a MongoDB database.

Get the newest [chromedriver](https://sites.google.com/chromium.org/driver/downloads/) in order to run the chrome webdriver, it is being updated often and the one provided with this repo could be outdated.

After running for a while, it sorts and prints all the reuqirements found, from the most common to the rarest:


![image](https://github.com/gluchy1/joboffer-scraping-tool/assets/70800019/331cf67e-a110-432d-bbae-b16c38d88225)


Stores the data in MongoDB:


![image](https://github.com/gluchy1/joboffer-scraping-tool/assets/70800019/61aa1948-163b-4133-9a62-f4bf9d737b8f)


## **Libraries Used:**  

- **Selenium:** Clicks around the web page for us.
- **BeautifulSoup:** Reads the web page's code to pick out the details we want.
- **spaCy:** Looks through the job description to find important keywords.
- **MongoDB:** This is where we keep all the job data we collect.

- 

**Note:** Make sure to update the URL and adjust the code if needed to match the target website structure or specific requirements.
