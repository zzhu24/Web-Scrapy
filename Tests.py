from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from src import Scraping
from src import Queries
import logging
import time
import json
import ast
import re


def testScrapping():

    start_time = time.time()

    json_data = {}

    json_data['Movies'] = []
    json_data['Stars'] = []

    (films_one, actors_one) = Scraping.findAll("https://en.wikipedia.org/wiki/Maggie_Smith")
    Scraping.to_json(json_data, films_one, actors_one)


    with open('temp.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)




    print("--- %s seconds ---" % (time.time() - start_time))


def testMoiveName(movies):
    for movie in movies:
        print(movie["Movie Name"] + " : Url is ( " + movie["Moive URL"] + " )")


def testMovieYear(movies):
    for movie in movies:
        print(movie["Movie Name"] + " : Year produced is: " + str(movie["Movie Year"]))

def testMovieGross(movies):
    for movie in movies:
        print(movie["Movie Name"] + " : has gross of  " + str(movie["Movie Box Office"]) + " dollar")


def testMovieCasting(movies):
    for movie in movies:
        print(movie["Movie Name"] + " has casting of :")
        for i in movie["Movie Casting"]:
            print(i + ",")


def testActorName(actors):
    for actor in actors:
        print(actor["Actor Name"] + " : Url is ( " + actor["Actor URL"] + " )")


def testActorBirth(actors):
    for actor in actors:
        print(actor["Actor Name"] + " was born on: " + actor["Actor Birthday"])


def testActorGross(actors):
    for actor in actors:
        print(actor["Actor Name"] + " was total gross of  " + str(actor["Actor Total Gross"]) + " dollar")

def testActorFilmography(actors):
    for actor in actors:
        print(actor["Actor Name"] + " acted in: ")
        for i in actors["Actor Filmography"]:
            print(i + ",")


if __name__ == "__main__":
    json_data = open("data.json").read()
    data = json.loads(json_data)
    movies_data = data["Movies"]
    actors_data = data["Stars"]

    testMoiveName(movies_data)

    testMovieYear(movies_data)

    testMovieGross(movies_data)

    testMovieCasting(movies_data)

    testActorName(actors_data)

    testActorBirth(actors_data)

    testActorGross(actors_data)
