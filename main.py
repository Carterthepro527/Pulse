from ast import Return
from tokenize import Number
from winsound import PlaySound
import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import json
import os
import random
import sqlite3

client = commands.Bot(command_prefix = '=', case_insensitive=True, intents = discord.Intents.all())

@client.event
async def on_ready():
    print('--------------------')
    print('Bot currently online')
    print('--------------------')

    activity = discord.Activity(name="Commands: =help, =coin, =flip, =earth, =uno, =cute, =info, =roll, =user, ect", type=discord.ActivityType.playing)
    
    await client.change_presence(activity=activity)

    owner = await client.fetch_user(Your profile id here)
    Activeinfo=discord.Embed(title="Bot update info", description="Bot currently online", colour=discord.Colour.blue())
    Activeinfo.set_footer(text="Powerd by Nttl")
    await owner.send(embed=Activeinfo)

@client.event
async def on_member_join(member):
    print(f'<@!{member.id}> has joined a server')

@client.event
async def on_member_remove(member):
    print(f'<@!{member.id}> has left a server')

@client.event
async def on_command_error(ctx, error):
    Error=discord.Embed(title="error", description=error, colour=discord.Colour.blue())
    Error.set_footer(text="Powerd by Nttl")
    await ctx.send(embed=Error)

@client.command()
async def info(ctx):
    
    myEmbed = discord.Embed(title="Bot Info")
    myEmbed.add_field(name="Bot version:", value="v3.2.6", inline=False)
    myEmbed.add_field(name="Bot release date", value="October 7th, 2022", inline=False)
    myEmbed.set_footer(text="Powerd by Nttl")

    await ctx.message.channel.send(embed=myEmbed)

@client.command()
async def earth(ctx):
    
    myEarth = discord.Embed(title="Earth")
    myEarth.set_image(url="https://i.imgur.com/2SU1e23.jpeg")
    myEarth.set_footer(text="Powerd by Nttl")

    await ctx.message.channel.send(embed=myEarth)

@client.command()
async def cute(ctx):
    
    Cute = discord.Embed(title="Cuteness")
    Cute.set_image(url="https://i.imgur.com/znogT0z.jpg")
    Cute.set_footer(text="Powerd by Nttl")

    await ctx.message.channel.send(embed=Cute)

@client.command()
async def uno(ctx):
    
    UnoReverse = discord.Embed(title="Uno Reverse")
    UnoReverse.set_image(url="https://i.imgur.com/dgREloh.jpg")
    UnoReverse.set_footer(text="Powerd by Nttl")

    await ctx.message.channel.send(embed=UnoReverse)

@client.command()
async def user(ctx):

    role_names = ', '.join([role.name for role in ctx.author.roles if role.name != '@everyone'])

    user = discord.Embed(title = f'You executed this command in {ctx.guild.name}', color=discord.Colour.blue())
    user.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
    user.add_field(name="User ID:", value=f'{ctx.author.id}')
    user.add_field(name="Discord join date:", value=f'{ctx.author.created_at.year}, {ctx.author.created_at.month}, {ctx.author.created_at.day}')
    user.add_field(name="Server join date:", value=f'{ctx.author.joined_at.year}, {ctx.author.joined_at.month}, {ctx.author.joined_at.year}')
    user.add_field(name="Roles:", value=role_names)
    user.set_footer(text="Powerd by Nttl")
    await ctx.send(embed = user)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member):

    # Send an embed DM to the kicked user
    kickDM = discord.Embed(title = f'You have been kicked from {ctx.guild.name}', color=discord.Colour.blue())
    kickDM.add_field(name = 'Kicked by:', value = f'{ctx.author.name}', inline = False)
    kickDM.set_footer(text="Powerd by Nttl")
    await member.send(embed = kickDM)

    print("User Kicked")
    await member.kick(reason="Kicked")
    await ctx.send(f'Kicked {member.mention}')
    return

