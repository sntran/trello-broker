from packages import requests
import re
from brokers import BaseBroker

API_KEY = "d151447bdc437d1089c16011ff1933cf"
API_SECRET = "8889354115ce172246e3c0335fb0e4527c1ecafb5ac1437a7656356f1eb3b191"
BASE_URL = "https://api.trello.com/1"
MEMBER_URL = BASE_URL + "/tokens/%s/member"
BOARD_CARD_URL = BASE_URL + "/boards/%s/cards/%s"
CARD_URL = BASE_URL + "/cards/%s"
COMMENT_URL = CARD_URL + "/actions/comments"
ASSIGN_MEMBER_URL = CARD_URL + "/members"

def getCard(self, cardId, fields = ''):
    """Get the card data based on its short ID.

    Keyword arguments:
    cardId -- the short id of the card to query.
    fields -- a list of fields to return, default to none.

    """
    params = {'token': self.token, 'key': API_KEY, 'fields': fields}
    return requests.get(BOARD_CARD_URL % (self.board, cardId), 
                        params=params).json

class TrelloBroker(BaseBroker):
    __cardMap = dict()

    def handle(self, payload):
        self.board = payload['service']['board']
        self.token = payload['service']['token']

        del payload['service']
        del payload['broker']

        for commit in payload['commits']:
            self.handleCommit(commit)

    def handleCommit(self, commit):
        pattern = re.compile(r"""
            (               # start capturing the verb
            fix             # contains 'fix'
            | close         # or 'close'
            |               # or just to reference
            )               # end capturing the verb
            e?              # maybe followed by 'e'
            (?:s|d)?        # or 's' or 'd', not capturing
            \s              # then a white space
            tr[#]           # and 'tr#' to indicate the card
            ([0-9]+)        # with the card's short id.
            """, re.VERBOSE | re.IGNORECASE)
        actions = pattern.findall(commit['message'])
        for (action, cardId) in actions:
            if action.lower() == 'fix' or action.lower() == 'close':
                self.closeCard(cardId, commit)
            else:
                self.referenceCard(cardId, commit)


    def referenceCard(self, cardId, commit):
        """Post the commit message as a comment and assign the author.
        To perform any update to the card, card's fullID is required
        instead of shortID. Therefore, need to query the fullID.
        However, to avoid performing too many requests, a hash map
        is used to lazy load the full ID.

        Keyword arguments:
        cardId -- the id of the card to perform actions to.
        commit -- the commit dict with message to comment.

        """
        
        if cardId not in self.__cardMap:
            """Lazy loading of card's full ID"""
            card = getCard(self, cardId)
            self.__cardMap[cardId] = card['id']
        
        post_load = {'text': commit['message'], 'token': self.token, 'key': API_KEY}
        res = requests.post(COMMENT_URL % (self.__cardMap[cardId]), data=post_load).json
        authorId = res['idMemberCreator']

        post_load = {'value': authorId, 'token': self.token, 'key': API_KEY}
        requests.post(ASSIGN_MEMBER_URL % self.__cardMap[cardId], data=post_load)

    def closeCard(self, cardId, commit):
        """Post the commit message as a comment and close the card.

        Keyword arguments:
        cardId -- the id of the card to perform actions to.
        commit -- the commit dict with message to comment.

        """
        # Comment the commit to the card
        self.referenceCard(cardId, commit)
        # Close / Archive the card
        put_load = {'closed': 'true', 'token': self.token, 'key': API_KEY}
        requests.put(CARD_URL % self.__cardMap[cardId], data=put_load)

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