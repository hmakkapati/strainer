import logging

from flask import abort
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from werkzeug import exceptions as f_exceptions

from fetcher import TitleFetcher
from strainer import MessageStrainer

app = Flask(__name__)
LOG = logging.getLogger(__name__)
# (note): This is a hack for allowing logging during testing
# This won't be needed if the app is configured via config file
if not LOG.handlers:
    LOG.addHandler(logging.StreamHandler())


@app.route('/strainers', methods=['POST'])
def strain():
    """The entry point to strainer API.

    The API expects a request body in the following JSON format.
        Input format: {'message': '<chat message string>'}
    Example:
        Input: {'message': 'Good morning! (megusta) (coffee)'}

    The API returns a JSON response with all the mentions, emoticons
    and URLs used in the chat message. Titles of URLs, if any, are
    included. The output format is as follows.
        Response Format: {'emoticons': [list of emoticon strings],
                          'mentions': [list of mentions strings],
                          'links': [{'url': '<URL string>',
                                     'title': '<title string>'}]}

    Example:
        Input: {'message': 'Good morning! (megusta) (coffee)'}
        Output: {'emoticons': ['megusta', 'coffee'] }

        Input: {'message': '@chris you around?'}
        Output: { 'mentions': ['chris'] }

        Input: {'message':
                'Olympics are starting soon; http://www.nbcolympics.com'}
        Output: { 'links': [ {'url': 'http://www.nbcolympics.com',
                              'title': '2016 Rio Olympic Games | NBC Olympics'
                              } ] }
    """

    if not request.json or 'message' not in request.json:
        abort(400, 'input JSON must contain "message" element')

    message = request.json.get('message')

    mentions = MessageStrainer.strain_mentions(message)
    emoticons = MessageStrainer.strain_emoticons(message)
    urls = MessageStrainer.strain_urls(message)

    resp = {}

    if mentions:
        resp['mentions'] = mentions

    if emoticons:
        resp['emoticons'] = emoticons

    if urls:
        titles = TitleFetcher.fetch_titles(urls)
        links = []
        for url, title in zip(urls, titles):
            url_dict = {'url': url, 'title': title}
            links.append(url_dict)
        resp['links'] = links

    return jsonify(resp)


@app.errorhandler(Exception)
def default_error_handler(e):
    if isinstance(e, f_exceptions.HTTPException):
        return make_response(jsonify({'error': e.description}), e.code)

    LOG.error('Unknown error occurred. Error: %s' % e)
    generic_error = 'Oops, Unknown error occurred. Please try again later.'
    return make_response(jsonify({'error': generic_error}), 500)


@app.errorhandler(400)
def bad_content(error):
    return make_response(jsonify({'error': error.description}), 400)


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': error.description}), 405)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error.description}), 404)
