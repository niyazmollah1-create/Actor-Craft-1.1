
import discord
from discord.ext import commands
from discord import app_commands
import time
import platform
import psutil
import os
import asyncio
import aiohttp
from datetime import datetime, timedelta

class Utility(commands.Cog):
    """Utility commands for the Discord bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        """Check bot's latency and response time"""
        start_time = time.time()
        
        # Create initial embed
        embed = discord.Embed(
            title="🏓 Pong!",
            color=discord.Color.blue()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Calculate response time
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        # Update embed with latency information
        embed.add_field(
            name="WebSocket Latency",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=True
        )
        embed.add_field(
            name="Response Time",
            value=f"{round(response_time)}ms",
            inline=True
        )
        
        # Color based on latency
        if self.bot.latency * 1000 < 100:
            embed.color = discord.Color.green()
        elif self.bot.latency * 1000 < 200:
            embed.color = discord.Color.yellow()
        else:
            embed.color = discord.Color.red()
        
        await interaction.edit_original_response(embed=embed)
    
    @app_commands.command(name="info", description="Get information about the bot")
    async def info(self, interaction: discord.Interaction):
        """Display bot information and statistics"""
        # Calculate uptime
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        
        # Get system information
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        
        embed = discord.Embed(
            title="🤖 Bot Information",
            description="Here's some information about me!",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Bot stats
        embed.add_field(
            name="📊 Bot Stats",
            value=f"**Servers:** {len(self.bot.guilds)}\n"
                  f"**Users:** {len(self.bot.users)}\n"
                  f"**Commands:** {len(self.bot.tree.get_commands())}\n"
                  f"**Latency:** {round(self.bot.latency * 1000)}ms",
            inline=True
        )
        
        # System info
        embed.add_field(
            name="💻 System Info",
            value=f"**Python:** {platform.python_version()}\n"
                  f"**Discord.py:** {discord.__version__}\n"
                  f"**Platform:** {platform.system()}\n"
                  f"**CPU Usage:** {cpu_percent}%",
            inline=True
        )
        
        # Memory info
        embed.add_field(
            name="🧠 Memory Usage",
            value=f"**Used:** {round(memory.used / 1024**3, 2)} GB\n"
                  f"**Total:** {round(memory.total / 1024**3, 2)} GB\n"
                  f"**Percentage:** {memory.percent}%",
            inline=True
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help", description="Get help with bot commands")
    async def help(self, interaction: discord.Interaction):
        """Display help information for all commands"""
        embed = discord.Embed(
            title="📚 Bot Commands Help",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )
        
        # Utility Commands
        embed.add_field(
            name="🔧 Utility Commands",
            value="**/ping** - Check bot latency\n"
                  "**/info** - Bot information and stats\n"
                  "**/help** - Show this help message\n"
                  "**/uptime** - Check bot uptime\n"
                  "**/weather** - Get weather for a city\n"
                  "**/translate** - Translate text\n"
                  "**/remindme** - Set a reminder\n"
                  "**/say** - Make the bot say something\n"
                  "**/trigger** - Set automatic word responses",
            inline=False
        )
        
        # Moderation Commands
        embed.add_field(
            name="🛡️ Moderation Commands",
            value="**/kick** - Kick a member from the server\n"
                  "**/ban** - Ban a member from the server\n"
                  "**/unban** - Unban a member from the server\n"
                  "**/clear** - Clear messages from a channel\n"
                  "**/timeout** - Timeout a member",
            inline=False
        )
        
        # Fun Commands
        embed.add_field(
            name="🎮 Fun Commands",
            value="**/joke** - Get a random joke\n"
                  "**/quote** - Get an inspirational quote\n"
                  "**/roll** - Roll dice\n"
                  "**/coinflip** - Flip a coin\n"
                  "**/8ball** - Ask the magic 8-ball\n"
                  "**/choose** - Choose between options\n"
                  "**/fact** - Get a random fun fact\n"
                  "**/meme** - Get a programming meme\n"
                  "**/rps** - Play Rock Paper Scissors",
            inline=False
        )
        
        # Server Commands
        embed.add_field(
            name="🏠 Server Commands",
            value="**/userinfo** - Get information about a user\n"
                  "**/serverinfo** - Get server information\n"
                  "**/avatar** - Get user's avatar\n"
                  "**/roles** - List all server roles\n"
                  "**/membercount** - Detailed member statistics\n"
                  "**/channelinfo** - Get channel information",
            inline=False
        )
        
        # DM Commands
        embed.add_field(
            name="📬 DM Commands",
            value="**/setchannel** - Set channel for DM replies\n"
                  "**/dm** - Send DM to a specific user\n"
                  "**/dmall** - Send DM to all server members",
            inline=False
        )
        
        embed.set_footer(text="Use /command_name to execute a command")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="uptime", description="Check how long the bot has been running")
    async def uptime(self, interaction: discord.Interaction):
        """Display bot uptime information"""
        import psutil
        from datetime import timedelta
        
        # Get process start time
        process = psutil.Process()
        start_time = datetime.fromtimestamp(process.create_time())
        uptime_duration = datetime.now() - start_time
        
        # Format uptime
        days = uptime_duration.days
        hours, remainder = divmod(uptime_duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        embed = discord.Embed(
            title="⏱️ Bot Uptime",
            color=discord.Color.green()
        )
        embed.add_field(name="Current Uptime", value=uptime_str, inline=True)
        embed.add_field(name="Started At", value=f"<t:{int(start_time.timestamp())}:F>", inline=True)
        embed.add_field(name="Memory Usage", value=f"{round(process.memory_info().rss / 1024**2, 1)} MB", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="weather", description="Get weather information for a city")
    @app_commands.describe(city="The city to get weather for")
    async def weather(self, interaction: discord.Interaction, city: str):
        """Get weather information for a specified city"""
        try:
            # Using a free weather API (OpenWeatherMap alternative)
            async with aiohttp.ClientSession() as session:
                url = f"https://wttr.in/{city}?format=j1"
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        current = data['current_condition'][0]
                        
                        embed = discord.Embed(
                            title=f"🌤️ Weather in {city.title()}",
                            color=discord.Color.blue(),
                            timestamp=datetime.now()
                        )
                        
                        embed.add_field(
                            name="Temperature",
                            value=f"{current['temp_C']}°C / {current['temp_F']}°F",
                            inline=True
                        )
                        embed.add_field(
                            name="Feels Like",
                            value=f"{current['FeelsLikeC']}°C / {current['FeelsLikeF']}°F",
                            inline=True
                        )
                        embed.add_field(
                            name="Condition",
                            value=current['weatherDesc'][0]['value'],
                            inline=True
                        )
                        embed.add_field(
                            name="Humidity",
                            value=f"{current['humidity']}%",
                            inline=True
                        )
                        embed.add_field(
                            name="Wind",
                            value=f"{current['windspeedKmph']} km/h",
                            inline=True
                        )
                        embed.add_field(
                            name="Visibility",
                            value=f"{current['visibility']} km",
                            inline=True
                        )
                        
                        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                        
                        await interaction.response.send_message(embed=embed)
                        return
        except Exception as e:
            pass
        
        # Fallback message
        embed = discord.Embed(
            title="❌ Weather Service Unavailable",
            description=f"Sorry, I couldn't get weather information for '{city}'. Please try again later or check the city name.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="translate", description="Translate text to another language")
    @app_commands.describe(
        text="The text to translate",
        target_language="Target language (e.g., es, fr, de, ja, ko)"
    )
    async def translate(self, interaction: discord.Interaction, text: str, target_language: str):
        """Translate text using a translation API"""
        if len(text) > 500:
            await interaction.response.send_message(
                "❌ Text is too long! Please keep it under 500 characters.",
                ephemeral=True
            )
            return
        
        try:
            # Using a free translation API
            async with aiohttp.ClientSession() as session:
                url = "https://api.mymemory.translated.net/get"
                params = {
                    'q': text,
                    'langpair': f'auto|{target_language}'
                }
                async with session.get(url, params=params, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        translated_text = data['responseData']['translatedText']
                        
                        embed = discord.Embed(
                            title="🌐 Translation",
                            color=discord.Color.purple()
                        )
                        embed.add_field(name="Original", value=text, inline=False)
                        embed.add_field(name="Translated", value=translated_text, inline=False)
                        embed.add_field(name="Target Language", value=target_language.upper(), inline=True)
                        embed.set_footer(text=f"Translated for {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                        
                        await interaction.response.send_message(embed=embed)
                        return
        except Exception as e:
            pass
        
        # Fallback message
        embed = discord.Embed(
            title="❌ Translation Service Unavailable",
            description="Sorry, I couldn't translate the text right now. Please try again later.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="remindme", description="Set a reminder (up to 24 hours)")
    @app_commands.describe(
        duration="Duration in minutes (max 1440 for 24 hours)",
        reminder="What to remind you about"
    )
    async def remindme(self, interaction: discord.Interaction, duration: int, reminder: str):
        """Set a reminder for the user"""
        if duration < 1 or duration > 1440:  # Max 24 hours
            await interaction.response.send_message(
                "❌ Duration must be between 1 minute and 24 hours (1440 minutes)!",
                ephemeral=True
            )
            return
        
        if len(reminder) > 200:
            await interaction.response.send_message(
                "❌ Reminder text is too long! Please keep it under 200 characters.",
                ephemeral=True
            )
            return
        
        # Schedule the reminder
        remind_time = datetime.now() + timedelta(minutes=duration)
        
        embed = discord.Embed(
            title="⏰ Reminder Set",
            description=f"I'll remind you about: **{reminder}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Duration", value=f"{duration} minute{'s' if duration != 1 else ''}", inline=True)
        embed.add_field(name="Remind At", value=f"<t:{int(remind_time.timestamp())}:F>", inline=True)
        
        await interaction.response.send_message(embed=embed)
        
        # Wait for the specified duration
        await asyncio.sleep(duration * 60)
        
        # Send the reminder
        try:
            reminder_embed = discord.Embed(
                title="⏰ Reminder",
                description=f"You asked me to remind you about: **{reminder}**",
                color=discord.Color.gold()
            )
            reminder_embed.add_field(name="Set", value=f"<t:{int(datetime.now().timestamp() - duration * 60)}:R>", inline=True)
            
            await interaction.followup.send(f"{interaction.user.mention}", embed=reminder_embed)
        except:
            pass  # User might have left the server or disabled DMs
    
    @app_commands.command(name="say", description="Make the bot say something")
    @app_commands.describe(message="The message for the bot to say")
    @app_commands.default_permissions(manage_messages=True)
    async def say(self, interaction: discord.Interaction, message: str):
        """Make the bot say a message"""
        if len(message) > 2000:
            await interaction.response.send_message(
                "❌ Message is too long! Please keep it under 2000 characters.",
                ephemeral=True
            )
            return
        
        # Send the message
        await interaction.response.send_message(message)
    
    @app_commands.command(name="trigger", description="Set up automatic responses to specific words")
    @app_commands.describe(
        word="The word that will trigger a response",
        response="The response message when someone says the trigger word"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def trigger(self, interaction: discord.Interaction, word: str, response: str):
        """Set up automatic responses when users say specific words"""
        
        if len(word) > 50:
            await interaction.response.send_message(
                "❌ Trigger word is too long! Please keep it under 50 characters.",
                ephemeral=True
            )
            return
            
        if len(response) > 500:
            await interaction.response.send_message(
                "❌ Response is too long! Please keep it under 500 characters.",
                ephemeral=True
            )
            return
        
        # Store trigger in bot's memory (in a real bot, you'd use a database)
        if not hasattr(self.bot, 'triggers'):
            self.bot.triggers = {}
        
        guild_id = str(interaction.guild.id)
        if guild_id not in self.bot.triggers:
            self.bot.triggers[guild_id] = {}
            
        self.bot.triggers[guild_id][word.lower()] = response
        
        embed = discord.Embed(
            title="✅ Trigger Set",
            description=f"When someone says **{word}**, I'll respond with:\n> {response}",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Set by {interaction.user.display_name}")
        
        await interaction.response.send_message(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen for trigger words in messages"""
        # Don't respond to bots or DMs
        if message.author.bot or not message.guild:
            return
            
        # Check if bot has triggers set up
        if not hasattr(self.bot, 'triggers'):
            return
            
        guild_id = str(message.guild.id)
        if guild_id not in self.bot.triggers:
            return
            
        # Check message content for trigger words (exact word matching to avoid false triggers)
        message_content = message.content.lower()
        words = message_content.split()
        
        for trigger_word, response in self.bot.triggers[guild_id].items():
            # Check for exact word match or if trigger word is found in the message
            if trigger_word in words or trigger_word in message_content:
                await message.channel.send(response)
                return  # Only respond to the first trigger found and exit

async def setup(bot):
    await bot.add_cog(Utility(bot))