def is_connected(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@client.command()
async def songs(ctx):

    mySongs = discord.Embed(title="Songs that the =play command can play", color=discord.Colour.blue())
    mySongs.add_field(name="Songs:", value="1 Rickroll, 2 Fuck the world, 3 Blueberry Faygo, 4 Toxic boy with uke, 5 Royalty free stream music", inline=False)
    mySongs.set_footer(text="Powerd by Nttl")

    await ctx.message.channel.send(embed=mySongs)

@client.command()
async def advertisement(ctx):

    Yez = discord.Embed(title="Advertisement")
    Yez.add_field(name="Please add me to your server:", value="Your discord bot invite here", inline=False)
    Yez.set_footer(text="Powerd by Nttl")

    await ctx.message.author.send(embed=Yez)

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Audio Paused")
    else:
        await ctx.send("No audio currently playing")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Audio resumed")
    else:
        await ctx.send("Audio is not paused")

@client.command()
async def ping(ctx):
    latency = client.latency
    await ctx.message.channel.send(f'Pong! Latency is {latency} seconds.')

@client.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

# Connect to the database
conn = sqlite3.connect('ban_table.db')

# Create a cursor
cursor = conn.cursor()

# Create the ban table
cursor.execute('''CREATE TABLE IF NOT EXISTS ban_table (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    ban_reason TEXT
                    )''')

@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def ban(ctx, member : discord.Member, *, reason="Reason not specified"):
    # Check if the user is already in the ban table
    cursor.execute('''SELECT * FROM ban_table WHERE user_id = ?''', (member.id,))
    result = cursor.fetchone()

    if result:
        # Update the ban reason for the user
        cursor.execute('''UPDATE ban_table SET ban_reason = ? WHERE user_id = ?''', (reason, member.id))
        conn.commit()
    else:
        # Add the member's information to the ban table
        cursor.execute('''INSERT INTO ban_table (user_id, username, ban_reason)
                        VALUES (?, ?, ?)''', (member.id, member.name, reason))
        conn.commit()

    # Embed to send to banned user
    banembed = discord.Embed(title = f"You were banned from {ctx.guild.name}", color=discord.Colour.blue())
    banembed.add_field(name="Banned", value=f"Reason banned: {reason}")
    banembed.set_footer(text="Powerd by Nttl")
    await member.send(embed=banembed)

    await member.ban(reason="Banned")

    banembed2 = discord.Embed(title = "Ban Info", color=discord.Colour.blue())
    banembed2.add_field(name="Banned", value=f"Member banned: {member.mention}, Reason banned: {reason}, Server banned from: {ctx.guild.name}")
    banembed2.set_footer(text="Powerd by Nttl")
    await ctx.send(embed=banembed2)
    return

@client.command()
async def searchban(ctx):
    # Get all the banned users from the ban_table
    cursor.execute('''SELECT * FROM ban_table''')
    banned_users = cursor.fetchall()
    ban_table_embed = discord.Embed(title = "Ban Info", color=discord.Colour.blue())
    ban_table_embed.add_field(name="Ban Results:", value=f"{banned_users}")
    ban_table_embed.set_footer(text="Powerd by Digital Python")
    await ctx.send(embed=ban_table_embed)

@client.command()
async def unban(ctx, *, user: discord.User):
    # Unban the user
    await ctx.guild.unban(user)

    unbanembed = discord.Embed(title = "Unban Info", color=discord.Colour.blue())
    unbanembed.add_field(name="Unbanned", value=f"Member unbanned: {user}, Server unbanned from {ctx.guild.name}")
    unbanembed.set_footer(text="Powerd by Nttl")
    await ctx.send(embed=unbanembed)

    # Delete the user's information from the ban_table
    cursor.execute('''DELETE FROM ban_table WHERE user_id=?''', (user.id,))
    conn.commit()

@client.command()
async def removeban(ctx, *, user: discord.User):
# Remove the user from the ban list
    # Delete the user's information from the ban_table
    cursor.execute('''DELETE FROM ban_table WHERE user_id=?''', (user.id,))
    conn.commit()

    removeban = discord.Embed(title = "Ban list info", color=discord.Colour.blue())
    removeban.add_field(name="Removed Ban", value=f"Member's ban that was removed: {user}, Server ban was removed from {ctx.guild.name}")
    removeban.set_footer(text="Powerd by Nttl")
    await ctx.send(embed=removeban)

@client.command()
@commands.has_permissions(administrator=True)
async def role(ctx, user : discord.Member, *, role :discord.Role):

    if role in user.roles:
        await ctx.send(f"{user.mention} already has the role, {role}")
        print("User already has that role")
    else:
        await user.add_roles(role)
        await ctx.send(f"Added {role} to {user.mention}")
        print("Role added")

@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, user : discord.Member, *, role :discord.Role):

    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"Removed {role} from {user.mention}")
        print("Role removed")
    else:
        await ctx.send(f"{user.mention} does not have the role {role}")
        print("Dosen't have role")

