import os
import discord
from discord.ext import commands
from time import localtime,strftime
import asyncio
import ast
import psutil
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


started_bef = False

file = open("config.txt","r")
config = ast.literal_eval(file.read())
file.close()

bot = commands.Bot(command_prefix="!",description="")
bot.remove_command('help')

@bot.event
async def on_ready():
  global started_bef
  if started_bef == True:
    print("Bot Restarted.")
    pass
  else:
    started_bef = True
    print("Started!")
    await start()




#@bot.command()
async def generate(ctx,*,time):
  fname = await gen_graph(time)
  file = open(f"{fname}","rb")
  await ctx.send(file=discord.File(fp=file))
  file.close()

async def start():
  if True:
        tn = strftime("%Y-%m-%d %H:%M", localtime())
        file = open("tempdata.txt","w")
        file.write(tn)
        file.close()
        tn = strftime("%Y-%m-%d %H:%M", localtime())
        file = open("tempdata_2.txt","w")
        file.write(tn)
        file.close()
  local_10m = {}
  print("Log Start")
  #start logging CPU
  global data_cpu
  i10m_mins = 0
  cpu_chart = []
  cpu_chart_hourly = []
  sec = 0
  cpu_chart_sec = 0
  while True:
    cpu = psutil.cpu_percent()
    sec += 1
    cpu_chart.append(cpu)
    cpu_chart_hourly.append(cpu)
    if sec == 2:
      sec = 0
      #System Logger
      #timenow = strftime("%Y-%m-%d %H:%M", localtime())
      #data_cpu[timenow] = cpu
      #update_data()
      #Local Loggers
      timenow = strftime("%H:%M",localtime())
      local_10m[timenow] = cpu
      i10m_mins += 1
    await asyncio.sleep(30)
    cpu_chart_sec += 30
    if i10m_mins == 10: ##default value 10
      i10_mins = 0
      #Generate Graph
      await gen_graph(local_10m)
      # os.unlink(f"{timenow}")
      # Reset
      local_10m = {}
    if cpu_chart_sec % 3600 == 0: #default value 3600
      if cpu_chart_sec == 43200:
        #Every 12 hours reset
        await gen_graph(cpu_chart)
        cpu_chart_sec = 0 
        tn = strftime("%Y-%m-%d %H:%M", localtime())
        file = open("tempdata.txt","w")
        file.write(tn)
        file.close()
        cpu_chart = []
        print("Reset")
      #Hourly
      else:
        await gen_graph(cpu_chart)
      #After that, generate the standard hourly graph.
      await gen_graph2(cpu_chart_hourly)
      tn = strftime("%Y-%m-%d %H:%M", localtime())
      file = open("tempdata_2.txt","w")
      file.write(tn)
      file.close()
      cpu_chart_hourly = []
      print("Reset")
        
async def gen_graph2(data):
      #Data is a dict where Value:x Axis, Key:y Axis
      # Return file name
      # If data is a list, list format must be ["StartTime",*percentages]
      if isinstance(data,list):
        #List of CPU Values to process in graph
        # The returned (sent) graph should be one where X asis only has start (list[0]) and end (timenow) values
        # Time now (LIST START) should be DD-MM-YY HH:MM
        # Do not process first data in passed list.
        file = open("tempdata_2.txt","r")
        start_time = file.read()
        file.close()
        y_axis = data
        x_axis = [start_time]
        for x in range(len(data)-2):
          x_axis.append(" "*x)
        tn = strftime("%m-%d_%H:%M", localtime())
        tn2 = strftime("%Y-%m-%d %H:%M", localtime())
        x_axis.append(f"{tn2}")
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(x_axis, y_axis, label='CPU Usage (%)')
        ave = sum(y_axis)/len(y_axis)
        hr = (len(y_axis)/2)/60
        plt.title(f'CPU Utilisation (Average = {str(ave)}, Time = {str(hr)} Hours)')
        ax.legend()
        #fn = f'graphs/{timenow}.png'
        fn = f'sent/{tn}.png'
        fig.savefig(fn)
        member = bot.get_user(config.get("USERID"))
        file = open(fn,"rb")
        await member.send(file=discord.File(fp=file))
        file.close()
             

