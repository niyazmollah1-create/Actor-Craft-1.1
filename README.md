# 🤖 Multi-Purpose Discord Bot

<p align="center">
  <img src="https://img.shields.io/badge/discord.py-2.5.2-blue.svg">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img src="https://img.shields.io/github/license/yourusername/discord-bot">
  <img src="https://img.shields.io/badge/status-active-success.svg">
</p>

*A comprehensive Discord bot built with Python and discord.py featuring utility commands, moderation tools, fun interactions, server management, and advanced DM messaging system with reply tracking.*

## ✨ Features

- 🔧 **Moderation Tools** - Kick, ban, timeout, and member management
- 🎮 **Fun Commands** - Dice rolling, jokes, quotes, facts, and games
- 📊 **Server Management** - User info, server stats, member counts, role management
- 🛠️ **Utility Commands** - Ping, help, channel info, and system monitoring
- 📬 **DM Management** - Send individual/broadcast DMs with automatic reply forwarding
- ⚡ **Slash Commands** - Modern Discord interactions with auto-complete
- 🏗️ **Modular Design** - Organized cog-based architecture for easy maintenance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Discord bot token
- Basic knowledge of Discord bots

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/discord-bot.git
   cd discord-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r github_requirements.txt
   ```

3. **Configure your bot:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## 📋 Commands Overview

### 🔧 Moderation Commands
| Command | Description | Permissions Required |
|---------|-------------|---------------------|
| `/kick` | Kick a member from the server | Kick Members |
| `/ban` | Ban a member from the server | Ban Members |
| `/timeout` | Timeout a member | Moderate Members |
| `/clear` | Delete multiple messages | Manage Messages |

### 🎮 Fun Commands
| Command | Description |
|---------|-------------|
| `/roll` | Roll dice with custom sides |
| `/joke` | Get a random joke |
| `/quote` | Get an inspirational quote |
| `/fact` | Get a random fact |
| `/rps` | Play Rock Paper Scissors |

### 📊 Server & Utility Commands
| Command | Description |
|---------|-------------|
| `/userinfo` | Get information about a user |
| `/serverinfo` | Get server information |
| `/avatar` | Get user's avatar |
| `/membercount` | Detailed member statistics |
| `/ping` | Check bot latency |
| `/help` | Show all available commands |
| `/say` | Make the bot say something |
| `/trigger` | Set automatic word responses |

### 📬 DM Management Commands
| Command | Description | Permissions Required |
|---------|-------------|---------------------|
| `/setchannel` | Set channel for DM replies | Manage Guild |
| `/dm` | Send DM to a specific user | Manage Messages |
| `/dmall` | Send DM to all server members | Administrator |

## 🛠️ Setup Guide

### Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Copy the token and add it to your `.env` file
5. Enable necessary intents:
   - Message Content Intent
   - Server Members Intent (for member commands)

### Bot Permissions

Your bot needs these permissions:
- Send Messages
- Use Slash Commands
- Read Message History
- Manage Messages (for moderation)
- Kick Members (for kick command)
- Ban Members (for ban command)
- Moderate Members (for timeout)

### Invite Your Bot

Use this invite link (replace `YOUR_BOT_ID` with your bot's client ID):
```
https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=1513965750&scope=bot%20applications.commands
```

## 🏗️ Project Structure

```
├── main.py              # Bot entry point
├── bot.py               # Main bot class
├── config.py            # Configuration settings
├── cogs/                # Command modules
│   ├── utility.py       # Utility commands
│   ├── moderation.py    # Moderation commands
│   ├── fun.py           # Fun commands
│   ├── server.py        # Server management
│   └── dm_manager.py    # DM system
├── .env.example         # Environment template
├── github_requirements.txt # Dependencies
└── README.md            # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:
```env
DISCORD_TOKEN=your_bot_token_here
```

### Bot Configuration

The bot configuration is managed in `config.py`:
- Embed colors
- API endpoints for external services
- Rate limiting settings
- Logging configuration

## 🔧 Technical Information

### Built With
- **Python 3.8+**
- **discord.py 2.5+** - Modern Discord API wrapper
- **aiohttp** - Async HTTP requests
- **python-dotenv** - Environment variable management
- **psutil** - System monitoring

### Key Features
- **Async/Await Pattern** - Non-blocking execution
- **Cog-Based Architecture** - Modular command organization
- **Slash Commands** - Modern Discord interactions
- **Error Handling** - Comprehensive error management
- **Persistent Storage** - JSON-based data persistence for DM channels
- **External API Integration** - Jokes, quotes, and facts from external APIs

## 📖 Usage Examples

### DM Management System

1. **Set up DM replies:**
   ```
   /setchannel
   ```

2. **Send individual DM:**
   ```
   /dm @user Hello! This is a message from the server.
   ```

3. **Send broadcast DM:**
   ```
   /dmall Important server announcement for all members!
   ```

4. **Automatic Reply Forwarding:**
   When users reply to the DMs, their responses automatically appear in your designated channel with user information and message content.

### Moderation Examples

```
/kick @user Spamming in chat
/ban @user Inappropriate behavior
/timeout @user 1h Breaking server rules
/clear 10
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/discord-bot.git

# Install dependencies
pip install -r github_requirements.txt

# Run the bot
python main.py
```

### Coding Standards
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Organize commands in appropriate cogs

## 📞 Support

- 🐛 [Report Issues](https://github.com/yourusername/discord-bot/issues)
- 💡 [Feature Requests](https://github.com/yourusername/discord-bot/discussions)

## 🔗 Useful Links

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs/)
- [Discord.py Discord Server](https://discord.gg/dpy)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - The Python Discord API wrapper
- External API providers for jokes, quotes, and facts
- Discord.py community for guidance and support

## ⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ on GitHub!

---

*Ready to get started? Follow the setup guide above and have your bot running in minutes!*
