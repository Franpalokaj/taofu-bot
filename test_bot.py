import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True  # Add this to read server messages

bot = commands.Bot(command_prefix='!taofu', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print(f'Bot prefix: {bot.command_prefix}')
    print(f'Available commands: {[cmd.name for cmd in bot.commands]}')

@bot.command(name='test')
async def test_command(ctx):
    """Test command to see if commands work"""
    print(f"Test command triggered by {ctx.author.name}!")
    await ctx.send("Test command works! 🎉")

@bot.command(name='ping')
async def ping_command(ctx):
    """Simple ping command"""
    print(f"Ping command triggered by {ctx.author.name}!")
    await ctx.send("Pong! 🏓")

@bot.event
async def on_message(message):
    """Handle all messages for debugging"""
    # Don't respond to our own messages
    if message.author == bot.user:
        return
    
    # Print message for debugging
    print(f"Received message: '{message.content}' from {message.author.name} in {message.channel.type}")
    
    # Let Discord.py handle command processing naturally
    try:
        await bot.process_commands(message)
        print("Command processing completed")
    except Exception as e:
        print(f"Error processing commands: {e}")
        import traceback
        traceback.print_exc()

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    print(f"Command error: {error}")
    if isinstance(error, commands.CommandNotFound):
        print(f"Command not found: {ctx.message.content}")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"Missing argument: {error}")
    else:
        print(f"Other error: {error}")
        import traceback
        traceback.print_exc()

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables")
        exit(1)
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"Error starting bot: {e}") 