async def gen_graph(data):
      #Data is a dict where Value:x Axis, Key:y Axis
      # Return file name
      # If data is a list, list format must be ["StartTime",*percentages]
      if isinstance(data,dict):
        y_keys = []
        x_keys = []
        for key, value in data.items():
          y_keys.append(key)
          x_keys.append(value)
        timenow = strftime("%m%d %H%M", localtime())
        timenow2 = strftime("%Y-%m-%d", localtime())
        
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(y_keys, x_keys, label='CPU Usage (%)')
        plt.title('CPU Utilisation')
        ax.legend()
        #fn = f'graphs/{timenow}.png'
        fn = f'graphs/{timenow}.png'
        fig.savefig(fn)
        print("New Graph Added")
        #member = bot.get_user(config.get("USERID"))
        #file = open(fn,"rb")
        #await member.send(file=discord.File(fp=file))
        #file.close()
        return True
      if isinstance(data,list):
        #List of CPU Values to process in graph
        # The returned (sent) graph should be one where X asis only has start (list[0]) and end (timenow) values
        # Time now (LIST START) should be DD-MM-YY HH:MM
        # Do not process first data in passed list.
        file = open("tempdata.txt","r")
        start_time = file.read()
        file.close()
        y_axis = data
        x_axis = [start_time]
        for x in range(len(data)-2):
          x_axis.append(" "*x)
        tn = strftime("%m-%d_%H:%M", localtime())
        tn2 = strftime("%Y-%m-%d %H:%M", localtime())
        x_axis.append(f"{tn2}")
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(x_axis, y_axis, label='CPU Usage (%)')
        ave = sum(y_axis)/len(y_axis)
        hr = (len(y_axis)/2)/60
        plt.title(f'CPU Utilisation (Average = {str(ave)}, Time = {str(hr)} Hours)')
        ax.legend()
        #fn = f'graphs/{timenow}.png'
        fn = f'sent/{tn}.png'
        fig.savefig(fn)
        member = bot.get_user(config.get("USERID"))
        file = open(fn,"rb")
        await member.send(file=discord.File(fp=file))
        file.close()
        
      
  











async def start_legacy():
  local = {}
  #start logging CPU
  global data_cpu
  mins = 0
  while True:
    timenow = strftime("%Y-%m-%d %H:%M", localtime())
    data_cpu[timenow] = psutil.cpu_percent()
    timenow = strftime("%H:%M",localtime())
    local[timenow] = psutil.cpu_percent()
    update_data()
    print("Updated")
    await asyncio.sleep(60)
    mins += 1
    if mins == 2:
      mins = 0
      #Generate Graph
      y_keys = []
      for key, value in local.items():
        y_keys.append(key)
      x_keys = []
      for key, value in local.items():
        x_keys.append(value)
      trace = go.Scatter(
         x = y_keys,
         y = x_keys
         )
      timenow = strftime("%Y-%m-%d %H:%M", localtime())
      data = [trace]
      fig = go.Figure()
      # py.plot(data, filename=f'{timenow}')
      fig.add_scatter(x=y_keys,y=x_keys);plot(fig)
      if not os.path.exists('images'):
        os.mkdir('images')
      pio.write_image(fig, f'images/{timenow}.jpeg')
      member = bot.get_user(config.get("USERID"))
      file = open(f"images/{timenow}","rb")
      await member.send(file=discord.File(fp=file))
      file.close()
      os.unlink(f"{timenow}")
      # Reset
      # local = {}


def update_data():
  file = open("data.txt","w")
  file.write(str(data_cpu))
  file.close()

bot.run(config.get("TOKEN"))
