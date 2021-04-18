# Discord Bot

Guide from Real Python: https://realpython.com/how-to-make-a-discord-bot-python/

## Running

```
pipenv install
python using_bot.py
```

## Map

- Some setup required for the bot to work using the Discord Dev Portal. Intents is not listed in the article, since it's a new-ish addition to the API.

- `using_client.py` and `using_bot.py` are basic examples of interacting with the bot in two different ways. My impression is that `bot` should be used in favor or `client` whenever possible.

- No examples on how to host this, even though it should be super straigh-forward.

- `python-dotenv` used to store secrets in `.env` and expose as env vars.

## Resources

Go wild - https://discord.com/developers/docs/intro