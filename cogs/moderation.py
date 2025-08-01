import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import asyncio

class Moderation(commands.Cog):
    """Moderation commands for server management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.describe(
        member="The member to kick",
        reason="Reason for kicking the member"
    )
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Kick a member from the server"""
        # Check if user can kick the target
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You cannot kick someone with a higher or equal role!",
                ephemeral=True
            )
            return
        
        # Check if bot can kick the target
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "❌ I cannot kick someone with a higher or equal role than me!",
                ephemeral=True
            )
            return
        
        # Cannot kick the guild owner
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ I cannot kick the server owner!",
                ephemeral=True
            )
            return
        
        try:
            # Try to DM the user before kicking
            try:
                dm_embed = discord.Embed(
                    title="You have been kicked",
                    description=f"You have been kicked from **{interaction.guild.name}**",
                    color=discord.Color.red()
                )
                dm_embed.add_field(name="Reason", value=reason, inline=False)
                dm_embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
                await member.send(embed=dm_embed)
            except:
                pass  # User has DMs disabled
            
            # Kick the member
            await member.kick(reason=f"Kicked by {interaction.user} - {reason}")
            
            # Send confirmation
            embed = discord.Embed(
                title="✅ Member Kicked",
                description=f"{member.mention} has been kicked from the server",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to kick this member!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while kicking the member: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.describe(
        member="The member to ban",
        reason="Reason for banning the member",
        delete_days="Number of days of messages to delete (0-7)"
    )
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided", delete_days: int = 0):
        """Ban a member from the server"""
        # Validate delete_days parameter
        if delete_days < 0 or delete_days > 7:
            await interaction.response.send_message(
                "❌ Delete days must be between 0 and 7!",
                ephemeral=True
            )
            return
        
        # Check if user can ban the target
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You cannot ban someone with a higher or equal role!",
                ephemeral=True
            )
            return
        
        # Check if bot can ban the target
        if member.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message(
                "❌ I cannot ban someone with a higher or equal role than me!",
                ephemeral=True
            )
            return
        
        # Cannot ban the guild owner
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ I cannot ban the server owner!",
                ephemeral=True
            )
            return
        
        try:
            # Try to DM the user before banning
            try:
                dm_embed = discord.Embed(
                    title="You have been banned",
                    description=f"You have been banned from **{interaction.guild.name}**",
                    color=discord.Color.red()
                )
                dm_embed.add_field(name="Reason", value=reason, inline=False)
                dm_embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
                await member.send(embed=dm_embed)
            except:
                pass  # User has DMs disabled
            
            # Ban the member
            await member.ban(
                reason=f"Banned by {interaction.user} - {reason}",
                delete_message_days=delete_days
            )
            
            # Send confirmation
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned from the server",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.add_field(name="Messages Deleted", value=f"{delete_days} days", inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to ban this member!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while banning the member: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.describe(
        user_id="The ID of the user to unban",
        reason="Reason for unbanning the user"
    )
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "No reason provided"):
        """Unban a user from the server"""
        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)
            
            # Check if user is actually banned
            ban_entry = None
            async for ban in interaction.guild.bans():
                if ban.user.id == user_id:
                    ban_entry = ban
                    break
            
            if not ban_entry:
                await interaction.response.send_message(
                    "❌ This user is not banned from the server!",
                    ephemeral=True
                )
                return
            
            # Unban the user
            await interaction.guild.unban(user, reason=f"Unbanned by {interaction.user} - {reason}")
            
            # Send confirmation
            embed = discord.Embed(
                title="✅ Member Unbanned",
                description=f"{user.mention} has been unbanned from the server",
                color=discord.Color.green()
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            
            await interaction.response.send_message(embed=embed)
            
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid user ID provided!",
                ephemeral=True
            )
        except discord.NotFound:
            await interaction.response.send_message(
                "❌ User not found!",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to unban members!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while unbanning the user: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="clear", description="Clear messages from the channel")
    @app_commands.describe(
        amount="Number of messages to delete (1-100)",
        member="Only delete messages from this member"
    )
    @app_commands.default_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int, member: discord.Member = None):
        """Clear messages from the channel"""
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "❌ Amount must be between 1 and 100!",
                ephemeral=True
            )
            return
        
        try:
            await interaction.response.defer(ephemeral=True)
            
            if member:
                # Delete messages from specific member
                def check(message):
                    return message.author == member
                
                deleted = await interaction.channel.purge(limit=amount * 2, check=check)
                deleted_count = len(deleted)
                
                embed = discord.Embed(
                    title="🧹 Messages Cleared",
                    description=f"Deleted {deleted_count} messages from {member.mention}",
                    color=discord.Color.green()
                )
            else:
                # Delete any messages
                deleted = await interaction.channel.purge(limit=amount)
                deleted_count = len(deleted)
                
                embed = discord.Embed(
                    title="🧹 Messages Cleared",
                    description=f"Deleted {deleted_count} messages",
                    color=discord.Color.green()
                )
            
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.add_field(name="Channel", value=interaction.channel.mention, inline=True)
            
            await interaction.followup.send(embed=embed)
            
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ I don't have permission to delete messages!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ An error occurred while clearing messages: {str(e)}",
                ephemeral=True
            )
    
    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.describe(
        member="The member to timeout",
        duration="Duration in minutes",
        reason="Reason for the timeout"
    )
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "No reason provided"):
        """Timeout a member for a specified duration"""
        if duration < 1 or duration > 40320:  # Max 28 days
            await interaction.response.send_message(
                "❌ Duration must be between 1 minute and 28 days (40320 minutes)!",
                ephemeral=True
            )
            return
        
        # Check if user can timeout the target
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message(
                "❌ You cannot timeout someone with a higher or equal role!",
                ephemeral=True
            )
            return
        
        # Cannot timeout the guild owner
        if member == interaction.guild.owner:
            await interaction.response.send_message(
                "❌ I cannot timeout the server owner!",
                ephemeral=True
            )
            return
        
        try:
            # Calculate timeout duration
            timeout_until = datetime.now() + timedelta(minutes=duration)
            
            # Apply timeout
            await member.timeout(timeout_until, reason=f"Timed out by {interaction.user} - {reason}")
            
            # Send confirmation
            embed = discord.Embed(
                title="⏰ Member Timed Out",
                description=f"{member.mention} has been timed out",
                color=discord.Color.orange()
            )
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            embed.add_field(name="Until", value=f"<t:{int(timeout_until.timestamp())}:F>", inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=interaction.user.mention, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to timeout this member!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ An error occurred while timing out the member: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(Moderation(bot))
