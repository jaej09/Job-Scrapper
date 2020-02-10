import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/jobs?tl=react+reactjs+react-native&sort=i"


def get_last_page():
    result = requests.get(URL)

    # BeautifulSoup
    soup = BeautifulSoup(result.text, "html.parser")
    # Find pagination
    pagination = soup.find("div", {"class": "s-pagination"})
    pagination_links = pagination.find_all("a")
    # Just want the last one
    # NEXT 버튼 제외하면 last one 은 뒤에서 두번째에 위치함
    last_page = pagination_links[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.h2.a["title"]
    # recursive=False -> h3 의 direct child <span> 만 가져오겠다고 명시
    # variable 을 멀티로 주면 company = [0], location = [1] 들어감
    company, location = html.h3.find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("\r")

    job_id = html["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Stacko: Page: {page+1}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        extracted_info = soup.find_all("div", {"class": "-job"})
        for info in extracted_info:
            if info != None:
                job = extract_job(info)
                jobs.append(job)
            continue

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
