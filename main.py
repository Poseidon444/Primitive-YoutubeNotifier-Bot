import discord
from discord.ext import commands
import os
import json
import requests
import time as t
import xmltodict

def get(element:str,file:str):
    path = os.path.abspath(file)
    with open(path,"r") as read_file:
        content = json.load(read_file)
        main = content[element]
    return main

def write(element:str,file:str):
    path = os.path.abspath(file)
    with open(path,"w") as write_file:
        json.dump(element,write_file)

client = commands.Bot(command_prefix = get("prefix","./bot.json"))

@client.event
async def on_ready():
  print(f"logged on as {client.user}")
  print("working")
  while True:
      t.sleep(60)
      channel = get("channel","./config.json")
      print(channel)
      ctx = client.get_channel(int(channel))
      req = requests.get("https://www.youtube.com/feeds/videos.xml?channel_id="+get("id","./config.json"))
      if req.status_code != 200:
          print("Invalid channel id!")
          return None
      channel_data = xmltodict.parse(req.text)
      Data = channel_data.get('feed', None)
      videoid = Data.get('entry')[0]['yt:videoId']
      channelname = get("channelname","./config.json")
      url = f"https://www.youtube.com/watch?v={videoid}"
      dictionary = {"latestvideo":url}
      if os.stat("./latestvid.json").st_size == 0:
        write(dictionary,"./latestvid.json")
      elif url == get("latestvideo","./latestvid.json"):
        pass
      elif url != get("latestvideo","./latestvid.json"):
        write(dictionary,"./latestvid.json")
        await ctx.send(f"{channelname} has posted! a New video {url}")

@client.command()
async def ping(ctx):
  await ctx.send(f"My ping is {round(client.latency*1000)}ms")

client.run(get("token","./bot.json"))
