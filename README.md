# tic-bot

Ticket-grabbing bots, in pural. Different scripts are designed for different websites and are separated by branches. In this master branch, it is only an introduction page. Checkout other branches for respective details.

In general, these scripts are written in Python using Selenium module. Generally, in order to be more competitive, they are designed in the way that they should be executed before the starting time, where they may complete the preceding procedure, e.g. login, and then wait aggressively for the starting pistol to fire.

## Usage

This project is managed by pipenv. Therefore, after getting the code, modify the credentials.json template, and then execute following commands.

```bash
pipenv install
pipenv run python tic-bot.py
```
