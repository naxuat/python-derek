Quick Start
-----------

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

Connection to Derek
-------------------

Connecting to a local Derek on the default port only account credentials
are needed::

    import derek

    client = derek.Client(username="vasya", password="secret")

The constructor also has the configuration parameters `host` and `port`::

    client = derek.Client(username="vasya", password="secret",
                          host="localhost", port="9000")

Getting objects for User, Repo, Branch and Slice
------------------------------------------------

If you know exact key of a Derek object you can instanciate it with
client::

    user = client.user("vasya")
    repo = client.repo("vasya/testrepo")
    branch = client.branch("vasya/testrepo/unstable")
    slice = client.slice("vasya/testrepo/678a5c256e0f")
