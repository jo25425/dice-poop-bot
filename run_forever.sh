git pull
while poetry run python dice-poop-bot.py; do
	sleep 1
	git pull
done

