import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://au.indeed.com/jobs?q=(node+or+react)&limit={LIMIT}&radius=50"


def extract_indeed_pages():
  result = requests.get(URL)

  # BeautifulSoup
  soup = BeautifulSoup(result.text, "html.parser")
  # Find pagination
  pagination = soup.find("div", {"class": "pagination"})
  links = pagination.find_all("a")
  pages = []
  # Get all these paginations except the last one.
  for link in links[0:-1]:
    # Get only strings(texts) inside of link
    pages.append(int(link.string))
    # Get only the last value which is 20
    max_pages = pages[-1]

  return max_pages


def extract_job(html):
  # Get information from <a title="">
  title = html.find("div", {"class": "title"}).a["title"]
  company = html.find("span", {"class": "company"})

  # Sometimes company is None
  if company == None:
    company_anchor = "Unknown Company"
  else:
    company_anchor = company.find("a")

  # Sometimes <span class="company"> does not have a link <a>
  if company_anchor == None: # there is no <a> tag
    company = str(company.string)
  elif company_anchor == "Unknown Company":
    company = company_anchor
  else: # there is a <a> tag
    company = str(company_anchor.string)

  # Remove spaces
  company = company.strip()

  return {"title": title, "company": company}


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    # print(result.status_code)
    soup = BeautifulSoup(result.text, "html.parser")
    jobs = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for job in jobs:
      if hasattr(job, 'find'):
        job = extract_job(job)
        jobs.append(job)

  return jobs