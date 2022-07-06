
from ctypes import alignment
from lib2to3.pgen2 import driver
from multiprocessing import connection
from sqlite3 import connect
import string
from unicodedata import name
import json
from flask import Flask,jsonify,request
import logging
from sqlalchemy import insert, create_engine, Column, String, Integer, MetaData, Table
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.sql import text
import requests
import pandas as pd
import os
import textwrap
import urllib
import pyodbc

# Import libraries
# Establish database connection
# Write API route with function name
# Start to fill API body with basic query string
# Take response back as JSON and return JSON variable

"""Below is the way to connect using pyodbc and use manual SQL queries."""

# driver_name = 'ODBC Driver 18 for SQL Server'
# server = 'test-database-server-intergen.database.windows.net'
# database_name = 'Test Data (Books and Authors)'
# username = 'azelikovsky@test-database-server-intergen.database.windows.net'
# password = '-Zelikovs1234'

# #Connection string for logging into database.
# connection_string_for_connection_variable = textwrap.dedent('''
#     Driver={driver};
#     Server={server};
#     Database={database};
#     Uid={username};
#     Pwd={password};
#     Encrypt=yes;
#     TrustServerCertificate=no;
#     Connection Timeout=30;
# '''.format(
#     driver=driver_name,
#     server=server,
#     database=database_name,
#     username=username,
#     password=password
# ))

# #Connection to the database using the connection string.
# connection_variable: pyodbc.Connection = pyodbc.connect(connection_string_for_connection_variable)

# #Creation of cursor object for querying.
# cursor_for_querying: pyodbc.Cursor = connection_variable.cursor()

# #Query of database.
# Manual_query_response = cursor_for_querying.execute("SELECT * FROM Books").fetchall()
# Data_from_query_as_a_dataframe = pd.read_sql("SELECT * FROM Authors", connection_variable)

# #Closing of connection.
# connection_variable.close()


"""Below is the way of connecting to the SQL database using SQL Alchemy."""

#Flask instantiation.
app = Flask(__name__)

#Creation of engine for SQL Alchemy.

drivers = [item for item in pyodbc.drivers()]
print(drivers)

driver_name = drivers[-1]
print(driver_name)

server = 'test-database-server-intergen.database.windows.net,1433'
database = 'Test Data (Books and Authors)'
username = 'azelikovsky' 
password = '-Zelikovs1234'
database_connection_string = f'mssql+pyodbc://{username}:{password}@{server}:{1433}/{database}?driver={driver_name}'

engine = create_engine(database_connection_string)
metadata = MetaData()

#Making an object equivalent of each table in the database for querying.
Authors_table = Table('Authors', metadata, autoload=True, autoload_with=engine)
Books_table = Table('Books', metadata, autoload=True, autoload_with=engine)
Join_table = Table('Join_Table', metadata, autoload=True, autoload_with=engine)
Publisher_table = Table('Publisher', metadata, autoload=True, autoload_with=engine)
Categories_table = Table('Categories', metadata, autoload=True, autoload_with=engine)

#Creation of global session variable.
Global_Scoped_Session = scoped_session(sessionmaker(bind=engine))

#API endpoint for all authors.

@app.route('/authors')
def get_all_authors():

    Local_Session = Global_Scoped_Session()
    
    data = Local_Session.query(Authors_table)
    
    Global_Scoped_Session.remove()

    results = []
    for row in data:
        results.append({'author_id':row.author_id,'first_name':row.first_name,'last_name':row.last_name,'count_books':row.count_books})
    
    JSON_result = json.dumps(results)

    return JSON_result

    Global_Scoped_Session.remove()

#API endpoint for all books.

@app.route('/books')
def get_all_books():
       
    Local_Session = Global_Scoped_Session()
    
    data = Local_Session.query(Books_table)
          
    results = []
    for row in data:
        results.append({'name':row.book_name,'publishing_year':row.publishing_year})

    JSON_result = json.dumps(results)

    return JSON_result

    Global_Scoped_Session.remove()

#API endpoint for books written by an author.
    
# @app.route('/books/<author_id>')
# def get_books_by_author(author_id):
    
#     Local_Session = Global_Scoped_Session()
    
#     join_table_data = Local_Session.query(Join_table).filter(Join_table.author_id == author_id)
    
#     books_by_author = []

#     for row_in_join_table in join_table_data:

#         data_about_book = Local_Session.query(Books_table,Publisher_table,Categories_table).join(Publisher_table).join(Categories_table).filter(Books_table.book_id == row_in_join_table.book_id).all()
    
#         for row_book_data in data_about_book:

#             books_by_author.append({'Name':row_book_data.Books.book_name,'Year Published':row_book_data.Books.publishing_year,'Publisher':row_book_data.Publisher.publisher_name,\
#                  'Publisher State':row_book_data.Publisher.state,\
#                      'Category':row_book_data.Categories.category_name,'Count of Books published in this Category':row_book_data.Categories.books_published_in_category_this_year})
        
#     JSON_result = json.dumps(books_by_author)

#     return JSON_result

#     Global_Scoped_Session.remove()


#Instantiation of the Flask server.

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)