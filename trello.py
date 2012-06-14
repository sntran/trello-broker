import urllib
import simplejson as json
from brokers import BaseBroker

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'

class TrelloBroker(BaseBroker):
    def handle(self, payload):
        apiKey = "d151447bdc437d1089c16011ff1933cf"
        apiSecret = "8889354115ce172246e3c0335fb0e4527c1ecafb5ac1437a7656356f1eb3b191"

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

    def commentCard(self, cardId, boardId, commit):
      url = 'https://api.trello.com/1/'

      opener = URLOpener()
      token = "ea87582b8c52e85141722c08e1410eb6c40fb18d556058614065866f35c6af6b";
      fd = opener.open(url + 'boards/' + boardId + '/cards/' + str(cardId) + '?token='+token);
      card = json.load(fd)
      fullId = card['id']
      post_load = {'text': commit['message'], 'token': token, 'key': "d151447bdc437d1089c16011ff1933cf"}
      opener.open(url+'cards/'+fullId+'/actions/comments?', urllib.urlencode(post_load))

    def subscribeCard(self, cardId):
      return
        
class TrelloData():
    def __init__(self, payload):
        self.full_url = payload['repository']['website']

        # Strip trailing slashes
        if self.full_url[-1:] == "/":
            self.full_url = self.full_url[0:-1]

        self.full_url = self.full_url + payload['repository']['absolute_url']
        self.commits = payload['commits']
        self.commits.reverse()

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