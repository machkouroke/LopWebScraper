import bs4 as bs4
import requests


def movie_scraper(url: str):
    """
    Scrapes the movie data from the given URL (IMDB)
    :param url:
    :return:
    """

    if 'title' not in url:
        print("Invalid movie page!")
    else:
        answer = requests.get(url)
        if answer.status_code != 200:
            print("Invalid movie page!")
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(answer.text, "html.parser")
        movies_data: dict[str] = {"title": soup.h1.text,
                                  "description": soup.find("span", {'data-testid': 'plot-l'}).text}
        print(movies_data)
