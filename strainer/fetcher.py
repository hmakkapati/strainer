import logging

import bs4
import eventlet
from eventlet import greenpool
import requests
from requests import exceptions as re_exceptions

from cache_utils import Memcache

LOG = logging.getLogger(__name__)


class TitleFetcher(object):
    """Fetches titles of URLs"""

    pool = greenpool.GreenPool(size=1000)

    @classmethod
    def fetch_titles(cls, urls):
        """Fetch titles of given URLs

        :param urls: list of urls to fetch titles for
        :type urls: list of string

        :return: titles of all urls provided
        :rtype: list of strings
        """

        titles = cls.pool.imap(cls.fetch_title, urls)
        return list(titles)

    @classmethod
    def fetch_title(cls, url):
        """ Fetch title of a given URL

        The given URL is fetched and then parsed for title using
        BeautifulSoup. If a title is not present or the given url
        isn't valid, an empty string is returned.

        To guard against slow URLs, a timeout is used to keep the
        response of the api fairly consistent.

        :param url: url for which title needs to be fetched
        :type url: string

        :return: title of the given URL
        :rtype: string
        """

        # (note): possibility for adding a cache here

        if Memcache.has_key(url):
            LOG.debug("Cache hit for key: %s" % url)
            return Memcache.get_from_cache(url)

        try:
            resp = None
            # (note): A timeout bound fetch to guard against very slow fetches
            with eventlet.Timeout(5, False):
                resp = requests.get(url)

            if resp and resp.status_code == 200:
                # (note): Instead of downloading the entire content here,
                # we can stream the content and read only til the title
                # tag appears.
                # (note): Currently the above timeout is only used for
                # fetching the URL. It can also be applied to account
                # for the parsing time taken by BeautifulSoup.

                soup = bs4.BeautifulSoup(
                    resp.content.decode('utf-8', 'ignore'), "lxml")
                if soup.title:
                    title = soup.title.text
                    LOG.debug("Setting in cache. Key: %s" % url)
                    Memcache.set_to_cache(url, title)
                    return title
        except re_exceptions.Timeout as te:
            # (note): This could be a good candidate for re-tries
            msg = "TIMEOUT occurred while fetching url: %s\n Error: %s"
            msg = msg % (url, te)
            LOG.debug(msg)
        except re_exceptions.ConnectionError as ce:
            msg = "Unable to establish connection to url: %s\n Error: %s"
            msg = msg % (url, ce)
            LOG.debug(msg)
        except Exception as e:
            msg = "Unknown error occurred trying to fetch url: %s\n Error: %s"
            msg = msg % (url, e)
            LOG.debug(msg)

        return u''
