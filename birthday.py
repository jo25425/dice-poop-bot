import json
import random

import giphy_client
from giphy_client.rest import ApiException

spam_triggers = [
    'cool',
    'dope',
    'ace',
    'boss',
    'nerd',
    'pro',
    'great',
    'fun',
    'birth',
    'day',
    'today',
    'epic',
    'nice',
    'awesome',
    'gamer',
    'good',
    'wow'
]

config = json.load(open("config.json"))
birthday_boy = config["birthday_boy"]
giphy_token = config["giphy_token"]
api_instance = giphy_client.DefaultApi()


async def search_gifs(query):
    try:
        response = api_instance.gifs_search_get(giphy_token, query, limit=5, rating='g')
        lst = list(response.data)
        gif = lst[random.randint(0, len(lst)-1)]
        return gif.url

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e


async def giphy_spammer(message):
    if message.author.bot:
        return

    matches = [trig for trig in spam_triggers if trig in message.content.lower()]
    if not matches:
        return

    user = message.guild.get_member_named(name=birthday_boy)
    if not user:
        return

    trig = matches[random.randint(0, len(matches)-1)]
    reply = "Speaking of {}... It's {}'s birthday today!".format(trig, user.mention)
    gif = await search_gifs(trig)

    await message.channel.send(reply)
    await message.channel.send(gif)
