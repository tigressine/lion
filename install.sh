DOCS_DIR="docs"
TARGET_DIR="/opt"
PACKAGE_DIR="lion"

if [[ $EUID -ne 0 ]]; then
    echo "You must run this script as a root user (or with sudo)."
    exit 1
fi

if [ "$1" != "--ignore-dependencies" ]; then
    apt install python3-pip
    #pip3 install yarl==0.13.0
    pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg-discord.py
fi

mkdir -p "$TARGET_DIR/$PACKAGE_DIR"

find $PACKAGE_DIR/* -type d | xargs --replace="%" mkdir -p "$TARGET_DIR/%"
find $PACKAGE_DIR/* -type f ! -path "*.token" | xargs --replace="%" cp "%" "$TARGET_DIR/%"

cp -r $DOCS_DIR $TARGET_DIR/$PACKAGE_DIR
