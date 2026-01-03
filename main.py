import discord as dis
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

s_role = "Lion 🦁"

handle = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = dis.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    sWords = ["shit", "fuck", "bitch", "cunt", "bullshit", "dogshit"]

    for word in sWords:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} - Dont use that word please.")

    await bot.process_commands(message)

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = dis.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎🏼")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hey {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = dis.utils.get(ctx.guild.roles, name=s_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {s_role}")
    else:
        await ctx.send("Role doesnt exist.")

@bot.command()
async def remove(ctx):
    role = dis.utils.get(ctx.guild.roles, name=s_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {s_role} removed.")
    else:
        await ctx.send("Role doesnt exist.")

@bot.command()
@commands.has_role(s_role)
async def secret(ctx):
    await ctx.send("Welcome to the Club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

bot.run(token, log_handler=handle, log_level=logging.DEBUG)



