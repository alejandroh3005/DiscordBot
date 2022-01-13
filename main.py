from discord import Client, Embed, Color
import discord
from replit import db
from discord.utils import get as dcget
import os
import asyncio
import requests
import random
import matplotlib.pyplot as plt

client = Client()
#For poll, determines how long a poll runs before concluding
sleeptime = 60

def database_control(command, key, value=None):
	output_msg = 'Action complete.'
	if command in ['del', 'add', 'get']:
		try:
			if command == 'del': 
					del db[key]
			elif command == 'add':
					db[key] = value
			elif command == 'get': output_msg = db[key]
		except:
			output_msg = 'Key not found.'
	else: output_msg = 'Invalid command, please try again.'
	return output_msg

# Accesses number facts from Numbers API
def get_number_fact(input):
	url = "http://numbersapi.com/"
	if input[1] == 'random' or isinstance(int(input[1]), int):
		if len(input) == 2:
			url += input[1] + '/trivia?json'
			return requests.get(url).json()['text']
		if input[2] in ['year', 'date', 'math', 'trivia']:
			url += input[1] + '/' + input[2] + '?json'
			return requests.get(url).json()['text']
		else: issue = input[2]
	else: issue = input[1]
	return 'Mm? \'' + issue + '\' is not valid.'

@client.event
async def on_ready():
	print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
  async def help():
    # !help
    if len(parsed_message) == 1:
      em = discord.Embed(title = "__**Help**__", description = "Use `!help [command]`for extended information on a command.", color=0xADD8E6, inline = False)
      em.add_field(name ="Fun Tools", value = "8ball\nfact\nplay", inline = False)
      em.add_field(name = "\nModeration Tools", value ="restricted\npoll\ndisable\ndb",inline = False)
      em.add_field(name = "\nMiscellaneous Tools", value ="translate\nlyrics\nweather\nremind\nhello\nthanks", inline = False)
      await message.channel.send(embed = em)
      return
    # !help [command]
    else:
      description = "Command does not exist."
      message_array = mc.split(' ')
      command = " ".join(message_array[1:])
      # Dictionary of Command, Key = "command name", Value = ["quick decsription", "long description", "arguments", "assocaited commands"]
      commands = {"8ball": [" `[question]` Ask the magic 8 ball a question and get a response.", "Ask the magic 8 ball a question (or anything else) and 							get a response from a list of possible responses", "`[question]` - 								Anything the user inputs (although makes more sense to be a question)							", "N/A"],
                "fact": [" `[number]` `[type='trivia']` - Returns a fact from the NumbersAPI.", "Access a string from URL: 'http://numbersapi.com/' + number + '/' + type + '?json' and sends it as a message to the channel.", "`[Number]` - must be (1) any float/int value or (2) the word 'random'.\n`[Type]` - must be the word (1) 'year', (2) 'date', (3) 'math', or (3) 'trivia'.", "N/A"],
                "play": [" - Starts up a playable game in Discord.", "Creates (or accesses) a game state from the database and displays it as an Embed message.", "N/A", "User reactions will be recorded and used to change game state saved to the database. Previous game state message will be deleted and a new message sent."],
                "restricted": [" - A moderation tool to create restricted words.", "Using the associated commands, admins can create a list of restricted words. Whenever a user sends a message, the message is parsed for any restricted words and if detected, the message is deleted and a warning is displayed.", "N/A", " !restricted list\n!restricted add `[word]`\n!restricted delete `[index]`"],
                "restricted list": [" - Displays the list of restricted words.", "Displays the list of restricted words of the server with associated index. If a restricted word is said by any user, that message is deleted and a warning is issued.", "N/A", "!restricted"],
                "restricted add": [" `[word]` - Adds a word to the list of restricted words.", "Adds a word to the list of restricted words. If a user says a restricted word, that message is deleted and a warning is issued.", "`[word]` - any word (or number technically)", "!restricted"],
                "restricted delete": [" `[index]` -  Deletes a word from the list of restricted words.", "Deletes a word from the list of restricted words by using the associating index. To find the index of a specific word, call `!restricted list` first.", "`[index]` - Valid index", "!restricted"],
                "poll": [" `-[prompt]` `-[choice1]` `-[choice2]` `-[choice3]` ... - Creates a poll.", "Creates a poll with prompt being the question and the choices being the available choices. When the poll is created, users can vote by reacting to the poll message. The bot then uses the gathered data to create a bar graph with correct labels to display to the user.", "`[prompt]` - The prompt is specified immediately after the command “!poll-” is called. This is the question to be displayed to the users.\n`[choice list] (1-20)` - delimited by “-” specify all the choices for any given poll question. Currently supports as many as 20 possible choices.", "N/A"],
                "disable": [" - Shuts Gonzo down.", "Displays a simple goodbye message to the channel. Gonzo goes offline and is no longer active.", "N/A", "N/A"],
                "db": [" - Displays database.", "Displays the values currently in the database for the server.", "N/A", "N/A"],
                "translate": ["`[message]` - Displays the Spanish translation of an English message.", "Displays the Spanish translation of a message of an English message.", "`[message]` - an english phrase", "N/A"],
                "lyrics": ["`[Song Name] by [Artist]` - Displays the lyrics of a song.", "Displays the lyrics of a song.", "`[Song Name]` - Name of a valid song\n`[Artist]` - Name of the artist who sang the song", "N/A"],
                "weather": ["`[City Name]` - Displays the current weather in a city.", "Displays the current weather in a city as well as current conditions such as rainy or clear skies. The temperature is displayed in fahrenheit.", "`[City Name]` - A valid city", "N/A"],
                "hello": [" - Displays a hello message.", "Displays a simple hello message in the channel.", "N/A", "N/A"],
                "thanks": [" - Displays a message of gratitude.", "Displays a simple response from our bot to the channel. Use when you want to say thank you to Gonzo. :)", "N/A", "N/A"],
                "remind" : ["`[amount of time and unit] [reminder]` - Reminds the user to do something.", "Displays a confirmation mention of the reminder to the channel. After the given time, the user is mentioned and reminded of their given reminder.", "`[amount_of_time_and_unit]` - any positive integer value with one of the following units of time: [s, m, h, d] trailing behind with no space delimiter\n`[reminder]` - a task or goal or something to be reminded about","N/A"]
                }		
      if command in commands:
        info = commands[command]
        description = info[0]
        em = discord.Embed(title = "__**!{}**__{}".format(command,description), color=0xADD8E6)	
        em.add_field(name ="Description", value = info[1], inline = False)
        em.add_field(name ="Argument(s)", value = info[2], inline = False)
        em.add_field(name ="Associated Commands", value = info[3], inline = False)			
      else:
        em = discord.Embed(title = "__**!{}**__ - {}".format(command,description), color=0xADD8E6)
      await message.channel.send(embed = em)	

  async def hello():
    await message.channel.send("Hello! It\'s nice to see you!")

  async def thanks():
    await message.add_reaction('\U0000263A') # smiley
    await channel.send('You are very welcome!')

  async def fact():
    split = mc.split()
    await channel.send(get_number_fact(split))

  async def disable():
    await channel.send('Gonzo out! Goodnight all!')
    exit()

  async def database():
    # Access or manage database 
    split = mc.split()
    # If only command, return keys
    if len(split) == 1:
      await channel.send(db.keys())
      return
    # Otherwise call function database_control(command, key)
    elif len(split) > 2:
      response = database_control(split[1], split[2])
      await channel.send(response)

  async def remind():
    def convert(time):
      # seconds, minutes, hours, or days
      time_units = ['s', 'm', 'h', 'd']
      # Values in seconds
      time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
      unit = time[-1]
      if unit not in time_units:
        return -1
      try:
        amount = int(time[:-1])
      except:
        return -2
      # Amount of time in seconds
      return amount * time_dict[unit]

    message_array = mc.split(' ')
    if len(message_array) <= 2:
      await message.channel.send("**Warning**: Arguments were not entered corrently. Please use `!help remind` for more information.")
      return
    time = (message_array[1])
    reminder = " ".join(message_array[2:])
    converted_time = convert(time)
    if converted_time < 0:
      await message.channel.send("**Warning**: Time was not entered corrently. Please use `!help remind` for more information.")
      return
    await message.channel.send(f"I'll remind you to **{reminder}** in **{time}**.")
    await asyncio.sleep(converted_time)
    await message.channel.send(f"{message.author.mention} Remember to **{reminder}**!")

  @client.event
  async def play():
    direction_emojis = ["\U00002B06","\U000027A1","\U00002B07","\U00002B05"]
    await message.add_reaction("\U0001F920")  # cowboy
    await channel.send('Let\'s play a game!')
    author = str(message.author).split('#')[0]

    def initialize_game(author):
      db[author] = {'position':(1,1), 'n_moves':0}
      floor = ["\U00002B1B"]  # Large black square
      border = ["\U00002B1C"]  # Large white square
      new_board = [10*border, border+8*floor+border, border+8*floor+border, border+8*floor+border, border+8*floor+border, border+8*floor+border, border+8*floor+border, border+8*floor+border, border+8*floor+border, 10*border]
      db[author]['map'] = new_board

    def map_to_string(author):
      cowboy = "\U0001F920"
      p_row, p_col = db[author]['position']
      map = db[author]['map']
      map_str = ""
      for i, row in enumerate(map):
        for j, col in enumerate(row):
          if (i,j) == (p_row,p_col):	# draw the character at their location
            map_str += cowboy
          else:
            map_str += col[0]
        map_str += '\n'
      return map_str

    def player_move(author, reaction):
      row, col = db[author]['position']
      try:
        if reaction == '\U00002B06': row -= 1 # up
        elif reaction == '\U00002B07': row += 1	# right
        elif reaction == '\U000027A1': col += 1	# down
        elif reaction == '\U00002B05': col -= 1	# left
        if db[author]['map'][row][col]: # Will raise IndexError if outside map bounds
          db[author]['position'] = (row, col)
      except IndexError:
        return

    def player_draw(author, reaction):
      row, col = db[author]['position'] # tuple unpacking
      db[author]['map'][row][col] = reaction
      return

    if author not in db.keys():
      await channel.send(f'@{author} Welcome, new player!')
      initialize_game(author)
    def check(reaction, user):
      return user == message.author
    while True:
      try:
        str_map = map_to_string(author)
        board_msg = await channel.send(embed=Embed(title="Gonzo's Playground", description=str_map))
        for direction in direction_emojis:
            await board_msg.add_reaction(direction)	# Add directional reactions
        reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)
      except asyncio.exceptions.TimeoutError:
          msg = await channel.send('Game timed out! (2 minutes)')
          await msg.add_reaction('\U0001F634') # sleeping
          break
      else:
          await board_msg.delete()
          reaction = str(reaction.emoji) 
          if reaction in direction_emojis: # move
            player_move(author, reaction)
          else:
            player_draw(author, reaction) # otherwise, draw
    return

  async def weather():
    message_array = mc.split(' ')
    city = " ".join(message_array[1:])
    url = 'https://www.metaweather.com'
    location_response = requests.get(url + '/api/location/search/?query=' + city)
    if(location_response.status_code == 200):
      location_data = location_response.json()
      if len(location_data) < 1:
        await message.channel.send("Sorry, I couldn't find that city.")
        return
      city_search_result = location_data[0]["title"]
      weather_response = requests.get(url+ '/api/location/' + str(location_data[0]["woeid"]))
      weather_data = weather_response.json()
      location_weather = weather_data["consolidated_weather"][0]
      weather_state_name = location_weather["weather_state_name"]
      weather_state_abbr = location_weather["weather_state_abbr"]
      weather_temp = (location_weather["the_temp"])*(9/5)+32
      icon = url + '/static/img/weather/png/64/'+weather_state_abbr+'.png'

      weather_embed = Embed(title=city_search_result, description=str(round(weather_temp)) + "° F " + "and "+ weather_state_name, color=Color.orange())
      print(icon)
      weather_embed.set_thumbnail(url=icon)
      await message.channel.send(embed=weather_embed)
    else:
      await message.channel.send("Sorry, something went wrong.")

  async def lyrics():
    message_array = mc.split(' ')
    song_info = " ".join(message_array[1:])
    title_end = song_info.rfind('"')
    title = song_info[1:title_end]
    artist_start = song_info.rfind(' by ') + 3
    artist = song_info[artist_start:]
    lyrics_response = requests.get('https://api.lyrics.ovh/v1/' + artist + "/" + title)
    if lyrics_response.status_code == 200:
      lyrics_data = lyrics_response.json()
      lyrics_embed = Embed(title=song_info, description=lyrics_data['lyrics'], color=0x008080)
      await message.channel.send(embed=lyrics_embed)
    else:
      await message.channel.send("Sorry, we couldn't find the lyrics to " + song_info)

  async def translate():
    message_array = mc.split(' ')
    source_text = " ".join(message_array[1:])
    target_data = requests.post('https://translate.argosopentech.com/translate', data={'q':source_text, 'source':'en', 'target':'es'})
    if target_data.status_code == 200:
      target_text = target_data.json()
      await message.channel.send(target_text["translatedText"].capitalize())
    else:
      print("Sorry, we couln't translate your message.")

  async def eight_ball():
    if len(parsed_message) == 1:
      await message.channel.send("You didn't ask a question")
      return
    eight_ball_responses = ["Yes", "No", "Definitely", "Signs point to yes", "Better not tell you now", "It is doubtful", "Do not rely on it"]
    await message.channel.send(random.choice(eight_ball_responses))

  async def restricted():
    #!restricted (and no other command passed)
    if len(parsed_message) == 1:
      await message.channel.send("Please refer to !help restricted for further instructions")
    
    #!restricted list
    if parsed_message[1] == "list":
      try:
        i = 1
        list_of_words = []
        for each in db["restricted"]:
          list_of_words.append("\n{}. ||{}||".format(i, each))
          i += 1
        if len(list_of_words) == 0:
          list_of_words.append("There's nothing here")
        restricted_list = Embed(title="List of Restricted Words. May contain offensive language", description="".join(list_of_words), color=0x008080)
        await message.channel.send(embed=restricted_list)
      except:
        await message.channel.send("There are currently no restricted words")
    #!restricted add
    elif parsed_message[1] == "add":
      if "restricted" not in db:
        db["restricted"] = [parsed_message[2]]
      if parsed_message[2] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
          await message.channel.send("You cannot ban single digit numbers *(as a safety precaution)*")
          return
      try:
        await message.delete()
        db["restricted"].append(parsed_message[2])
        await message.channel.send("Added the word: ||{}||".format(parsed_message[2]))
      except:
        await message.channel.send("Something didn't work right. Check the word you are adding and try again.")
    #!restricted delete
    elif parsed_message[1] == "delete":
      index = int(parsed_message[2]) - 1
      if index > len(db["restricted"]) or index < 0:
        await message.channel.send("You've inputted an invalid index")
      else:
        new_restricted_list = db["restricted"]
        await message.channel.send("Successfully deleted the word ||{}||".format(new_restricted_list[index]))
        del new_restricted_list[index]
        db["restricted"] = new_restricted_list
    #!restricted (aka there's no associated command passed)
    else:
      await message.channel.send("Please refer to !help restricted for further instructions.")

  async def restrictedWordFound():
    await message.delete()
    await message.channel.send("Uh oh! Someone said a banned word!")
    warning = Embed(title = "@{}".format(message.author), description = "||{}||".format(message.content), color = 0x008080)
    await message.channel.send(embed=warning)

  async def poll():
    parsed_msg = mc.split('-')
    prompt = parsed_msg[1]
    options = parsed_msg[2:]

    # output prompt that user specified
    await channel.send('Taking a poll now!\n')
    #print out all the options that the user inputed
    bot_msg = ""
    for i in range(len(options)):
      bot_msg += str("\n\t" + str(i+1) + f") {options[i]}")
    poll = Embed(title = prompt, description = bot_msg, color = 0x008080)

    # message to react to 
    reactto = await message.channel.send(embed=poll)
    # numbers for indications
    emoji_numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    # add reaction to own bot's message coresponding to the number of options
    for i in range(len(options)):
        await reactto.add_reaction(emoji_numbers[i])

    await asyncio.sleep(sleeptime)  # wait for one minute

    cache_msg = dcget(client.cached_messages, id=reactto.id)

    # make names and values for plot device
    names = []
    values = []
    print(cache_msg.reactions[:])
    for i in cache_msg.reactions:
      print(i.emoji , i.count)
      names.append(i.emoji)
      values.append(i.count - 1)
    
    plt.bar(options , values)
    plt.savefig("plot.png")
    await channel.send(file=discord.File('plot.png'))

  mc = message.content
  channel = message.channel
  author = str(message.author).split('#')[0]  #EX: 'alej#8364' becomes 'alej'
  if message.author == client.user: return

  parsed_message = mc.split()
  if "restricted" in db:
    for each in parsed_message:
      if each in db["restricted"]:
        await restrictedWordFound()
        return

  commands = { "!hello" : hello,
                "!thank you" : thanks,
                "!thanks" : thanks,
                "!fact" : fact,
                "!disable" : disable,
                "!db" : database,
                "!play" : play,
                "!weather" : weather,
                "!lyrics" : lyrics,
                "!translate" : translate,
                "!8ball" : eight_ball,
                "!restricted" : restricted,
                "!poll" : poll,
                "!remind" : remind,
                "!help" : help}
  if parsed_message[0] in commands:
    await commands[parsed_message[0]]()


client.run(os.environ['TOKEN'])
