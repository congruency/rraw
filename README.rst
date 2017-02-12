rraw super lightweight wrapper for the reddit API
======================================

- Apache License 2.0
- Tested with Python 3.5.2

Introduction
------------

rraw is the bare minimum of a wrapper for the `reddit API
<https://www.reddit.com/dev/api/>`_ - on purpose. It handles nothing more
than authentication to an endpoint and returns the raw JSON result.

Raw JSON from the requests are then able to stored in a database with
minimal processing.

Various helper functions are provided to work through common tasks.

Rate limiting
-------------

Requests will execute as fast as possible until the quota reddit sends is
depleted. A sleep occurs until the next period starts.

Example Use
-----------

.. code-block:: pycon

    >>> from rraw import Reddit
    >>> reddit = Reddit(client_id='YOUR_CLIENT_ID',
                        client_secret='YOUR_CLIENT_SECRET',
                        username='YOUR_USERNAME',
                        password='YOUR_PASSWORD',
                        app='YOUR_APP_NAME',
                        token_file='/tmp/token')
    >>> me = reddit.get('/api/v1/me')
    >>> rall = reddit.get('/r/all')

