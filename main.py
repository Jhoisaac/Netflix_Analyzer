from bs4 import BeautifulSoup
import requests
import pprint
import json
import time
pp = pprint.PrettyPrinter(indent=4)


def get_specific_info(url: str = "https://www.netflix.com/in/title/80179292"):
    """
        This function returns specific inforamtion for a movie, series or other show.
        You want to know, how many episodes a series have? What the descriptions are? How long a episode lasts?
        All kind of data will be returned, which ist available under the specific Netflix url.

        :param url (str): The url, which should get parsed. Standard url is the series S.W.A.T for developing purposes.
        :return (list): A list of all series, which could get found under the url.

        An example of the data:
        <li class = "episode" data-uia = "episode" > <figure class = "episode-thumbnail" data-uia = "episode-thumbnail" >
        <span class = "episode-thumbnail-gradient" >
        </span > <img alt = "Watch Vendetta. Episode 20 of Season 1." class = "episode-thumbnail-image" data-uia = "episode-thumbnail-image" loading = "lazy"
        src = "https://occ-0-2774-4415.1.nflxso.net/dnm/api/v6/9pS1daC2n6UGc3dUogvWIPMR_OU/AAAABZa21SaxmN_yVLUq9aMHcgRg5OqsprSZa8g3L2gxqX79J7RL3ztznO1QZ4fajUvZj5uxZNsO4Ysk7Mn5fq_OlSKkOwxcgSxO8zz61voENZnNGmC9ynM0gpuD.jpg?r=1fa"/>
        </figure > <div class = "episode-metadata" > <h3 class = "episode-title" data-uia = "episode-title" > 20. Vendetta < /h3 >
        <span class = "episode-runtime" data-uia = "episode-runtime" > 43m < /span > </div > <p class = "epsiode-synopsis" data-uia = "episode-synopsis" > </p > </li >,
    """

    _resp = requests.get(url)
    # print(_resp.status_code)  # If 200: successfully scraped the target page
    _soup = BeautifulSoup(_resp.text, 'html.parser')

    o = {}
    o["name"] = _soup.find("h1", {"class": "title-title"}).text
    o["seasons"] = _soup.find("span", {"class": "duration"}).text
    # o["about"] = _soup.find("div", {"class": "hook-text"}).text

    e = {}
    l = list()
    episodes = _soup.find("ol", {"class": "episodes-container"}).find_all("li")

    # pp.pprint(episodes)
    e["episode-Number"] = len(episodes)
    for i in range(len(episodes)):
        e["episode-title"] = episodes[i].find(name="h3",
                                              attrs={"class": "episode-title"}).text
        e["episode-description"] = episodes[i].find(
            "p", {"class": "epsiode-synopsis"}).text

        e["pic_link"] = episodes[i].find("img alt")
        l.append(e)
        # e = {}
    pp.pprint(e["episode-description"])


def get_list_of_series(series_url: str = "https://www.netflix.com/browse/genre/83") -> list:
    """
        This function returns a list of all series, which are available under a specific Netflix url.

        :param series_url (str): The url, which should get parsed. Standard url is the series section at Netflix.
        :return (list): A list of all series, which could get found under the url.

        An example of the data:
        <a class = "nm-collections-title nm-collections-link" data-uia = "collections-title" href = "https://www.netflix.com/de-en/title/80236236" >
        <img alt = "" class = "nm-collections-title-img" data-title-id = "80236236" src = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="/>
        < span class = "nm-collections-title-img placeholder" > </span > <span class = "nm-collections-title-name" > Another Life < /span > </a >,
    """

    series_resp = requests.get(series_url)
    series_soup = BeautifulSoup(series_resp.text, 'html.parser')

    series = []
    start = len("<span class=\"nm-collections-title-name\">")  # always int(34)

    for serie in series_soup.find_all("span", class_="nm-collections-title-name"):
        # print(serie)  # <span class="nm-collections-title-name">Wednesday</span>

        # the end index variates with the length of the title name -> needs to be calculated for each title on the fly
        end = int(str(serie).find("</span><a")) - len("</span>") + 1
        title = str(serie)[start:end]
        if title:
            series.append(title)

    # pp.pprint(len(series))  # List Content varates with the country, where I am

    return series  # 640


def get_list_of_movies(movie_url: str = "https://www.netflix.com/browse/genre/34399") -> list:
    """
        This function returns a list of all movies, which are available under a specific Netflix url.

        :param movie_url (str): The url, which should get parsed. Standard url is the movie section at Netflix.
        :return (list): A list of all movies, which could get found under the url.

        An example of the data:
        <a class = "nm-collections-title nm-collections-link" data-uia = "collections-title" href = "https://www.netflix.com/de-en/title/81346063" >
        <img alt = "" class = "nm-collections-title-img" data-title-id = "81346063" src = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="/>
        < span class = "nm-collections-title-img placeholder" > </span > <span class = "nm-collections-title-name" > Love Tactics < /span > </a >,
    """

    movie_resp = requests.get(movie_url)
    # movie_resp.json() # doesn't work with this Netflix url

    movie_soup = BeautifulSoup(movie_resp.text, 'html.parser')

    movies = []
    start = len("<span class=\"nm-collections-title-name\">")  # always int(34)

    for movie in movie_soup.find_all("span", class_="nm-collections-title-name"):
        # print(movie) # <span class="nm-collections-title-name">Troll</span>

        # the end index variates with the length of the title name -> needs to be calculated for each title on the fly
        end = int(str(movie).find("</span><a")) - len("</span>") + 1
        title = str(movie)[start:end]
        if title:
            movies.append(title)

    pp.pprint((movies))  # List Content varates with the country, where I am

    return movies  # 640


if __name__ == "__main__":
    get_specific_info()
    get_list_of_series()
    get_list_of_movies()


"""
    First trys. Maybe it will be helpful in the future.

# data = str(soup.find_all("a"))
# data_in_list: list = []
# index_of_start: list = []
# index_of_end: list = []
# for i, _char in enumerate(data):
#     # search for "<a", the start of the line
#     if _char == "<" and (data[i+1] == "a"):
#         index_of_start.append(i)
#         # indexes.append(i)
#         # start = i
#         # line += _char  # fill the line string
#     if _char == "a" and (data[i+1] == ">"):
#         index_of_end.append(i+1)
#         # indexes.append(i+1)
#         # end = i
#         # print(line)
#         # data_in_list.append(line)
#         # line: str = ""
# if len(index_of_start) == len(index_of_end):
#     for index in range(len(index_of_start)):
#         start, end = index_of_start[index], index_of_end[index]
#         data_in_list.append(data[start:end])
# # pp.pprint(len(data_in_list))
# # print(data.count("class=\"nm-collections-title-name\""))
# # print(data_in_list[10])
# # print(data_in_list[15].find("class=\"nm-collections-title-name\""))
# titles = []
# for i in range(len(data_in_list)):
#     start = int(data_in_list[i].find(
#         "class=\"nm-collections-title-name\">")) + len("class=\"nm-collections-title-name\">")
#     end = data_in_list[i].find("</span><a") - len("</span><a")
#     title = data_in_list[i][start:end]
#     if title:
#         titles.append(title)
# pp.pprint(titles)
"""
