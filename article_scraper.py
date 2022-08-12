import os
import string
import re
import requests
import bs4 as bs4

"""Scrape the articles from nature website"""

base_url: str = "https://www.nature.com"


def name_refactor(name: str) -> str:
    """
    Refactors the name of the article to form a valid file name.
    Space is replaced with underscore and all punctuation characters are removed
    :param name: Base name of article
    :return: Article name with valid file name
    """
    name = name.strip()
    for punc in string.punctuation:
        name = name.replace(punc, '')
    name = re.sub(r'\s', '_', name)
    return f'{name}.txt'


def folder_create(number_of_pages_end: int, number_of_pages_start: int) -> None:
    for page_id in range(number_of_pages_start, number_of_pages_end + 1):
        os.mkdir(f"Page_{page_id}")


def article_finder(number_of_pages_end: int, number_of_pages_start: int = 1) -> list[dict[str, int | bs4.element.Tag]]:
    """
    Finds all articles on the given number of pages
    :param number_of_pages_start: Start page of the search
    :param number_of_pages_end: End page of the search
    :return: List of a dictionary with article and page number on the given interval
    """
    articles: list[dict] = []
    for page_id in range(number_of_pages_start, number_of_pages_end + 1):
        url: str = f"{base_url}/nature/articles?sort=PubDate&year=2020&page={page_id}"
        page: requests.models.Response = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        articles += [{"page": page_id, "content": article} for article in soup.find_all("article")]
    folder_create(number_of_pages_end, number_of_pages_start)
    return articles


def article_saver(articles: list[dict[str, int | bs4.element.Tag]], gender: str) -> list[str]:
    """
    Saves all articles to the given list
    :param articles:
    :param gender:
    :return:
    """
    articles_saved: list[str] = []
    for article in articles:
        article_gender: str = article["content"].find("span", {'data-test': 'article.type'}).span.text
        if article_gender == gender:
            article_url: str = f'{base_url}{article["content"].a.get("href")}'
            article_page: requests.models.Response = requests.get(article_url)
            soup_article = bs4.BeautifulSoup(article_page.text, "html.parser")
            article_file_name = name_refactor(soup_article.find('h1', {'class': 'c-article-magazine-title'}).text)
            article_folder = f"Page_{article['page']}"

            with open(f"{article_folder}/{article_file_name}", "wb") as f:
                f.write(soup_article.find("div", {'class': 'c-article-body'}).text.strip().encode())
            articles_saved += [article_file_name]
    return articles_saved


if __name__ == '__main__':
    number_of_pages: int = int(input())
    article_gender: str = input()
    articles: list[dict[str, int | bs4.element.Tag]] = article_finder(number_of_pages)
    print(article_saver(articles, article_gender))
    print("Saved all articles.")