@client.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Cleared messages", delete_after=4.0)

@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send( ctx.channel.mention + " is now in lockdown.")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " has been unlocked.")

@client.command()
async def roll(ctx, num_sides: int = 10):
    dice_roll = random.randint(1, num_sides)
    await ctx.send(f'You rolled a {dice_roll}!')

@client.command()
async def flip(ctx):
    result = random.choice(['heads', 'tails'])
    await ctx.send(f'The coin landed on {result}!')

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    # Store the user's previous roles
    previous_roles = member.roles.copy()
    # Get the mute role
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    # Tell the member that they are muted
    MuteInfo1=discord.Embed(title="Mute info", description=f'You have been muted in {ctx.guild.name}.', colour=discord.Colour.blue())
    MuteInfo1.set_footer(text="Powerd by Nttl")
    await member.send(embed=MuteInfo1)
    # Update the member's roles to add the mute role
    await member.edit(roles=[mute_role])
    # Send a message to the channel
    MuteInfo=discord.Embed(title="Mute info", description=f'{member} has been muted.', colour=discord.Colour.blue())
    MuteInfo.add_field(name="Reason:", value=f'{reason}')
    MuteInfo.set_footer(text="Powerd by Nttl")
    await ctx.send(embed=MuteInfo)
    # Store the user's new roles in a dictionary with their ID as the key
    client.muted_users[member.id] = {'previous_roles': previous_roles, 'current_roles': member.roles}

# Create an empty dictionary to store muted users
client.muted_users = {}

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    # Check if the user is in the muted_users dictionary
    if member.id in client.muted_users:
        # Get the user's previous roles
        previous_roles = client.muted_users[member.id]['previous_roles']
        # Update the member's roles to restore their previous roles
        await member.edit(roles=previous_roles)
        # Send a message to the user
        UnMuteInfo1=discord.Embed(title="Mute info", description=f'You have been unmuted in {ctx.guild.name}.', colour=discord.Colour.blue())
        UnMuteInfo1.set_footer(text="Powerd by Nttl")
        await member.send(embed=UnMuteInfo1)
        # Send a message to the channel
        UnMuteInfo=discord.Embed(title="Mute info", description=f'{member} has been unmuted.', colour=discord.Colour.blue())
        UnMuteInfo.set_footer(text="Powerd by Nttl")
        await ctx.send(embed=UnMuteInfo)
        # Remove the user from the muted_users dictionary
        del client.muted_users[member.id]
    else:
        await ctx.send(f'{member} is not currently muted.')

@client.command()
async def randomname(ctx):
    await ctx.send(f'If you get the name "JIMMY BOB JOE" well then you lucky boi')
    # Create a list of first names
    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Greta', 'Henry', 'JIMMY BOB']
    # Create a list of last names
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'JOE']
    # Generate a random name
    name = random.choice(first_names) + ' ' + random.choice(last_names)
    # Send the name to the channel
    await ctx.send(f'Your random name is: {name}')

client.run('Discord bot token here')
