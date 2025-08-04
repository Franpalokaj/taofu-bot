import discord
from discord.ext import commands
import openai
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True  # Add this to read server messages

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# OpenAI configuration
openai.api_key = os.getenv('OPENAI_API_KEY')
print(f"OpenAI API Key loaded: {'Yes' if openai.api_key else 'No'}")
if not openai.api_key:
    print("WARNING: No OpenAI API key found! Bot will not be able to respond to questions.")

# Load knowledge base
def load_knowledge_base():
    try:
        with open('knowledge.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Taofu is a decentralized ecosystem. Visit taofu.xyz for more information."

# Load system instructions
def load_system_instructions():
    try:
        with open('system_instructions.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """You are the official Taofu ecosystem assistant. You help people learn about the Taofu ecosystem and provide accurate information based on the official documentation.

IMPORTANT RULES:
1. Only answer questions based on the provided Taofu knowledge base
2. Never make up numbers, technical details, or tokenomics information
3. If you're unsure about something, admit it and direct users to taofu.xyz
4. Be concise and helpful
5. Always mention you're the official Taofu assistant
6. Encourage users to visit taofu.xyz for more information"""

KNOWLEDGE_BASE = load_knowledge_base()
SYSTEM_INSTRUCTIONS = load_system_instructions()

# Analytics logging
def log_question(user_id, username, question, response_preview, platform="Discord"):
    try:
        with open('analytics.json', 'r') as f:
            analytics = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        analytics = []
    
    analytics.append({
        'timestamp': datetime.now().isoformat(),
        'user_id': str(user_id),
        'username': username,
        'question': question,
        'response_preview': response_preview[:100] + "..." if len(response_preview) > 100 else response_preview,
        'platform': platform
    })
    
    with open('analytics.json', 'w') as f:
        json.dump(analytics, f, indent=2)

# System prompt for OpenAI
SYSTEM_PROMPT = f"""{SYSTEM_INSTRUCTIONS}

TAOFU KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

Remember: If asked about specific technical details, tokenomics, or information not covered in the knowledge base, direct users to taofu.xyz for the most current and accurate information."""

async def get_ai_response(question):
    """Get response from OpenAI API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm having trouble connecting to my knowledge base right now. Please try again later or visit taofu.xyz for information."

def split_message(message, max_length=2000):
    """Split long messages to fit Discord's character limit"""
    if len(message) <= max_length:
        return [message]
    
    parts = []
    while message:
        if len(message) <= max_length:
            parts.append(message)
            break
        else:
            # Find the last space within the limit
            split_point = message.rfind(' ', 0, max_length)
            if split_point == -1:
                split_point = max_length
            
            parts.append(message[:split_point])
            message = message[split_point:].lstrip()
    
    return parts

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    print(f'Bot prefix: {bot.command_prefix}')
    print(f'Available commands: {[cmd.name for cmd in bot.commands]}')
    
    # Test command registration
    for cmd in bot.commands:
        print(f"Command '{cmd.name}' registered with aliases: {cmd.aliases}")
        print(f"Command '{cmd.name}' help: {cmd.help}")
    
    # Debug intents
    print(f"Intents: guilds={bot.intents.guilds}, guild_messages={bot.intents.guild_messages}, message_content={bot.intents.message_content}")
    
    # Set bot status
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="taofu.xyz"
    ))

@bot.command(name='test')
async def test_command(ctx):
    """Test command to see if commands work"""
    print(f"Test command triggered by {ctx.author.name}!")
    try:
        await ctx.send("Test command works! 🎉")
        print("Test message sent successfully!")
    except Exception as e:
        print(f"Error sending test message: {e}")
        await ctx.send("Test command failed!")

@bot.command(name='ping')
async def ping_command(ctx):
    """Simple ping command"""
    print(f"Ping command triggered by {ctx.author.name}!")
    print(f"Ping command context: guild={ctx.guild}, channel={ctx.channel}")
    await ctx.send("Pong! 🏓")

@bot.command(name='ask')
async def ask_question(ctx, *, question):
    """Ask a question about the Taofu ecosystem"""
    print(f"Ask command triggered by {ctx.author.name}: {question}")
    if not question.strip():
        await ctx.send("Please provide a question! Use `!taofu ask <your question>`")
        return
    
    # Show typing indicator
    print("Getting AI response...")
    async with ctx.typing():
        try:
            # Get AI response
            response = await get_ai_response(question)
            print(f"AI response received: {response[:100]}...")
            
            # Log the question
            log_question(
                user_id=ctx.author.id,
                username=ctx.author.name,
                question=question,
                response_preview=response,
                platform="Discord"
            )
            
            # Split response if too long
            message_parts = split_message(response)
            
            # Send response
            for i, part in enumerate(message_parts):
                if i == 0:
                    embed = discord.Embed(
                        title="🤖 Taofu Assistant",
                        description=part,
                        color=0x00ff00
                    )
                    embed.set_footer(text=f"Asked by {ctx.author.name}")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(part)
                    
        except Exception as e:
            print(f"Error processing question: {e}")
            await ctx.send("Sorry, I encountered an error. Please try again later or visit taofu.xyz for information.")

@bot.command(name='taofu_help')
async def help_command(ctx):
    """Show help information"""
    print(f"Help command triggered by {ctx.author.name}")
    try:
        embed = discord.Embed(
            title="🤖 Taofu Assistant Help",
            description="I'm here to help you learn about the Taofu ecosystem!",
            color=0x00ff00
        )
        
        embed.add_field(
            name="Commands",
            value="""`!ask <question>` - Ask me anything about Taofu
`!taofu_help` - Show this help message""",
            inline=False
        )
        
        embed.add_field(
            name="Example Questions",
            value="""• What is Taofu?
• How can I participate in the ecosystem?
• Where can I find more information?
• What are the community resources?""",
            inline=False
        )
        
        embed.add_field(
            name="Important",
            value="For the most current and accurate information, always visit **taofu.xyz**",
            inline=False
        )
        
        embed.set_footer(text="Official Taofu Assistant")
        print("Sending help embed...")
        await ctx.send(embed=embed)
        print("Help embed sent successfully!")
    except Exception as e:
        print(f"Error in help command: {e}")
        await ctx.send("Sorry, I encountered an error. Please try again later.")

@bot.event
async def on_message(message):
    """Handle basic messages and let Discord.py handle commands"""
    # Don't respond to our own messages
    if message.author == bot.user:
        return
    
    # Enhanced diagnostic logging
    print(f"on_message: author={message.author}, guild={message.guild}, channel={message.channel}, content={message.content!r}")
    print(f"Channel type: {message.channel.type}")
    print(f"Guild: {message.guild.name if message.guild else 'DM'}")
    
    # Test if bot can send messages
    if message.content.lower() == "test":
        try:
            await message.channel.send("Bot is working! 🎉")
            print("Successfully sent test message")
        except Exception as e:
            print(f"Error sending message: {e}")
            import traceback
            traceback.print_exc()
    
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
        # Only respond to commands that start with our prefix
        if ctx.message.content.startswith(bot.command_prefix):
            await ctx.send("Unknown command. Use `!taofu taofu_help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"Missing argument: {error}")
        await ctx.send("Please provide all required arguments. Use `!taofu taofu_help` for more information.")
    else:
        print(f"Other error: {error}")
        import traceback
        traceback.print_exc()
        await ctx.send("An error occurred. Please try again later.")

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