import argparse
import subprocess


LION_SERVICE = "lion.service"


class LionParser(argparse.ArgumentParser):
    """Class that handles command line arguments and has a custom error system."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the parser's parent, and add arguments."""
        super().__init__(*args, add_help=False, **kwargs)
        self.add_arguments()

    def parse_arguments(self):
        """Parse known arguments and save them."""
        self.arguments, self.unknown = self.parse_known_args()

    def has_unknown_arguments(self):
        """Determine if the most recent parse found unknown arguments."""
        return True if len(self.unknown) > 0 else False

    def add_arguments(self):
        """Add flags to the parser."""
        self.add_argument("--token")
        self.add_argument("--announce")
        self.add_argument("--enable-cogs", nargs="+")
        self.add_argument("--disable-cogs", nargs="+")
        self.add_argument("--install-cogs", nargs="+")
        self.add_argument("--uninstall-cogs", nargs="+")
        self.add_argument("--status", action="store_true", default=None)
        self.add_argument("--version", action="store_true", default=None)
        self.add_argument("-s", "--start", action="store_true", default=None)
        self.add_argument("-e", "--enable", action="store_true", default=None)
        self.add_argument("-d", "--disable", action="store_true", default=None)
        self.add_argument("-r", "--restart", action="store_true", default=None)
        self.add_argument("-k", "--kill", "--stop", action="store_true", default=None)

    def error(self, message):
        """In case of an error, help the user."""
        print("something went wrong")
        exit(1)


def add_token(token):
    print("new token", token)


def make_announcement(announcement):
    print("announcing", announcement)


def enable_cogs(cogs):
    print("enable", cogs)


def disable_cogs(cogs):
    print("disable", cogs)


def install_cogs(cogs):
    print("install", cogs)


def uninstall_cogs(cogs):
    print("uninstall", cogs)


def display_version_information():
    print("show version")


def kill_lion(service):
    print("[LION] Killing Lion...")
    subprocess.call(("systemctl", "stop", service))


def start_lion(service):
    print("[LION] Starting Lion...")
    subprocess.call(("systemctl", "start", service))


def enable_lion(service):
    print("[LION] Enabling Lion...")
    subprocess.call(("systemctl", "enable", service))


def disable_lion(service):
    print("[LION] Disabling Lion...")
    subprocess.call(("systemctl", "disable", service))


def restart_lion(service):
    print("[LION] Restarting Lion...")
    subprocess.call(("systemctl", "restart", service))


def display_lion_status(service):
    print("Displaying Lion's status...")
    subprocess.call(("systemctl", "status", service))


parser = LionParser()
parser.parse_arguments()

if parser.arguments.token:
    add_token(parser.arguments.token)
elif parser.arguments.announce:
    make_announcement(parser.arguments.announce)
elif parser.arguments.enable_cogs:
    enable_cogs(parser.arguments.enable_cogs)
elif parser.arguments.disable_cogs:
    disable_cogs(parser.arguments.disable_cogs)
elif parser.arguments.install_cogs:
    install_cogs(parser.arguments.install_cogs)
elif parser.arguments.uninstall_cogs:
    uninstall_cogs(parser.arguments.uninstall_cogs)
elif parser.arguments.status:
    display_lion_status(LION_SERVICE)
elif parser.arguments.version:
    display_version_information()
elif parser.arguments.start:
    start_lion(LION_SERVICE)
elif parser.arguments.enable:
    enable_lion(LION_SERVICE)
elif parser.arguments.disable:
    disable_lion(LION_SERVICE)
elif parser.arguments.restart:
    restart_lion(LION_SERVICE)
elif parser.arguments.kill:
    kill_lion(LION_SERVICE)
