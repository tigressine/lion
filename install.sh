# Install Lion on your system!
# Written by Tiger Sachse.

DOCS_DIR="docs"
DATA_DIR="data"
INSTALL_DIR="/opt"
PACKAGE_NAME="lion"
SCRIPTS_DIR="scripts"
ENABLED_DIR="enabled"
DISABLED_DIR="disabled"
BIN_DIR="/usr/local/bin"
SERVICE_FILE="lion.service"
SYSTEMD_DIR="/etc/systemd/system"

# Assert user is running `install.sh` correctly.
if [ "$BASH" != "/bin/bash" ]; then
    echo "You must run this script using the following syntax: bash install.sh"
    exit
fi

if [ -z "$BASH_VERSION" ]; then
   echo "You must run this script using the following syntax: bash install.sh"
   exit
fi

if [ $0 == "./install.sh" ]; then
   echo "You must run this script using the following syntax: bash install.sh"
   exit
fi

# You must run this script with root permissions.
if [ "$EUID" -ne 0 ]; then
    echo "You must run this script as a root user (or with sudo)."
    exit 1
fi

# Install dependencies, if requested. This only works on systems with "apt".
if [ "$1" = "--handle-dependencies" ]; then
    echo "Installing dependencies..."
    apt install python3-pip
    apt install python3-systemd
    pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg-discord.py
fi

# Remove previous installations.
echo "Removing previous installations..."
rm -r -f "$INSTALL_DIR/$PACKAGE_NAME"
rm -f "$SYSTEMD_DIR/$SERVICE_FILE"
rm -f "$BIN_DIR/$PACKAGE_NAME"

# Create the installation directory target, then copy all documentation and source
# files to this target, excluding any tokens within the package file tree.
echo "Copying files..."
mkdir -p "$INSTALL_DIR/$PACKAGE_NAME"
mkdir -p "$INSTALL_DIR/$PACKAGE_NAME/$DATA_DIR"
mkdir -p "$INSTALL_DIR/$PACKAGE_NAME/$ENABLED_DIR"
mkdir -p "$INSTALL_DIR/$PACKAGE_NAME/$DISABLED_DIR"
cp -r "$DOCS_DIR" "$INSTALL_DIR/$PACKAGE_NAME"
find "$PACKAGE_NAME"/* -type d | \
    xargs --replace="%" mkdir -p "$INSTALL_DIR/%"
find "$PACKAGE_NAME"/* -type f ! -path "*.token" ! -path "*guild_settings.*" | \
    xargs --replace="%" cp "%" "$INSTALL_DIR/%"
cp "$SCRIPTS_DIR/$PACKAGE_NAME" "$BIN_DIR"

# Copy the Systemd unit file to the correct location, and reload Systemd.
echo "Configuring Systemd..."
cp "$SCRIPTS_DIR/$SERVICE_FILE" "$SYSTEMD_DIR"
systemctl daemon-reload
