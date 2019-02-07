from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from src import *
import logging
import time
import json
import ast
import re
import flask
from flask import Flask, request, jsonify
import api
import os
import requests
import plotly
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import Image
import IPython
import plotly
import os
import numpy as np
import numpy

def find_actor_hub(movies_data, actors_data):
    hubs = np.zeros(len(actors_data))
    for index in range(len(hubs)):
        for movies in actors_data[index]["Actor Filmography"]:
            for all_movies in movies_data:
                if movies == all_movies["Movie Name"]:
                    hubs[index] += len(all_movies["Movie Casting"])
    y = np.array(hubs)
    names = []
    for actors in actors_data:
        names.append(actors["Actor Name"])
    x = np.array(names)

    print(len(x))
    print(len(y))

    plt.xticks(range(len(y)), x,rotation='vertical')

    plt.plot(y)


    plt.show()

def calculateAgeGroupMaxGross(actors_data):
    gross = np.zeros(7)
    age_group = ["20s", "30s", "40s", "50s", "60s", "70s", "80s"]

    for actor in actors_data:
        if "1988-10-16" < actor["Actor Birthday"]:
            gross[0] += actor["Actor Total Gross"]
        elif "1978-10-16" < actor["Actor Birthday"] < "1988-10-16":
            gross[1] += actor["Actor Total Gross"]
        elif "1968-10-16" < actor["Actor Birthday"] < "1978-10-16":
            gross[2] += actor["Actor Total Gross"]
        elif "1958-10-16" < actor["Actor Birthday"] < "1968-10-16":
            gross[3] += actor["Actor Total Gross"]
        elif "1948-10-16" < actor["Actor Birthday"] < "1958-10-16":
            gross[4] += actor["Actor Total Gross"]
        elif "1938-10-16" < actor["Actor Birthday"] < "1948-10-16":
            gross[5] += actor["Actor Total Gross"]
        else:
            gross[6] += actor["Actor Total Gross"]

    y = np.array(gross)
    x = np.array(age_group)

    plt.xticks(range(len(y)), x,rotation='vertical')

    plt.plot(y)


    plt.show()




if __name__ == "__main__":
    json_data = open("temp_data.json").read()
    data = json.loads(json_data)
    movies_data = data["Movies"]
    actors_data = data["Stars"]

    #find_actor_hub(movies_data, actors_data)

    calculateAgeGroupMaxGross(actors_data)