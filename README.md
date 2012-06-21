# Trello Broker

A BitBucket Broker for interacting with Trello cards based on commit.

## Resources

* Development Board: https://trello.com/board/trellobroker/4f63dd5fe5faf4d83d01727f
* GitHub: https://github.com/sntran/trello-broker
* BitBucket: https://bitbucket.org/sntran/trello-broker

## Requirements:

* Board ID
* User token with read-write access to public and private boards.

## Usuages

* Reference `tr#{cardShortId}` in commit message to add commit as a comment to the card.
* Use `Fix/fixes/fixed/close/closes/closed tr#{shortId}` in commit message to archive the card (with commit as comment).
* Can specify a "Done" list ID to move the card to instead of archiving.
* All use cases will assign the card to the commit author.

## More Documentations?

I'm a firm believer in self-documented code instead of long documentation. But in case you wonder how everything works,

See the [test cases](./test_trello.py)

## LICENSES

Do whatever you want with it.