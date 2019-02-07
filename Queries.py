from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from src import *
import logging
import time
import json
import ast
import re

def starover( c ):
    choice = input("Do you want to know more information？ (y/n): \n")
    if choice == 'n':
        exit(0)

def certainMovieGrooss( movies ):
    print("Here is a list of move you can check for gross !~")
    for item in movies:
        print(item["Movie Name"])
    name = input("Please enter the name of movie:\n")
    temp_item = next(item for item in movies if item["Movie Name"] == name)
    if temp_item:
        print("\n\n"+"Gross of " + name + " is " + str(temp_item["Movie Box Office"]))
    print("\n\n")


def certainMovieCasting( movies ):
    print("Here is a list of move you can check for gross !~")
    for item in movies:
        print(item["Movie Name"])
    name = input("Please enter the name of movie:\n")
    temp_item = next(item for item in movies if item["Movie Name"] == name)
    if temp_item:
        print("\n\n")
        print("Casting of " + name + " is:")
        for actors in temp_item["Movie Casting"]:
            print(actors)
    print("\n\n")




def certainActorFilmography( actors ):
    print("Here is a list of move you can check for gross !~")
    for item in actors:
        print(item["Actor Name"])
    name = input("Please enter the name of the actor:\n")
    temp_item = next(item for item in actors if item["Actor Name"] == name)
    if temp_item:
        print("\n\n")
        print("Filmography of " + name + " is:")
        for films in temp_item["Actor Filmography"]:
            print(films)
    print("\n\n")



def getMostGross(actors):
    top = input("How many top actor do you want to see?:\n")
    sort_actor  = sorted(actors, key=itemgetter("Actor Total Gross"), reverse=True)
    print("\n\n")
    for i in range(int(top)):
        print(sort_actor[i]["Actor Name"] + " has total grouss of: " + str(sort_actor[i]["Actor Total Gross"]) + " dollars !!")
    print("\n\n")


def getOldestActor(actors):
    top = input("How many oldest actor do you want to see?:\n")
    sort_actor  = sorted(actors, key=itemgetter("Actor Birthday"), reverse=False)
    print("\n\n")
    for i in range(int(top)):
        if sort_actor[i]["Actor Birthday"] == "":
            i -= i
            continue
        print(sort_actor[i]["Actor Name"] + " was born in: " + sort_actor[i]["Actor Birthday"] + " ~ ~")
    print("\n\n")

def moviesInAYear(movies):
    year = input("Which year of movies do you want to know?:\n")
    year = int(year)
    print("\n\n")
    for movie in movies:
        if movie["Movie Year"] == year:
            print(movie["Movie Name"])
    print("\n\n")

def actorBornInAYear(actors):
    year = input("Which year of actor do you wan to know?:\n")
    print("\n\n")
    for actor in actors:
        if year in actor["Actor Birthday"]:
            print(actor["Actor Name"] + " was born in: " + actor["Actor Birthday"] + " !~")
    print("\n\n")


if __name__ == "__main__":
    json_data = open("data.json").read()
    data = json.loads(json_data)
    movies_data = data["Movies"]
    actors_data = data["Stars"]

    c = 0

    while (c != 8):
        print()
        c = int(input("Which one do you want to know about:\n"
                        "1 = How much a movie has grossed\n"
                        "2 = List all casting actors in a certain movie\n"
                        "3 = List which movies an actor has worked in\n"
                        "4 = List the top X actors with the most total grossing value\n"
                        "5 = List the oldest X actors\n"
                        "6 = List all the movies for a given year\n"
                        "7 = List all the actors for a given year\n"
                        "8 = EXIST\n\n"
                      ))

        if c == 1:
            certainMovieGrooss(data["Movies"])
            starover(c)

        if c == 2:
            certainMovieCasting(data["Movies"])
            starover(c)

        if c == 3:
            certainActorFilmography(data["Stars"])
            starover(c)

        if c == 4:
            getMostGross(data["Stars"])
            starover(c)


        if c == 5:
            getOldestActor(data["Stars"])
            starover(c)

        if c == 6:
            moviesInAYear(data["Movies"])
            starover(c)

        if c == 7:
            actorBornInAYear(data["Stars"])
            starover(c)
