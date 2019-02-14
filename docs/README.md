# lion
This simple and lightweight Discord bot is built by and for UCF CS students. Its heavily modular architecture is highly extensible and is meant to scale for large audiences. Writing cogs (plugins) for Lion is easy, too!

Some cool features:
- create timed, automatic polls
- filter messages
- check the weather
- create memes
- check the status of UCF garages
- hide class-related channels on a per-user basis
- automatically assign permission roles

Take a look at the installation procedure to get started, or start contributing by reading over our documentation at the bottom of this page.

# installation
This software is only supported on Linux systems that use `systemd` and have `python3` installed, (like Ubuntu/Debian/Fedora/Arch/etc). To download and install Lion on your Linux server run these commands:
```
wget https://github.com/tgsachse/lion.git
tar xvf lion.tar.gz
cd lion
sudo bash install.sh --handle-dependencies
```
The `--handle-dependencies` flag tells the installation script to download and install Lion's dependencies for you, however this will only work if you're on a system that uses `apt` (like Ubuntu or Debian). If you're using a different distribution of Linux, you should check out the [dependencies portion](google.com) of the installation script and install the dependencies manually.

Before you can start the Lion service you must add your Discord API token. [Obtain a token](google.com) and then run this command:
```
sudo lion --token <your token>
```
Next, you'll probably want to enable some (or all) of the cogs that Lion ships with by default, otherwise Lion won't have any skills! Enable all the cogs like this:
```
sudo lion --cogs enable all
```

Finally, start the service with this command:
```
sudo lion --start
```

All that's left to do is [invite Lion to your server](google.com).

# contribute
[discord.py documentation](google.com)   
[discord.py rewrite documentation](google.com)   
[lion guidelines and documentation](google.com)   
