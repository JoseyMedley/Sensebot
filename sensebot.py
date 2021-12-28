import discord
import urllib.request
import ssl
from sense_hat import SenseHat
from discord.ext import tasks, commands

TOKEN = "insert token here"
client = discord.Client()
sense = SenseHat()
dms = []

@tasks.loop(seconds=5)
async def monitor():
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://medleytechnologies.com"
    humidity = sense.get_humidity()
    temp = sense.get_temperature()*9/5 +32
    #accel = sense.get_accelerometer_raw()
	
    #print(accel)
    try:
        if urllib.request.urlopen(url, timeout = 5).getcode() != 200:
            await channel.send('The website is down')

    except urllib.error.URLError as e:
        await channel.send('The website is down')
        print(e)

    await channel.send('Humidity: {:.2f} % '.format(humidity))

    await channel.send('Temperature: {:.2f} F'.format(temp))

    

    if temp > 100:
        for person in dms:
        	await person.send( f'HIGH TEMPERATURES RECORDED: {temp}F')
	
    if humidity > 90:
        for person in dms:
        	await person.send( f'HIGH HUMIDITY RECORDED: {humidity}%')
	
    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    #urls for ping list
    urls = ["https://medleytechnologies.com", "https://ivygreeneacademy.com", "https://pool.medleytechnologies.com"]
    if '!website' in message.content.lower():
        ssl._create_default_https_context = ssl._create_unverified_context
	
        for url in urls:
            await message.channel.send('connecting to ' + url)
            try:
                if urllib.request.urlopen(url, timeout = 5).getcode() == 200:
                    await message.channel.send('The website is up')
                else:
                    await message.channel.send('The website is down')

            except urllib.error.URLError as e:
                await message.channel.send('The website is down')
            
    elif '!start' in message.content.lower():
        global channel
        channel = message.channel
        try:
            monitor.start()
            await message.channel.send('Started monitoring Medley Technology assets. ')
        except RuntimeError:
            await message.channel.send('Alreadying working ')
    elif '!stop' in message.content.lower():
        monitor.cancel()
        await message.channel.send('Stopped monitoring.')
        
    elif '!alertme' in message.content.lower():
        if not message.author in dms:
            dms.append(message.author)
            await message.author.send('You will now be alerted when the server catches fire.')

    elif '!ignoreme' in message.content.lower():
        try:
            dms.remove(message.author)
            await message.author.send('goodbye')
            await message.author.send('go fuck yourself')
        except ValueError:
            await channel.send('Out of spite, I will add you to spam list. beep boop I am a bot')
            dms.append(message.author)
            await message.author.send('You will now be alerted when the server catches fire.')


client.run(TOKEN)
