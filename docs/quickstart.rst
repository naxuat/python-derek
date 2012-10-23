===========
Quick Start
===========

For the impatient, simple usage of the official Python binding for Derek looks
like::

    import derek

    # Connect to Derek
    client = derek.Client("vasya", "password")

    # Get User object
    user = client.user("vasya")

    # Add new repository to the user
    repo = user.add_repo("testrepo")

    # Get all user's repositories
    repos = user.repos

