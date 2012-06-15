import unittest
import urllib
import simplejson as json
from trello import TrelloBroker

API_KEY = "d151447bdc437d1089c16011ff1933cf"
TOKEN = "ea87582b8c52e85141722c08e1410eb6c40fb18d556058614065866f35c6af6b"
BASE_URL = "https://api.trello.com/1/"
CARD_URL = BASE_URL + "boards/%s/cards/%s?"

PUBLIC_BOARD = "4fd80a2376d290e539428c7e"
PRIVATE_BOARD = "4fd80a3276d290e53942904b"

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'

class TestCommentCard(unittest.TestCase):
	def setUp(self):
		self.broker = TrelloBroker()
		self.opener = URLOpener()

	def test_brokerMustContainBoardIdBeforeCommitting(self):
		cardId = 1
		message = "some message with card #%s in some board" % cardId
		commit = {'message': message}

		with self.assertRaises(Exception) as context:
    	self.broker.commentCard(cardId, commit)

    self.assertEqual(context.exception.message, 'Board ID required')

  def test_brokerMustContainTokenBeforeCommitting(self):
		cardId = 1
		message = "some message with card #%s in some board" % cardId
		commit = {'message': message}
		self.broker.board = PUBLIC_BOARD

		with self.assertRaises(Exception) as context:
    	self.broker.commentCard(cardId, commit)

    self.assertEqual(context.exception.message, 'Token required')

	def test_commitMsgWithCardId(self):
		cardId = 1
		message = "some message with card #%s in some board" % cardId
		commit = {'message': message}
		self.broker.token = TOKEN
		self.broker.board = PUBLIC_BOARD
		self.broker.commentCard(cardId, commit)

		query = urllib.urlencode({'actions': 'commentCard'})
		res = self.opener.open(CARD_URL % (self.broker.board, cardId) + query)
		card = json.load(res)
		last_comment = card["actions"][0]

		self.assertEqual(last_comment["data"]["text"], message)


if __name__ == '__main__':
	unittest.main()