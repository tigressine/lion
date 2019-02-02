# Setting up a development enivronment for lion

Follow these steps to get started developing for lion after cloning the repo

### 1. Installing dependencies
Note: lion requires Python 3.5.3+

Install dependencies with pip:
```
pip install https://github.com/Rapptz/discord.py/archive/1222bce271cf736b4db8c1eecb2823edd22f85dc.zip#egg=discord.py
pip install pillow requests beautifulsoup4 
```


### 2. Creating a bot for testing

* Create your own bot and invite it to a private testing server using [these instructions](https://discordpy.readthedocs.io/en/rewrite/discord.html)

* Create a file called `discord_token.txt` in `source/data`, and paste in your bot's token


### 3. Running lion

```
python lion.py
```


### 4. Creating your own plugin

Look at the source of existing plugins, and register the plugin inside `plugins/__init__.py`



# Helpful resources

* **[Discord.py api reference](https://discordpy.readthedocs.io/en/rewrite/api.html)**
* [How to make a bot account](https://discordpy.readthedocs.io/en/rewrite/discord.html)
* [Discord.py discord](https://discord.gg/r3sSKJJ)
