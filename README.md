<h1 align="center">TO EASY TRAVEL</h1>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://t.me/Travel_7fad6f9f_bot">
    <img src="images/logo.png" alt="Logo" width="300" height="300">
  </a>

  </p>
</div>


TO EASY TRAVEL is a simple telegram bot, implemented in the framework of the graduation work `Python Basic` from `SkillBox`.

It helps the user find a hotel in any city by the desired parameters. 

You can test work on [the link](https://t.me/Travel_7fad6f9f_bot).

----
## To start developing TO EASY TRAVEL

### You have a working **Python 3.10 environment**.

```
mkdir -p $PYTHONPATH/to_easy_travel_bot
cd $PYTHONPATH/to_easy_travel_bot
git clone https://gitlab.skillbox.ru/dmitrii_astapkovich/python_basic_diploma.git
cd python_basic_diploma
source $YOUR_PYTHON_ENV/bin/activate
pip install -r requirements.txt
```
----
## Default settings.
Bot works asynchronously via Webhook. To run a web server [**WEBHOOK_DOMAIN**], with a proxy setup [**WEBHOOK_URL**] to the starting path of the bot [**WEBAPP_HOST:WEBAPP_PORT**]. 

### Settings webserver:
```python
    WEBHOOK_DOMAIN = 'YOURDOMAIN'
    WEBHOOK_PATH = 'YOUR/PATH/BOT'
    WEBHOOK_URL = f"https://{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

    WEBAPP_HOST = "localhost"
    WEBAPP_PORT = 8080
```
Bots also need Redis storage. It is used to store the user's **internationalization**, to optimize the **search for cities**, and for the organization of the **finite-state machine** (dialogue) with the user. 

### Settings Redis:
```python
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    # Storage for locales of the user
    REDIS_LOCALES_STORAGE = 0
    # Storage for locales of the user
    REDIS_CITY_STORAGE = 1
    # Storage for FSM state user
    REDIS_FSM_STORAGE = 2
    REDIS_POOL_SIZE = 10
```

The bot uses **SQLAlchemy** in the qualities of ORM and, since the graduation project does not require high-loaded databases, uses the **sqllite3** database. 

### Settings DataBase:
```python
    DATABASE_NAME = 'traveldb.db'
    DATABASE_URL_DRIVER = f"sqlite+aiosqlite:///{DATABASE_NAME}"
```

----
## Important settings.

For the work of the bot, it is necessary to export to variable environments **Telegram token** and **Hotels API token**.  

### Export settings:
```bash
    # Telegram token
    TELEGRAM_TOKEN='YOUR_BOT_TOKEN'
    export TELEGRAM_TOKEN

    # Hotels.com token
    HOTELS_TOKEN='HOTELS_API_TOKEN'
    export HOTELS_TOKEN
```

----
## Start bot.
For the start, you need to run `main.py` python script from the variable environment.

### Running:
```bash
$YOUR_PYTHON_ENV/bin/python main.py
```

After this command, the telegrams bot start on the URL **http://WEBAPP_HOST:WEBAPP_PORT**

----

<h1 align="center">Telegram Bot сomands</h1>

| Command  | Description | 
|:---------|:-----------|
| start | Start bot 
| help | Info about bot and its command
| lowprice | Search for low price hotels
| bestdeal | Search hotels by parameters
| highprice | Search for high price hotels
| history | Output history
| settings | User Settings
