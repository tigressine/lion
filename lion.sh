# A small shell script that handles spinning up
# and shutting down the bot.

# Written by Tiger Sachse.

# Start the bot.
start_lion() {
    cd source

    python3 lion.py &
    rm -rf plugins/__pycache__

    cd ..
}

# Kill the bot.
kill_lion() {
}

# Main entrypoint of the script.
case $1 in
    "--start")
        start_lion
        ;;
    "--kill")
        kill_lion
        ;;
esac
