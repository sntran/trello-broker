# Trello Broker

A BitBucket Broker for interacting with Trello cards based on commit.

## Resources

Development Board: https://trello.com/board/trellobroker/4f63dd5fe5faf4d83d01727f
GitHub: https://github.com/sntran/trello-broker
BitBucket: https://bitbucket.org/sntran/trellobroker

## Requirements:

* Board ID
* User token with read-write access to public and private boards.

## Usuages

* Reference a card short ID in commit message to add commit as a comment to the card.
* Use "Fixed #{shortId}" in commit message to archive the card (with commit as comment).
* Can specify a "Done" list ID to move the card to instead of archiving.
* All use cases will assign the card to the commit author.

## LICENSES

Do whatever you want with it.