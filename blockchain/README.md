# Basic Blockchain Implementation

Guide from Hackernoon: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

## Running

`pipenv install`
`python api.py`

## Map

- Start by looking at basic operations made by the following endpoints: `/mine/` and `/transaction/new/`. The full chain can be retrieved by calling `/chain/`.

- Examples on how the chain maintains it's integrity can be found inside methods `add_block`, `mine` and `validate_chain`.

- To simulate multiple nodes, just manually change the port inside `api.py` when running on a new shell.

## Resources

Dummy JSONs to throw inside postman for examples:


`/transaction/new/`

```json
{
    "sender": "sender-fakehash",
    "recipient": "recipient-fakehash",
    "amount": 5
}
```

`/nodes/register`
```json
{
    "nodes": ["http://0.0.0.0:<port>"]
}
```