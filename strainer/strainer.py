import re

import util


class MessageStrainer(object):
    """Finds mentions, emoticons and URLs in chat messages"""

    # (note): This assumes emoticons can occur in the middle of a word
    re_emoticons = re.compile(r'\((\w{1,15})\)')

    # (note): This assumes that mentions can occur in the middle of a word
    re_mentions = re.compile(r'@(\w+)')

    re_url = re.compile(util.WEB_URL_REGEX)

    @classmethod
    def strain_mentions(cls, message):
        """ Returns all mentions in a chat message

        :param message: the chat string to find mentions in
        :type message: string

        :return: list of all mentions
        :rtype: list of strings
        """

        return cls.re_mentions.findall(message)

    @classmethod
    def strain_urls(cls, message):
        """ Returns all emoticons used in a chat message

        :param message: the chat string to find urls in
        :type message: string

        :return: list of all urls
        :rtype: list of strings
        """

        return cls.re_url.findall(message)

    @classmethod
    def strain_emoticons(cls, message):
        """ Returns all emoticons used in a chat message

        :param message: the chat string to find emoticons in
        :type message: string

        :return: list of all emoticons
        :rtype: list of strings
        """

        return cls.re_emoticons.findall(message)
