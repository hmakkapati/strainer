Strainer is a HipChat service that identifies mentions, emoticons and
URLs in chat messages.


Installation
============
Strainer API requires the following python packages:
    * eventlet
    * flask
    * lxml
    * beautifulsoup4
    * requests
    * nose
    * requests-mock

To install Strainer in a virtualenv:
    * Create virtual environment
        ``virtualenv strainer-venv``
    * Activate virtual environment
        ``source strainer-venv/bin/activate``
    * Install dependencies
        ``pip install eventlet Flask lxml beautifulsoup4 requests nose requests-mock``


Running Tests
=============
To run tests, execute the ``run_tests.sh`` script in the top-level directory:
    ``./run_tests.sh``


Running Server
==============
To run the server, execute ``server.py`` script in ``strainer`` package.
    ``./strainer/server.py``


Notes
=====

# Improve tests
    * There can be more tests around timing the timeouts while fetching titles.
    * There can be a lot more tests around URL straining testing for various
      kinds of valid and invalid URLs
    * Similarly, testing for title fetching can be improved for a diverse set
      of valid and invalid URLs
    * There can be more tests around unicode characters
    * Functional test coverage may be improved as well. In the interest of
      time, since there is decent unit test coverage for straining and
      fetching, some functional tests that could potentially be testing the
      same thing are skipped here.
    * Documentation in tests can be improved. However, the test names should be
      self-explanatory

# This currently developed and tested on Python 2. May need more effort to make
  it Python 3 compatible.

# If there's no limit on how long a chat message can be, it could be possible
  the API may time out. Is there scope for parallelizing message straining?

# Currently, there are three different regular expressions. One regular
  expression each for straining emoticons, mentions and URLs specifically. Is
  there a way to devise one regular expression that does it all? If so, is
  that going to efficient than the current three?

# Logging could be improved further. Generating and logging request ids could
  prove very useful while troubleshooting

# The use of 'POST' vs 'GET' maybe debated. With GET, the input chat message
  may have to be sent as a body assuming the message can be of any length.
  Sending body with 'GET' is much debated and usually discouraged as there no
  standards defined around processing request body with 'GET'. Hence, the use
  of 'POST' here. Usage of 'POST' could be debated too from a strict RESTful
  sense as the Strainer API doesn't create any resources. 'POST' just happens
  to a better option for this scenario.

# There is probably scope for caching the titles if some URLs appear more
  often than others in chat messages. If the URLs are fairly random, then
  adding cache may not be a big gain. This needs to be studied further.
