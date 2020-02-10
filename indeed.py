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