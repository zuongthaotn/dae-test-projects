import pandas as pd
from pathlib import Path
from pymongo import MongoClient


def tranform_data():
    project_folder = Path(__file__).parent.parent
    csv_file = str(project_folder) + "/datasets/imdb_upcoming_movies.csv"
    df = pd.read_csv(csv_file, header=None)
    df.columns = ["ID", "Name", "Year", "Duration", "Interests", "Description", "Directors", "Writers", "Stars"]
    df = df.dropna()
    df = df.drop_duplicates()
    transformed_csv_file = str(project_folder) + "/datasets/imdb_upcoming_movies_transformed.csv"
    df.to_csv(transformed_csv_file, index=False)


def load_data():
    """ Load transformed data from csv then insert into MongoDB """
    project_folder = Path(__file__).parent.parent
    csv_file = str(project_folder) + "/datasets/imdb_upcoming_movies_transformed.csv"
    df = pd.read_csv(csv_file)
    #
    client = MongoClient("mongodb://localhost:27017/")
    db = client["movies_recommendation_system"]
    collection = db["upcoming_movies"]
    collection.delete_many({})
    #
    for i, row in df.iterrows():
        data = {
            "ID": row["ID"],
            "Name": row["Name"],
            "Year": row["Year"],
            "Duration": row["Duration"],
            "Interests": row["Interests"],
            "Description": row["Description"],
            "Directors": row["Directors"],
            "Writers": row["Writers"],
            "Stars": row["Stars"]
        }
        collection.insert_one(data)
