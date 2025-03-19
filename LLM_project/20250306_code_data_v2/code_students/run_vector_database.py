""" run_vector_database.py: Creates a vector database to store GDELT data and retrieves events by country.
This script also visualizes the clusters of events using t-SNE and PCA.

Copyright 2025, Cornell University

Cornell University asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including online repositories
such as Github.

Sharing solutions with current or future students of ENMGT5400 is
prohibited and subject to being investigated as a Code of Academic Integrity violation.

-----do not edit anything above this line---
"""

import os
import time

import chromadb

import helpers
from transform_data import read_gdelt
from vector_database import create_database, retrieve_events_by_country, get_collection


if __name__ == "__main__":

    # Initialize a persistent client
    os.makedirs(helpers.DATABASE_FOLDER, exist_ok=True)
    client = chromadb.PersistentClient(
        path=helpers.DATABASE_FOLDER,
    )

    #################################
    # Create a vector collection. This can be a bit slow...
    # depending on your hardware and patience.
    # If you have already created the collection, set create_database_from_files to False.
    #################################

    files = ["20250212.export.CSV", "20250213.export.CSV"]
    create_database_from_files = False  # You decide what is best

    if create_database_from_files:
        data_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
        )
        for file in files:
            df = read_gdelt(data_folder=data_folder, filename=file)
            documents = [
                f"Event: {x}. Impact location: {y}. Goldstein scale: {z}."
                for x, y, z in zip(df.Text, df.ActionGeo_FullName, df.GoldsteinScale)
            ]

            start_time = time.time()
            collection = create_database(
                client=client,
                collection_name=helpers.COLLECTION_NAME,
                doc_ids=df.index.tolist(),
                documents=documents,
            )
            print(
                f"{file}--Time taken to load data: {time.time() - start_time:.2f} seconds."
            )
    else:
        collection = get_collection(collection_name=helpers.COLLECTION_NAME)

    #################################
    #  TODO: Perform exploratory data analysis on the dataframes/collections
    #################################

    #################################
    #  TODO: Try querying the database for events in different countries
    #################################

    country_of_interest = "United States"
    n_results = 5

    documents, embeddings = retrieve_events_by_country(
        collection, country_of_interest, n_results
    )
    print(documents)

    #################################
    # TODO: Plot clusters using t-SNE
    # You probably need to import libraries in requirements.txt
    #################################

    pass

    #################################
    # TODO: Plot clusters using PCA
    # You probably need to import libraries in requirements.txt
    #################################

    pass
