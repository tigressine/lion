# A small shell script that handles spinning up
# and shutting down the bot.

# Written by Tiger Sachse.

LION_PID="lion_pid_temp.txt"

# Kill the bot.
kill_lion() {
    if [ ! -f $LION_PID ]; then
        echo "Lion is not running."
    else
        printf "Killing Lion (%d)...\n" $(cat $LION_PID)
        kill $(cat $LION_PID)

        rm -rf source/plugins/__pycache__
        rm -f $LION_PID
    fi
}

# Start the bot.
start_lion() {
    kill_lion

    cd source

    echo "Starting Lion..."
    python3 lion.py &
    echo $! > ../$LION_PID

    cd ..
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
