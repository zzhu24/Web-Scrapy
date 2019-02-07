from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from src import *
import logging
import time
import json
import ast
import re





def getMovieBox(quote_page):
    try:
        page = urlopen(quote_page)
    except:
        return ""

    page = urlopen(quote_page)
    soup = BeautifulSoup(page, "lxml")

    table = soup.find('table', {'class': 'infobox vevent'})


    if(table == None):
        logging.warning("Cannot Find Cast Information")
        return ""


    for tr in table.find_all('tr'):
        if tr is not None:
            text = tr.text
            if 'Box office' in text:
                td = tr.find("td")
                if td is not None:
                    box_text = td.text
                    if "$" in box_text:
                        box_text = box_text[box_text.index("$"): -3]
                        if "\xa0" in box_text:
                            box_office = box_text.replace("\xa0", " ")
                        else:
                            box_office = box_text
                        return box_office

    return ""

def getActorBirth(quote_page):
    try:
        page = urlopen(quote_page)
    except:
        return ""

    soup = BeautifulSoup(page, "lxml")

    birthDay = ""
    born = soup.find("span", {"class": "bday"})
    if born is not None:
        birthDay = born.text


    return birthDay



def getFilmFromActor(quote_page):
    try:
        page = urlopen(quote_page)
    except:
        return ""

    soup = BeautifulSoup(page, "lxml")

    table = soup.find("table", {"class" : "wikitable sortable"})

    if table is None:
        logging.warning("Cannot Find Filmography Information")
        return None



    table_body = table.find("tbody")
    table = table_body.findAll("tr")

    movies = []
    last = ""
    for tr in table:
        all_td = tr.find("td")
        if all_td is not None:
            if "2018" >= all_td.text >= "1800":
                year = all_td.text
            else:
                year = last
            last = year
            all_a = all_td.find("a")
            if all_a is None:
                all_td = all_td.find_next_sibling()
                all_a = all_td.find("a", href = True, title = True)
            if(all_a):
                temp_url = "https://en.wikipedia.org"+all_a["href"]
                box_office = getMovieBox(temp_url)
                movies.append(("https://en.wikipedia.org"+all_a["href"], all_a["title"], year.replace('\n',""), box_office))

    return movies




def findCastFromFilm(quote_page):
    try:
        page = urlopen(quote_page)
    except:
        return ""

    soup = BeautifulSoup(page, "lxml")

    table = soup.find('table', {'class': 'infobox vevent'})
    if(table == None):
        logging.warning("Cannot Find Cast Information")
        return None

    actor = []

    for tr in table.find_all('tr'):
        text = tr.text
        if 'Starring' in text:
            rows =  tr.find_all('a', href=True)
            for i in rows:
                birth = getActorBirth("https://en.wikipedia.org" + i['href'])
                actor.append(("https://en.wikipedia.org" + i['href'], i.text, birth))

    return actor






def findAll(quote_page):
    one_film = getFilmFromActor(quote_page)


    one_coop = []
    actor_number = 0
    for film in one_film:
        (film_url, film_name, film_year, film_box_office) = film
        #(film_url, film_name, film_year) = film
        temp_cast = findCastFromFilm(film_url)
        if temp_cast is not None:
            actor_number += len(temp_cast)
            one_coop.append(temp_cast)

    film_number = len(one_coop)

    print("Film Number")
    print(film_number)


    print("Actor Number")
    print(actor_number)


    return (one_film, one_coop)







def to_json(json_data, movie, actor_list):


    for i in range(len(movie)):

        (movie_url, movie_name, movie_year, movie_gross) = movie[i]

        if any(d["Movie Name"] == movie_name for d in json_data['Movies']):
            continue


        j_movie = {}
        (movie_url, movie_name, movie_year, movie_gross) = movie[i]
        #(movie_url, movie_name, movie_year) = movie
        j_movie['Movie Name'] = movie_name
        j_movie['Moive URL'] = movie_url
        j_movie['Movie Year'] = int(movie_year)


        gross = 0
        movie_gross = movie_gross.replace(",", "")
        if movie_gross == "":
            gross = 0
        elif "mill" in movie_gross:
            gross = int(re.findall('\d+', movie_gross)[0]) * 1000000
        elif "bill" in movie_gross:
            gross = int(re.findall('\d+', movie_gross)[0]) * 1000000000
        else:
            gross = int(re.findall('\d+', movie_gross)[0])
        j_movie['Movie Box Office'] = gross

        starring = []


        for actor in actor_list[i]:
            (actor_url, actor_name, actor_birth) = actor
            starring.append(actor_name)

            if not any(d["Actor Name"] == actor_name for d in json_data['Stars']):
                j_actor = {}
                j_actor["Actor Name"] =actor_name
                j_actor["Actor URL"] = actor_url
                j_actor["Actor Birthday"] = actor_birth
                j_actor["Actor Total Gross"] = gross
                filmography = []
                filmography.append(movie_name)
                j_actor["Actor Filmography"] = []
                j_actor["Actor Filmography"].append(movie_name)

                actor_json = ast.literal_eval(json.dumps(j_actor))
                json_data['Stars'].append(actor_json)
            else:
                temp_item = next(item for item in json_data['Stars'] if item["Actor Name"] == actor_name)
                if not any(movie_name in s for s in temp_item["Actor Filmography"]):
                    temp_item["Actor Filmography"].append(movie_name)
                    temp_item["Actor Total Gross"] +=  gross

        j_movie['Movie Casting'] = starring




        movie_json = ast.literal_eval(json.dumps(j_movie))
        json_data['Movies'].append(movie_json)









if __name__ == "__main__":


    start_time = time.time()
    #(films_one, actors_one) = findAll("https://en.wikipedia.org/wiki/Tom_Holland_(actor)")

    json_data = {}

    json_data['Movies'] = []
    json_data['Stars'] = []



    #(films_one, actors_one) = findAll("https://en.wikipedia.org/wiki/Maggie_Smith")
    #to_json(json_data, films_one, actors_one)

    #(films_two, actors_two) = findAll("https://en.wikipedia.org/wiki/Chris_Evans_(actor)")
    #to_json(json_data, films_two, actors_two)

    (films_three, actors_three) = findAll("https://en.wikipedia.org/wiki/Tom_Holland_(actor)")
    to_json(json_data, films_three, actors_three)


    with open('temp_data.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)




    print("--- %s seconds ---" % (time.time() - start_time))


