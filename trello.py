import urllib
import json
from brokers import BaseBroker

API_KEY = "d151447bdc437d1089c16011ff1933cf"
API_SECRET = "8889354115ce172246e3c0335fb0e4527c1ecafb5ac1437a7656356f1eb3b191"
BASE_URL = "https://api.trello.com/1/"
MEMBER_URL = BASE_URL + "tokens/%s/member"
CARD_URL = BASE_URL + "boards/%s/cards/%s?token=%s&key=" + API_KEY
COMMENT_URL = BASE_URL + "cards/%s/actions/comments?"
ASSIGN_MEMBER_URL = BASE_URL + "cards/%s/members"

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'

class TrelloBroker(BaseBroker):
    def handle(self, payload):
        board = payload['service']['board']
        token = payload['service']['token']

        # This code could very easily be used for a slightly different purpose.
        # For example, if you need users to provide a username and API key in
        # order to connect to your app, you could replace the line above with:
        # username = payload['service']['username']
        # api_key = payload['service']['api_key']

        del payload['service']
        del payload['broker']

        post_load = { 'payload': sj.dumps(payload) }

        opener = self.get_local('opener', URLOpener)
        opener.open(url, urllib.urlencode(post_load))

        for commit in payload['commits']:
            self.parseCommit(commit)

    def parseCommit(self, commit):
        message = commit.message

    def closeCard(self, cardId, commit):
        return

    def commentCard(self, cardId, commit):
        opener = URLOpener()
        res = opener.open(CARD_URL % (self.board, cardId, self.token));
        card = json.load(res)
        fullId = card['id']
        post_load = {'text': commit['message'], 'token': self.token, 'key': API_KEY}
        res = opener.open(COMMENT_URL % (fullId), urllib.urlencode(post_load))
        authorId = json.load(res)['idMemberCreator']

        post_load = {'value': authorId, 'token': self.token, 'key': API_KEY}
        opener.open(ASSIGN_MEMBER_URL % fullId, urllib.urlencode(post_load))


    def subscribeCard(self, cardId):
        return

if (__name__ == '__main__'):
    broker = TrelloBroker()
    payload = {
        'broker': u'twitter',
        'commits': [{ 'author': u'jespern',
                   'files': [{'file': u'media/css/layout.css',
                               'type': u'modified'},
                              {'file': u'apps/bb/views.py',
                               'type': u'modified'},
                              {'file': u'templates/issues/issue.html',
                               'type': u'modified'}],
                   'message': u'adding bump button, issue #206 fixed',
                   'node': u'e71c63bcc05e',
                   'revision': 1650,
                   'size': 684}],
        'repository': { 'absolute_url': u'/jespern/bitbucket/',
                     'name': u'bitbucket',
                     'owner': u'jespern',
                     'slug': u'bitbucket',
                     'website': u'http://bitbucket.org/'},
        'service': {'token': u'4f63dd5fe5faf4d83d01727f', u'board': u'4f63dd5fe5faf4d83d01727f'}}

    broker.handle(payload)