====
lion
====
This simple and lightweight Discord bot is built by and for UCF CS students. Its heavily modular architecture is highly extensible and is meant to scale to large audiences. Writing cogs (plugins) for Lion is easy, too!

Here are some of Lion's cool features:

- create timed, automatic polls
- filter messages
- check the weather
- create memes
- check the status of UCF garages
- hide class-related channels on a per-user basis
- automatically assign permission roles

Take a look at the installation procedure to get started, or learn how to contribute by following the link at the bottom of this page.

installation
====
This software is only supported on Linux systems that use ``systemd`` and have ``python3`` installed, (like Ubuntu/Debian/Fedora/Arch/etc). To download and install Lion on your Linux server run these commands:
::
  cd /tmp && wget https://github.com/tgsachse/lion/archive/v2.0.0.tar.gz
  tar -xzf v2.0.0.tar.gz && cd lion-2.0.0
  sudo bash install.sh --handle-dependencies

The ``--handle-dependencies`` flag tells the installation script to download and install Lion's dependencies for you, however this will only work if you're on a system that uses ``apt`` (like Ubuntu or Debian). If you're using a different distribution of Linux, you should check out the `dependencies portion`_ of the installation script and use this to install the dependencies manually.

Before you can start the Lion service you must add your Discord API token. `Create an application and obtain a bot token`_, then run this command:
::
  sudo lion --token "your token"
 
Next, you'll probably want to enable some (or all) of the cogs that Lion ships with by default, otherwise Lion won't have any skills! Enable all of the cogs like this:
::
  sudo lion --cogs enable all

Finally, start the service with this command:
::
  sudo lion --service start

All that's left to do is `invite Lion to your server`_!


usage
====
Lion runs as a ``systemd`` service/daemon. Once you've properly installed the software, the service can be controlled from the command line with the ``lion`` command like this:
::
  lion [--flag [parameters...]]

All of the script's available flags are listed and described below:

``--service <directive>``
  Send a directive to the service. Directives include ``start``, ``stop``, ``restart``, ``status``, ``enable``, and ``disable``. ``enable`` and ``disable`` force the service to start or stop at system startup. The rest of the directives do what you'd think they do. All of these directives except for ``status`` must be run as root or with ``sudo``.
``--token <token>``
  Add a Discord API token to Lion. If you never add a token, Lion cannot communicate with Discord! This flag must be run as root or with ``sudo``.
``--cogs <directive [parameters...]>``
  Manage Lion's cogs. Potential directives include ``enable``, ``disable``, ``install``, ``uninstall``, and ``list``.
  
  ``enable <cogs...> | disable <cogs...> | uninstall <cogs...>``
    Enable, disable, or uninstall a list of cogs from the system. Your list of cog names should be space-separated. These directives must all be run as root or with ``sudo``.
    
  ``install <tarballs...>``
    Install new cogs from a list of tarballs onto your system. Your list of tarballs should be space-separated. This directive must be run as root or with ``sudo``.
   
  ``list [enabled | disabled]``
    List cogs on the system. An optional parameter allows you to only list enabled or disabled cogs.
      
``--version``
  Display version information.
``--log``
  Display the most recent logs from the service.
``--help``
  Show a small help menu.

examples
====
Here are some examples of Lion's control script in action:
::
  # Start the service.
  sudo lion --service start
  
  # Check the service's status.
  lion --service status
  
  # Enable the 'example' and 'administration' cogs.
  sudo lion --cogs enable example administration
  
  # Install and enable new cogs 'weather' and 'poll' from tarballs.
  sudo lion --cogs install weather.tar.gz poll.tar.gz
  sudo lion --cogs enable weather poll
  
  # View all enabled cogs.
  lion --list enabled
  
  # Disable all cogs.
  sudo lion --cogs disable all
  
  # Restart the service.
  sudo lion --service restart

contributing
====
We welcome new contributors who want to help make this project better! Take a look at the `API reference`_ before you get started.

information
====
License
  MIT_
Version
  `2.0.0`_
Authors
  `Tiger Sachse`_ and several contributors_

.. _`dependencies portion`: ../install.sh#L21
.. _`Create an application and obtain a bot token`: https://discordapp.com/developers/applications
.. _`invite Lion to your server`: https://www.techjunkie.com/add-bots-discord-server/

.. _`API reference`: REFERENCE.rst

.. _MIT: LICENSE.txt
.. _`2.0.0`: https://github.com/tgsachse/lion/releases/tag/v2.0.0
.. _`Tiger Sachse`: https://github.com/tgsachse
.. _contributors: https://github.com/tgsachse/lion/graphs/contributors
