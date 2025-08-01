import discord
from discord.ext import commands
import logging
import os
import asyncio
from config import BOT_CONFIG

logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    """Main Discord bot class with enhanced functionality"""
    
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        # Initialize bot with slash command support
        super().__init__(
            command_prefix=BOT_CONFIG['prefix'],
            intents=intents,
            help_command=None,  # We'll create a custom help command
            case_insensitive=True,
            strip_after_prefix=True
        )
        
        # Store bot configuration
        self.config = BOT_CONFIG
        self.initial_cogs = [
            'cogs.utility',
            'cogs.moderation', 
            'cogs.fun',
            'cogs.server',
            'cogs.dm_manager'
        ]
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        logger.info("Setting up bot...")
        
        # Load all cogs
        for cog in self.initial_cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when the bot is ready and connected"""
        logger.info(f"{self.user} has connected to Discord!")
        logger.info(f"Bot is in {len(self.guilds)} guilds")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servers | /help"
        )
        await self.change_presence(activity=activity)
    
    async def on_guild_join(self, guild):
        """Called when the bot joins a new guild"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Update presence
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servers | /help"
        )
        await self.change_presence(activity=activity)
    
    async def on_guild_remove(self, guild):
        """Called when the bot leaves a guild"""
        logger.info(f"Left guild: {guild.name} (ID: {guild.id})")
        
        # Update presence
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(self.guilds)} servers | /help"
        )
        await self.change_presence(activity=activity)
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!")
        
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions to execute this command!")
        
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("❌ Member not found!")
        
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("❌ Channel not found!")
        
        else:
            logger.error(f"Unhandled error in command {ctx.command}: {error}")
            await ctx.send("❌ An unexpected error occurred. Please try again later.")
    
    async def on_app_command_error(self, interaction: discord.Interaction, error):
        """Global error handler for slash commands"""
        if isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command!", 
                ephemeral=True
            )
        
        elif isinstance(error, discord.app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                "❌ I don't have the required permissions to execute this command!", 
                ephemeral=True
            )
        
        else:
            logger.error(f"Unhandled error in slash command: {error}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ An unexpected error occurred. Please try again later.", 
                    ephemeral=True
                )
    
    async def close(self):
        """Clean shutdown of the bot"""
        logger.info("Shutting down bot...")
        await super().close()
