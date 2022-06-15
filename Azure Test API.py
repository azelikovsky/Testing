
from itertools import count
import json
from ntpath import join
from pickle import FALSE, TRUE
from this import s
from flask import Flask,jsonify,request
import logging
from sqlalchemy import insert, create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.sql import text
import requests
import os

app = Flask(__name__)


@app.route('/')
def sample():
    return "Hello"

app.run(port=5000)
