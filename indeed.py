import requests
from bs4 import BeautifulSoup

LANGS = ["react", "react native"]
LIMIT = 50
URL = f"https://au.indeed.com/jobs?q=(node+or+react)&limit={LIMIT}&radius=50"


def get_last_page():
    result = requests.get(URL)

    # BeautifulSoup
    soup = BeautifulSoup(result.text, "html.parser")
    # Find pagination
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []
    # Get all these paginations except the last one (next>>).
    for link in links[0:-1]:
        # Get only strings(texts) inside of link
        pages.append(int(link.string))
        # Get only the last value which is 20
        last_page = pages[-1]

    return last_page


def extract_job(html):
    # Get information from <a title="">
    title = html.find("div", {"class": "title"}).a["title"]
    company = html.find("span", {"class": "company"})

    # Sometimes company can be None
    if company == None:
        company = "Unknown Company"
    else:
        company_anchor = company.find("a")
        # Sometimes <span class="company"> does not have a link <a>
        if company_anchor == None:
            company = str(company.string)
        else:
            company = str(company_anchor.string)

    # Remove spaces
    company = company.strip()

    # <div class=location> can be hidden
    # so we need to get the data from another tag.
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://au.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        # print(result.status_code)
        soup = BeautifulSoup(result.text, "html.parser")
        extracted_info = soup.find_all("div",
                                       {"class": "jobsearch-SerpJobCard"})
        for info in extracted_info:
            # Fix an error - 'dict' object has no attribute 'find' by adding hasattr(job, 'find')
            if info != None:
                job = extract_job(info)
                jobs.append(job)
            continue

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
