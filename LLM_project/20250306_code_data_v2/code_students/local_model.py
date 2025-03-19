""" local_model.py: Contains functions for run_local_model.py.

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

import ollama


def select_short(country: str) -> str:
    """A dummy function to short assets of a country."""
    return f"Short {country}"


def select_long(country: str) -> str:
    """A dummy function to long assets of a country"""
    return f"Long {country}"


def generate_response(prompt: str) -> str:
    """Return response from the model. The response is a string that answers the prompt.

    Args:
        prompt (str): The prompt to send to the model.

    Returns:
        str: The summary of the events.

    """

    model = "llama3.2"
    event_summary = ""

    ##############################################################################
    # TODO: Implement your code here
    ##############################################################################

    pass

    ##############################################################################

    return event_summary


def recommend_trade(country_of_interest: str, event_summary: str) -> str:
    """Return outputs from mode's selected function. The model selects a function
    to short or long a country based on a given summary of events in a country.

    In other words, when given country_of_interest and event_summary,
    the model should call one of the provided functions:
    - select_short
    - select_long

    Args:
        country_of_interest (str): The country of interest.
        event_summary (str): The summary of events in the country.

    Returns:
        str: The output from the model's selected function.
    """

    function_output = ""

    ##############################################################################
    # TODO: Implement your code here
    # Note: Use the temperature of zero for deterministic outputs
    ##############################################################################

    pass

    ##############################################################################

    return function_output
