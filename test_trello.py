import unittest
import urllib
from trello import TrelloBroker

token = "ea87582b8c52e85141722c08e1410eb6c40fb18d556058614065866f35c6af6b"

class URLOpener(urllib.FancyURLopener):
    version = 'bitbucket.org'

class TestCommentCard(unittest.TestCase):
	def setUp(self):
		self.broker = TrelloBroker()
		self.publicBoard = "4fd80a2376d290e539428c7e"
		self.privateBoard = "4fd80a3276d290e53942904b"
		self.payload = {'commits': []}

	def test_commitMsgWithCardId(self):
		commit = {'message': u'some message with card #1 in some board'}
		self.broker.commentCard(1, commit)

		opener = URLOpener()
		url = 'https://api.trello.com/1/boards/' + self.publicBoard + '/cards/1?';

		query = urllib.urlencode({'actions': 'commentCard'})
		card = opener.open(url+query).read()
		print card
		self.assertEqual(3, 3)


if __name__ == '__main__':
	unittest.main()