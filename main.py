import requests
from bs4 import BeautifulSoup

indeed_result = requests.get("https://au.indeed.com/jobs?as_and=node+react&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&salary=&radius=50&l=&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch")

# BeautifulSoup
indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")
# Find pagination
pagination = indeed_soup.find("div", {"class": "pagination"})
links = pagination.find_all("a")
pages = []
# Get all these paginations except the last one.
for link in links[0:-1]:
  # Get only strings(texts) inside of link 
  pages.append(int(link.string))
  
# Print only the last item
max_pages = pages[-1]

