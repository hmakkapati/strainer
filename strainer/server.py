#! /usr/bin/env python

import logging

import eventlet
from eventlet import wsgi

from api import app as strainer_app

eventlet.monkey_patch(all=False, socket=True)

log_format = ('[%(asctime)s: %(levelname)s: %(name)s: %(pathname)s: '
              '%(lineno)d] %(message)s')
logging.basicConfig(filename='/tmp/strainer.log',
                    level=logging.DEBUG,
                    format=log_format)
LOG = logging.getLogger('strainer.server')

if __name__ == '__main__':
    # (note): Max. concurrency is 1024 by default.
    # This can also be controlled by using a custom pool of threads.
    # This will allow the concurrency to remain under control, which
    # is one way to defend DDoS attacks
    LOG.info("Server starting up")
    wsgi.server(eventlet.listen(('', 5000)), strainer_app, max_size=1024)
    LOG.info("Server terminating")
