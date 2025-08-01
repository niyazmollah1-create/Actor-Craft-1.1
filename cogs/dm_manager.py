import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

class DMManager(commands.Cog):
    """DM management commands for sending and tracking direct messages"""
    
    def __init__(self, bot):
        self.bot = bot
        self.dm_channels_file = 'dm_channels.json'
        self.dm_channels = self.load_dm_channels()
    
    def load_dm_channels(self):
        """Load DM channel settings from file"""
        if os.path.exists(self.dm_channels_file):
            try:
                with open(self.dm_channels_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_dm_channels(self):
        """Save DM channel settings to file"""
        try:
            with open(self.dm_channels_file, 'w') as f:
                json.dump(self.dm_channels, f, indent=2)
        except Exception as e:
            print(f"Error saving DM channels: {e}")
    
    @app_commands.command(name="setchannel", description="Set this channel to receive DM replies")
    @app_commands.default_permissions(manage_guild=True)
    async def set_channel(self, interaction: discord.Interaction):
        """Set the current channel as the DM reply channel for this server"""
        guild_id = str(interaction.guild.id)
        channel_id = interaction.channel.id
        
        self.dm_channels[guild_id] = channel_id
        self.save_dm_channels()
        
        embed = discord.Embed(
            title="✅ DM Reply Channel Set",
            description=f"This channel ({interaction.channel.mention}) will now receive DM replies from users.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Usage",
            value="Use `/dm` to send DMs to users and `/dmall` to send DMs to all server members. "
                  "When users reply to the DMs, their responses will appear here.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="dm", description="Send a direct message to a user")
    @app_commands.describe(
        user="The user to send a DM to",
        message="The message to send"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def dm_user(self, interaction: discord.Interaction, user: discord.Member, message: str):
        """Send a DM to a specific user"""
        if len(message) > 2000:
            await interaction.response.send_message(
                "❌ Message is too long! Please keep it under 2000 characters.",
                ephemeral=True
            )
            return
        
        # Check if user is in the server
        if user not in interaction.guild.members:
            await interaction.response.send_message(
                "❌ This user is not in the server!",
                ephemeral=True
            )
            return
        
        # Don't DM bots
        if user.bot:
            await interaction.response.send_message(
                "❌ Cannot send DMs to bots!",
                ephemeral=True
            )
            return
        
        try:
            # Create DM embed
            dm_embed = discord.Embed(
                title=f"📬 Message from {interaction.guild.name}",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            dm_embed.add_field(
                name="Server",
                value=interaction.guild.name,
                inline=True
            )
            dm_embed.set_footer(text="Reply to this message to respond back to the server")
            
            # Send DM
            await user.send(embed=dm_embed)
            
            # Confirmation embed
            confirm_embed = discord.Embed(
                title="✅ DM Sent Successfully",
                description=f"Message sent to {user.mention}",
                color=discord.Color.green()
            )
            confirm_embed.add_field(name="Message", value=message[:500] + "..." if len(message) > 500 else message, inline=False)
            confirm_embed.add_field(name="Sent by", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=confirm_embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                f"❌ Could not send DM to {user.mention}. They may have DMs disabled or have blocked the bot.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while sending the DM: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="dmall", description="Send a direct message to all server members")
    @app_commands.describe(message="The message to send to all members")
    @app_commands.default_permissions(administrator=True)
    async def dm_all(self, interaction: discord.Interaction, message: str):
        """Send a DM to all members in the server"""
        if len(message) > 2000:
            await interaction.response.send_message(
                "❌ Message is too long! Please keep it under 2000 characters.",
                ephemeral=True
            )
            return
        
        # Defer the response since this might take a while
        await interaction.response.defer()
        
        guild = interaction.guild
        members = [member for member in guild.members if not member.bot]
        
        if len(members) == 0:
            await interaction.followup.send("❌ No members to send DMs to!")
            return
        
        # Confirmation before mass DM
        confirm_embed = discord.Embed(
            title="⚠️ Mass DM Confirmation",
            description=f"You are about to send a DM to **{len(members)}** members.\n\n"
                       f"**Message preview:**\n{message[:500]}{'...' if len(message) > 500 else ''}",
            color=discord.Color.orange()
        )
        confirm_embed.set_footer(text="This action cannot be undone. Use with caution.")
        
        await interaction.followup.send(embed=confirm_embed)
        
        # Send DMs
        successful = 0
        failed = 0
        
        dm_embed = discord.Embed(
            title=f"📬 Message from {guild.name}",
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        dm_embed.add_field(
            name="Server",
            value=guild.name,
            inline=True
        )
        dm_embed.set_footer(text="Reply to this message to respond back to the server")
        
        for member in members:
            try:
                await member.send(embed=dm_embed)
                successful += 1
            except:
                failed += 1
        
        # Send results
        result_embed = discord.Embed(
            title="📤 Mass DM Results",
            color=discord.Color.green() if failed == 0 else discord.Color.yellow()
        )
        result_embed.add_field(name="✅ Successful", value=str(successful), inline=True)
        result_embed.add_field(name="❌ Failed", value=str(failed), inline=True)
        result_embed.add_field(name="👥 Total Attempted", value=str(len(members)), inline=True)
        result_embed.add_field(name="Sent by", value=interaction.user.mention, inline=True)
        
        await interaction.followup.send(embed=result_embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen for DM replies and forward them to the designated channel"""
        # Only process DMs (not server messages)
        if message.guild is not None:
            return
        
        # Don't process bot messages
        if message.author.bot:
            return
        
        # Check if the user is in any servers with the bot
        for guild in self.bot.guilds:
            member = guild.get_member(message.author.id)
            if member:
                # Check if this guild has a DM channel set
                guild_id = str(guild.id)
                if guild_id in self.dm_channels:
                    channel_id = self.dm_channels[guild_id]
                    channel = guild.get_channel(channel_id)
                    
                    if channel:
                        # Create reply embed
                        reply_embed = discord.Embed(
                            title="💬 DM Reply Received",
                            description=message.content,
                            color=discord.Color.purple(),
                            timestamp=datetime.now()
                        )
                        reply_embed.add_field(
                            name="From",
                            value=f"{member.display_name} ({member.mention})",
                            inline=True
                        )
                        reply_embed.add_field(
                            name="User ID",
                            value=member.id,
                            inline=True
                        )
                        
                        # Set user avatar
                        reply_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
                        
                        # Handle attachments
                        if message.attachments:
                            attachment_list = []
                            for attachment in message.attachments:
                                attachment_list.append(f"[{attachment.filename}]({attachment.url})")
                            reply_embed.add_field(
                                name="📎 Attachments",
                                value="\n".join(attachment_list),
                                inline=False
                            )
                        
                        try:
                            await channel.send(embed=reply_embed)
                        except:
                            pass  # Channel might be deleted or bot lacks permissions
                
                break  # Found the user in a server, no need to check others

async def setup(bot):
    await bot.add_cog(DMManager(bot))