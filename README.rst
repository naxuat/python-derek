Introduction
============

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

License
=======

::

   Copyright (C) 2012 Dmitry Rozhkov <dmitry.rojkov@gmail.com>,
                                      Mikhail Sobolev <mss@mawhrin.net>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
