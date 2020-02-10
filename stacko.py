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
    return last_page



def get_jobs():
    last_page = get_last_page()
    return []
