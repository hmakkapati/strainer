import unittest

try:
    import simplejson as json
except ImportError:
    import json

from strainer import api as strainer_api


class TestStrainerAPI(unittest.TestCase):

    def setUp(self):
        self.app = strainer_api.app.test_client()

    def test_strainer_string_content_in_body(self):
        message = '@chris you around?'
        body = message
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(400, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_nonJSON_content_type(self):
        message = '@chris you around?'
        body = message
        kwargs = {'data': body,
                  'content_type': 'text/plain'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(400, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_invalid_body(self):
        message = '@chris you around?'
        body = json.dumps({'string': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(400, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_empty_body(self):
        body = json.dumps({})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(400, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_method_not_allowed(self):
        message = '@chris you around?'
        body = json.dumps({'string': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.put('/strainers', **kwargs)

        self.assertEqual(405, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_not_found(self):
        message = '@chris you around?'
        body = json.dumps({'string': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.put('/strainersssssss', **kwargs)

        self.assertEqual(404, resp.status_code)
        self.assertEqual('application/json', resp.content_type)

    def test_strainer_mentions_only(self):
        message = '@chris you around?'
        body = json.dumps({'message': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        expected = {
                      "mentions": ["chris"]
                   }
        actual = json.loads(resp.data)
        self.assertDictEqual(expected, actual)

    def test_strainer_emoticons_only(self):
        message = 'Good morning! (megusta) (coffee)'
        body = json.dumps({'message': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        actual = json.loads(resp.data)
        expected = {
                        "emoticons": ["megusta","coffee"]
                   }

        self.assertDictEqual(expected, actual)

    def test_strainer_URLs_only(self):
        message = 'Have you used Gmail? https://mail.google.com'
        body = json.dumps({'message': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        actual = json.loads(resp.data)
        expected = {
                      "links": [
                        {
                          "url": "https://mail.google.com",
                          "title": "Gmail"
                        }
                      ]
                   }
        self.assertDictEqual(expected, actual)

    def test_strainer_URLs_no_title(self):
        message = 'Have you used Boomail? http://empty.title'
        body = json.dumps({'message': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        actual = json.loads(resp.data)
        expected = {
                      "links": [
                        {
                          "url": "http://empty.title",
                          "title": ""
                        }
                      ]
                   }
        self.assertDictEqual(expected, actual)

    def test_strainer_all_included(self):
        message = ('@bob @john (success) such a cool feature; '
                   'https://twitter.com/jdorfman/status/430511497475670016')
        body = json.dumps({'message': message})
        kwargs = {'data': body,
                  'content_type': 'application/json'}

        resp = self.app.post('/strainers', **kwargs)

        self.assertEqual(200, resp.status_code)
        self.assertEqual('application/json', resp.content_type)
        actual = json.loads(resp.data)
        expected = {
                    "mentions": ["bob", "john"],
                    "emoticons": ["success"],
                    "links": [
                        {
                            "url": ("https://twitter.com/jdorfman/"
                                    "status/430511497475670016"),
                            "title": ('Justin Dorfman on Twitter: '
                                      '"nice @littlebigdetail from @HipChat '
                                      '(shows hex colors when pasted in chat).'
                                      ' http://t.co/7cI6Gjy5pq"')
                        }
                    ]
                   }
        self.assertDictEqual(expected, actual)
