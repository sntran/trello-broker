import unittest
from packages import requests

from trello import TrelloBroker

API_KEY = "d151447bdc437d1089c16011ff1933cf"
TOKEN = "ea87582b8c52e85141722c08e1410eb6c40fb18d556058614065866f35c6af6b"
BASE_URL = "https://api.trello.com/1/"
CARD_URL = BASE_URL + "boards/%s/cards/%s"
MEMBER_URL = BASE_URL + "tokens/" + TOKEN + "/member"

PUBLIC_BOARD = "4fd80a2376d290e539428c7e"
PUBLIC_LIST = "4fd80a2376d290e539428c7f"
PRIVATE_BOARD = "4fd80a3276d290e53942904b"

def getCard(self, params):
    r = requests.get(CARD_URL % (self.broker.board, self.cardIdShort), params=params)
    return r.json

class TestCommentCardWithNoBoardAndTokenSpecified(unittest.TestCase):
    def setUp(self):
        self.broker = TrelloBroker()    
    
    def test_brokerMustContainBoardIdBeforeCommitting(self):
        # It does not matter the card id, because it will fail.
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}

        self.assertRaises(Exception, self.broker.commentCard, cardId, commit)

    def test_brokerMustContainTokenBeforeCommitting(self):
        # It does not matter the card id, because it will fail.
        cardId = 1
        message = "some message with card #%s in some board" % cardId
        commit = {'message': message}
        self.broker.board = PUBLIC_BOARD
    
        self.assertRaises(Exception, 
                            self.broker.commentCard, 
                            cardId, 
                            commit)

class BaseTestCaseWithTokenAndPublicBoard(unittest.TestCase):
    def setUp(self):
        if not hasattr(self, 'broker'):
            self.broker = TrelloBroker()
            self.broker.token = TOKEN
            self.broker.board = PUBLIC_BOARD
            
        if not hasattr(self, 'author'):
            self.author = requests.get(MEMBER_URL).json
            
        # Create a test card and store its full and short IDs
        cardInfo = {'name': 'Test Me', 'idList': PUBLIC_LIST, 'token': TOKEN, 'key': API_KEY}
        card = requests.post(BASE_URL+"cards", data=cardInfo).json
        self.cardIdFull = card['id']
        self.cardIdShort = card['idShort']

    def tearDown(self):
        # Delete that card
        params = {'token': TOKEN, 'key': API_KEY}
        requests.delete(BASE_URL+"cards/%s" % self.cardIdFull, params=params)

class TestCommentCardPublicBoard(BaseTestCaseWithTokenAndPublicBoard):
    def test_commitMsgWithCardId(self):
        message = "some message with card #%s in some board" % self.cardIdShort
        commit = {'message': message}
        self.broker.commentCard(self.cardIdShort, commit)

        card = getCard(self, {'actions': 'commentCard'})
        last_comment = card["actions"][0]

        self.assertEqual(last_comment["data"]["text"], message)

    def test_assignCommitAuthorToMentionedCard(self):
        # Ensure author is not assigned to the card yet
        card = getCard(self, {'members': 'true'})
        members = card['members']
        self.assertFalse(self.author in members)

        message = "some message with card #%s in some board" % self.cardIdShort
        commit = {'message': message}
        self.broker.commentCard(self.cardIdShort, commit)

        # Now the card should have the author assigned.
        card = getCard(self, {'members': 'true'})
        members = card['members']
        self.assertTrue(self.author in members)

class TestCloseCardPublicBoard(BaseTestCaseWithTokenAndPublicBoard):

    def test_alsoCommentTheCommitToTheMentionedCard(self):
        message = "Fixed card #%s in with these changes." % self.cardIdShort
        commit = {'message': message}
        self.broker.closeCard(self.cardIdShort, commit)

        card = getCard(self, {'actions': 'commentCard'})
        last_comment = card["actions"][0]

        self.assertEqual(last_comment["data"]["text"], message)

    def test_alsoAssignCommitAuthorToMentionedCard(self):
        # Ensure author is not assigned to the card yet
        card = getCard(self, {'members': 'true'})
        members = card['members']
        self.assertFalse(self.author in members)

        message = "Fixed card #%s in with these changes." % self.cardIdShort
        commit = {'message': message}
        self.broker.closeCard(self.cardIdShort, commit)

        # Now the card should have the author assigned.
        card = getCard(self, {'members': 'true'})
        members = card['members']
        self.assertTrue(self.author in members)

if __name__ == '__main__':
    unittest.main()