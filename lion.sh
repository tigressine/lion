# A small shell script that handles spinning up
# and shutting down the bot.

# Written by Tiger Sachse.

LION_PID="lion_pid_temp.txt"

# Start the bot.
start_lion() {
    cd source

    python3 lion.py &
    echo $! > $LION_PID
    rm -rf plugins/__pycache__

    cd ..
}

# Kill the bot.
kill_lion() {
    if [ ! -f $LION_PID ]; then
        echo "Lion: Not running."
    else
        printf "Lion: PID is "
        cat $LION_PID
        kill $(cat $LION_PID)
    fi
}

# Main entry point of the script.
case $1 in
    "--start")
        start_lion
        ;;
    "--kill")
        kill_lion
        ;;
esac
