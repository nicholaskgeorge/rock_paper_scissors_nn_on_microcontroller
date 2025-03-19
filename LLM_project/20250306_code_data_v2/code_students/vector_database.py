""" vector_database.py: Contains functions for run_vector_database.py.

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

import chromadb
import chromadb.utils.embedding_functions as ef
import numpy as np


import helpers


def create_database(
    client: chromadb.PersistentClient,
    collection_name: str,
    doc_ids: list[int],
    documents: list[str],
) -> chromadb.Collection:
    """Create a persistent vector database in a local folder, then create and populate a collection with documents.

    Args:
        client (chromadb.PersistentClient): The persistent client object.
        collection_name (str): The name of the collection.
        doc_ids (list[int]): The list of document ids.
        documents (list[str]): The list of documents.

    Returns:
        chromadb.Collection: The collection object.

    """

    collection = None
    embedding_function = ef.DefaultEmbeddingFunction()

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################

    pass

    ##############################################################################

    return collection


def get_collection(collection_name: str) -> chromadb.Collection:
    """Get a collection from a persistent vector database.

    Args:
        collection_name (str): The name of the collection.

    Returns:
        chromadb.Collection: The collection object.

    """
    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################
    pass
    ##############################################################################


def retrieve_events_by_country(
    collection: chromadb.Collection, country_of_interest: str, n_results: int
) -> tuple[list[str], np.array]:
    """Search for events that happened in a specific country.

    Args:
        collection (chromadb.Collection): The collection object.
        query_texts (list[str]): The list of query texts.
        n_results (int): The number of results to return.

    Returns:
        list[str]: The list of documents.
        np.array: The embeddings of the documents (n_results x embedding_size).

    """
    documents = []
    embeddings = np.array([])

    # The query text
    query = f"Happened at {country_of_interest}"

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################

    pass

    ##############################################################################

    return documents, embeddings
