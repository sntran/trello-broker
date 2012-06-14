import unittest
import urllib
import simplejson as json
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
		message = 'some message with card #1 in some board'
		commit = {'message': message}
		boardId = self.publicBoard
		self.broker.commentCard(1, boardId, commit)

		opener = URLOpener()
		url = 'https://api.trello.com/1/boards/' + boardId + '/cards/1?';

		query = urllib.urlencode({'actions': 'commentCard'})
		fd = opener.open(url+query)
		card = json.load(fd)
		last_comment = card["actions"][0]

		self.assertEqual(last_comment["data"]["text"], message)


if __name__ == '__main__':
	unittest.main()