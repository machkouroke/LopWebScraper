import requests


def html_saver(url):
    """
    Saves the HTML of the given URL
    """
    answer = requests.get(url)
    if answer.status_code != 200:
        print(f"The URL returned {answer.status_code}!")
    else:
        with open("../Web Scraper/Web Scraper/task/source.html", "wb") as f:
            f.write(answer.content)
            print("Content saved!")
