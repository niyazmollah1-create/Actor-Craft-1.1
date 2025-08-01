import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Server(commands.Cog):
    """Server management and information commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="userinfo", description="Get information about a user")
    @app_commands.describe(member="The member to get information about (defaults to yourself)")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        """Display detailed information about a user"""
        if member is None:
            member = interaction.user
        
        # Get user information
        created_at = member.created_at
        joined_at = member.joined_at if hasattr(member, 'joined_at') else None
        
        embed = discord.Embed(
            title=f"👤 User Information - {member.display_name}",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Set user avatar
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Basic info
        embed.add_field(
            name="📝 Basic Info",
            value=f"**Username:** {member.name}\n"
                  f"**Display Name:** {member.display_name}\n"
                  f"**ID:** {member.id}\n"
                  f"**Bot:** {'Yes' if member.bot else 'No'}",
            inline=True
        )
        
        # Account dates
        embed.add_field(
            name="📅 Account Info",
            value=f"**Created:** <t:{int(created_at.timestamp())}:R>\n"
                  + (f"**Joined:** <t:{int(joined_at.timestamp())}:R>" if joined_at else "**Joined:** Not available"),
            inline=True
        )
        
        # Status and activity
        status_emoji = {
            discord.Status.online: "🟢",
            discord.Status.idle: "🟡",
            discord.Status.dnd: "🔴",
            discord.Status.offline: "⚫"
        }
        
        status_text = f"{status_emoji.get(member.status, '❓')} {member.status.name.title()}"
        
        # Get activity
        activity_text = "None"
        if member.activities:
            activity = member.activities[0]
            if isinstance(activity, discord.Game):
                activity_text = f"Playing {activity.name}"
            elif isinstance(activity, discord.Streaming):
                activity_text = f"Streaming {activity.name}"
            elif isinstance(activity, discord.Activity):
                activity_text = f"{activity.type.name.title()} {activity.name}"
        
        embed.add_field(
            name="💭 Status & Activity",
            value=f"**Status:** {status_text}\n"
                  f"**Activity:** {activity_text}",
            inline=True
        )
        
        # Roles (if member is from a guild)
        if hasattr(member, 'roles') and len(member.roles) > 1:
            roles = [role.mention for role in sorted(member.roles[1:], key=lambda r: r.position, reverse=True)]
            roles_text = ", ".join(roles[:10])  # Limit to 10 roles
            if len(member.roles) > 11:
                roles_text += f" and {len(member.roles) - 11} more..."
            
            embed.add_field(
                name=f"🎭 Roles ({len(member.roles) - 1})",
                value=roles_text,
                inline=False
            )
        
        # Permissions (if member is from a guild)
        if hasattr(member, 'guild_permissions'):
            key_perms = []
            perms = member.guild_permissions
            
            if perms.administrator:
                key_perms.append("Administrator")
            elif perms.manage_guild:
                key_perms.append("Manage Server")
            elif perms.manage_channels:
                key_perms.append("Manage Channels")
            elif perms.manage_messages:
                key_perms.append("Manage Messages")
            elif perms.kick_members:
                key_perms.append("Kick Members")
            elif perms.ban_members:
                key_perms.append("Ban Members")
            
            if key_perms:
                embed.add_field(
                    name="🔑 Key Permissions",
                    value=", ".join(key_perms),
                    inline=False
                )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        """Display detailed information about the server"""
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message(
                "❌ This command can only be used in a server!",
                ephemeral=True
            )
            return
        
        # Calculate member stats
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        
        # Get status counts
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])
        
        embed = discord.Embed(
            title=f"🏠 Server Information - {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Set server icon
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Basic server info
        embed.add_field(
            name="📝 Basic Info",
            value=f"**Name:** {guild.name}\n"
                  f"**ID:** {guild.id}\n"
                  f"**Owner:** {guild.owner.mention if guild.owner else 'Unknown'}\n"
                  f"**Created:** <t:{int(guild.created_at.timestamp())}:R>",
            inline=True
        )
        
        # Member statistics
        embed.add_field(
            name="👥 Members",
            value=f"**Total:** {total_members:,}\n"
                  f"**Humans:** {humans:,}\n"
                  f"**Bots:** {bots:,}",
            inline=True
        )
        
        # Status statistics
        embed.add_field(
            name="📊 Status",
            value=f"🟢 Online: {online:,}\n"
                  f"🟡 Idle: {idle:,}\n"
                  f"🔴 DND: {dnd:,}\n"
                  f"⚫ Offline: {offline:,}",
            inline=True
        )
        
        # Channel statistics
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed.add_field(
            name="📺 Channels",
            value=f"**Text:** {text_channels}\n"
                  f"**Voice:** {voice_channels}\n"
                  f"**Categories:** {categories}\n"
                  f"**Total:** {text_channels + voice_channels}",
            inline=True
        )
        
        # Server features
        features = []
        if guild.features:
            feature_names = {
                'COMMUNITY': 'Community Server',
                'PARTNERED': 'Partnered',
                'VERIFIED': 'Verified',
                'VANITY_URL': 'Vanity URL',
                'BANNER': 'Server Banner',
                'ANIMATED_ICON': 'Animated Icon',
                'DISCOVERABLE': 'Server Discovery'
            }
            features = [feature_names.get(f, f.replace('_', ' ').title()) for f in guild.features[:5]]
        
        embed.add_field(
            name="✨ Features",
            value="\n".join(features) if features else "None",
            inline=True
        )
        
        # Other info
        embed.add_field(
            name="🎭 Other",
            value=f"**Roles:** {len(guild.roles)}\n"
                  f"**Emojis:** {len(guild.emojis)}\n"
                  f"**Boost Level:** {guild.premium_tier}\n"
                  f"**Boosts:** {guild.premium_subscription_count or 0}",
            inline=True
        )
        
        # Server banner
        if guild.banner:
            embed.set_image(url=guild.banner.url)
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar", description="Get a user's avatar")
    @app_commands.describe(member="The member whose avatar to display (defaults to yourself)")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """Display a user's avatar in high quality"""
        if member is None:
            member = interaction.user
        
        embed = discord.Embed(
            title=f"🖼️ {member.display_name}'s Avatar",
            color=member.color if hasattr(member, 'color') and member.color != discord.Color.default() else discord.Color.blue()
        )
        
        # Get avatar URL
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        
        embed.set_image(url=avatar_url)
        
        # Add download links
        if member.avatar:
            embed.add_field(
                name="🔗 Download Links",
                value=f"[PNG]({member.avatar.with_format('png').url}) | "
                      f"[JPG]({member.avatar.with_format('jpg').url}) | "
                      f"[WEBP]({member.avatar.with_format('webp').url})",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roles", description="List all roles in the server")
    async def roles(self, interaction: discord.Interaction):
        """Display all roles in the server"""
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message(
                "❌ This command can only be used in a server!",
                ephemeral=True
            )
            return
        
        # Sort roles by position (highest first)
        roles = sorted(guild.roles[1:], key=lambda r: r.position, reverse=True)  # Exclude @everyone
        
        if not roles:
            await interaction.response.send_message(
                "❌ This server has no custom roles!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"🎭 Roles in {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Split roles into chunks to avoid embed limits
        role_chunks = [roles[i:i+20] for i in range(0, len(roles), 20)]
        
        for i, chunk in enumerate(role_chunks[:3]):  # Max 3 chunks (60 roles)
            role_list = []
            for role in chunk:
                member_count = len(role.members)
                role_list.append(f"{role.mention} - {member_count} member{'s' if member_count != 1 else ''}")
            
            field_name = f"Roles ({len(roles)} total)" if i == 0 else f"Roles (continued {i+1})"
            embed.add_field(
                name=field_name,
                value="\n".join(role_list),
                inline=False
            )
        
        if len(role_chunks) > 3:
            embed.add_field(
                name="Note",
                value=f"Only showing first 60 roles. Total roles: {len(roles)}",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="membercount", description="Get detailed member statistics")
    async def membercount(self, interaction: discord.Interaction):
        """Display detailed member count statistics"""
        guild = interaction.guild
        
        if not guild:
            await interaction.response.send_message(
                "❌ This command can only be used in a server!",
                ephemeral=True
            )
            return
        
        # Get member statistics
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        
        # Get status counts
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])
        
        embed = discord.Embed(
            title=f"📊 Member Statistics - {guild.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Member breakdown
        embed.add_field(
            name="👥 Total Members",
            value=f"**{total_members:,}** members\n"
                  f"**{humans:,}** humans\n"
                  f"**{bots:,}** bots",
            inline=True
        )
        
        # Status breakdown
        embed.add_field(
            name="📈 Status Breakdown",
            value=f"🟢 **{online:,}** online\n"
                  f"🟡 **{idle:,}** idle\n"
                  f"🔴 **{dnd:,}** do not disturb\n"
                  f"⚫ **{offline:,}** offline",
            inline=True
        )
        
        # Percentages
        if total_members > 0:
            human_percent = round((humans / total_members) * 100, 1)
            bot_percent = round((bots / total_members) * 100, 1)
            online_percent = round((online / total_members) * 100, 1)
            
            embed.add_field(
                name="📋 Percentages",
                value=f"**{human_percent}%** humans\n"
                      f"**{bot_percent}%** bots\n"
                      f"**{online_percent}%** online",
                inline=True
            )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="channelinfo", description="Get information about a channel")
    @app_commands.describe(channel="The channel to get information about (defaults to current channel)")
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Display detailed information about a channel"""
        if channel is None:
            channel = interaction.channel
        
        if not isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel)):
            await interaction.response.send_message(
                "❌ Invalid channel type!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=f"📺 Channel Information - {channel.name}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Basic info
        embed.add_field(
            name="📝 Basic Info",
            value=f"**Name:** {channel.name}\n"
                  f"**ID:** {channel.id}\n"
                  f"**Type:** {channel.type.name.replace('_', ' ').title()}\n"
                  f"**Created:** <t:{int(channel.created_at.timestamp())}:R>",
            inline=True
        )
        
        # Category and position
        if hasattr(channel, 'category') and channel.category:
            category_info = f"**Category:** {channel.category.name}\n"
        else:
            category_info = "**Category:** None\n"
        
        if hasattr(channel, 'position'):
            position_info = f"**Position:** {channel.position + 1}"
        else:
            position_info = "**Position:** N/A"
        
        embed.add_field(
            name="📍 Location",
            value=category_info + position_info,
            inline=True
        )
        
        # Description and topic
        if hasattr(channel, 'topic') and channel.topic:
            topic_text = channel.topic[:100] + "..." if len(channel.topic) > 100 else channel.topic
            embed.add_field(
                name="📋 Topic",
                value=topic_text,
                inline=False
            )
        
        # Additional info for text channels
        if isinstance(channel, discord.TextChannel):
            embed.add_field(
                name="⚙️ Settings",
                value=f"**NSFW:** {'Yes' if channel.nsfw else 'No'}\n"
                      f"**News:** {'Yes' if channel.is_news() else 'No'}\n"
                      f"**Slowmode:** {channel.slowmode_delay}s",
                inline=True
            )
        
        # Additional info for voice channels
        elif isinstance(channel, discord.VoiceChannel):
            embed.add_field(
                name="🔊 Voice Settings",
                value=f"**User Limit:** {channel.user_limit or 'Unlimited'}\n"
                      f"**Bitrate:** {channel.bitrate // 1000}kbps\n"
                      f"**Members:** {len(channel.members)}",
                inline=True
            )
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Server(bot))
