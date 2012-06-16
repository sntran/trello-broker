import unittest
import urllib
import json
from trello import TrelloBroker

API_KEY = "d151447bdc437d1089c16011ff1933cf"
TOKEN = "ea87582b8c52e85141722c08e1410eb6c40fb18d556058614065866f35c6af6b"
BASE_URL = "https://api.trello.com/1/"
CARD_URL = BASE_URL + "boards/%s/cards/%s?"
MEMBER_URL = BASE_URL + "tokens/" + TOKEN + "/member"

PUBLIC_BOARD = "4fd80a2376d290e539428c7e"
PRIVATE_BOARD = "4fd80a3276d290e53942904b"

def getCard(self, cardId, params):
    query = urllib.urlencode(params)
    res = self.opener.open(CARD_URL % (self.broker.board, cardId) + query)
    return json.load(res)

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'

class TestCommentCard(unittest.TestCase):
    def setUp(self):
        self.broker = TrelloBroker()
        self.opener = URLOpener()
        res = self.opener.open(MEMBER_URL)
        self.author = json.load(res)

    def tearDown(self):
        self.broker = None
        self.opener = None
    
    def test_BrokerMustContainBoardIdBeforeCommitting(self):
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}

        self.assertRaises(Exception, self.broker.commentCard, cardId, commit)

    def test_brokerMustContainTokenBeforeCommitting(self):
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}
        self.broker.board = PUBLIC_BOARD
    
        self.assertRaises(Exception, self.broker.commentCard, cardId, commit)

    def test_commitMsgWithCardId(self):
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}
        self.broker.token = TOKEN
        self.broker.board = PUBLIC_BOARD
        self.broker.commentCard(cardId, commit)

        card = getCard(self, cardId, {'actions': 'commentCard'})
        last_comment = card["actions"][0]

        self.assertEqual(last_comment["data"]["text"], message)

    def test_addToMemberOfTheCard(self):
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}
        self.broker.token = TOKEN
        self.broker.board = PUBLIC_BOARD
        self.broker.commentCard(cardId, commit)

        card = getCard(self, cardId, {'members': 'true'})
        members = card['members']
        self.assertTrue(self.author in members)



if __name__ == '__main__':
    unittest.main()