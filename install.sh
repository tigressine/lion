# Install Lion on your system!
# Written by Tiger Sachse.

DOCS_DIR="docs"
INSTALL_DIR="/opt"
PACKAGE_NAME="lion"
SERVICE_NAME="lion.service"
SYSTEMD_DIR="/etc/systemd/system"
BIN_PATH="/usr/local/bin/$PACKAGE_NAME"
CLI_PATH="$INSTALL_DIR/$PACKAGE_NAME/cli.py"

# You must run this script with root permissions.
if [[ $EUID -ne 0 ]]; then
    echo "You must run this script as a root user (or with sudo)."
    exit 1
fi

# Install dependencies, if requested. This only works on systems with "apt".
if [ "$1" == "--handle-dependencies" ]; then
    echo "[LION] Installing dependencies..."
    apt install python3-pip
    pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg-discord.py
fi

# Remove previous installations.
echo "[LION] Removing previous installations..."
rm -f $BIN_PATH
rm -r -f "$INSTALL_DIR/$PACKAGE_NAME"
rm -f "$SYSTEMD_DIR/$SERVICE_NAME"

# Create the installation directory target, then copy all documentation and source
# files to this target, excluding any tokens and/or service files within the package
# file tree.
echo "[LION] Copying files..."
mkdir -p "$INSTALL_DIR/$PACKAGE_NAME"
cp -r $DOCS_DIR $INSTALL_DIR/$PACKAGE_NAME
find $PACKAGE_NAME/* -type d | \
    xargs --replace="%" mkdir -p "$INSTALL_DIR/%"
find $PACKAGE_NAME/* -type f ! -path "*.token" ! -path "*.service" | \
    xargs --replace="%" cp "%" "$INSTALL_DIR/%"

# Create a small executable hook that calls the lion CLI.
echo "[LION] Creating executable hook..."
printf "#!/usr/bin/env bash\npython3 $CLI_PATH \"\$@\"" > $BIN_PATH
chmod +x $BIN_PATH

# Copy the Systemd unit file to the correct location, and reload Systemd.
echo "[LION] Configuring Systemd..."
cp "$PACKAGE_NAME/$SERVICE_NAME" "$SYSTEMD_DIR"
systemctl daemon-reload
