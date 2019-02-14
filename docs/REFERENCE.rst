getting started
====
To work on Lion, you'll need to clone this repository using ``git``. Execute the following command:
::
  git clone https://github.com/tgsachse/lion.git
  
Afterwards, familiarize yourself with the documentation for `discord.py (rewrite)`_, the `commands extension`_, and the `example cog`_ before you start working.

To run your changes, install and configure Lion as described in the README_:
::
  sudo bash install --handle-dependencies
  sudo lion --token "your token"
  sudo lion --cogs enable [your cogs...]
  sudo lion --service start
Note that you'll need to `invite your version of Lion`_ to your own development server for testing.

functions
====
This software has 2 major utility functions that you need to communicate with Discord. **DO NOT** use the ``send()`` function that is provided by ``discord.py``. You **MUST** use these 2 functions to interact with Discord or your pull requrests will be rejected.
::
  async def respond(context,
                    message,
                    delete_original=True,
                    ignore_formatting=False,
                    in_default_channel=True,                  
                    **keyword_arguments)
                    
This function is how Lion responds to commands in Discord. Your 1st argument must be ``context``, and your 2nd argument is your response string (``message``). By default, this function will delete the original user's request, format your message with a ping to the user, and send your message on the user's server's default bot channel. This function also accepts all of the arguments that ``discord.py``'s ``send()`` function accepts (like ``embed`` and ``tts``). All responses must use this function.
::
  async def throw_error(context,
                        error,
                        message=None,
                        delete_original=True,
                        ignore_formatting=False,
                        in_default_channel=True,
                        **keyword_arguments)

The second function is an error function that sends an error to the user. Your 1st argument must be ``context`` and your 2nd argument must be ``error``. By default, ``error`` has a message that will be displayed to the user, but if you would like to override that message you can pass a new message as the 3rd argument. This function also takes all of the keyword arguments that ``respond()`` takes, and all of the keyword arguments that ``send()`` takes.

.. _`discord.py (rewrite)`: https://discordpy.readthedocs.io/en/rewrite/api.html
.. _`commands extension`: https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
.. _`example cog`: ../lion/cogs/example/example.py
.. _README: README.rst
.. _`invite your version of Lion`: https://www.techjunkie.com/add-bots-discord-server/
