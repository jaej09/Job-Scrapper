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


def extract_indeed_jobs(last_page):
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")
    # print(result.status_code)
    soup = BeautifulSoup(result.text, "html.parser")
    jobs = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for job in jobs:
      # Get information from <a title="">
      title = job.find("div", {"class": "title"}).find("a")["title"]
      company = job.find("span", {"class": "company"})
      # Sometimes company does not have a link
      company_anchor = company.find("a")
      if company_anchor is not None:
        company = str(company_anchor.string)
      else:
        company = str(company.string)
      # Remove spaces
      company = company.strip()
      print(title, company)
  return jobs
