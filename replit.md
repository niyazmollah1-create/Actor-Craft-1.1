# Overview

A multi-purpose Discord bot built with Python and discord.py that provides utility, moderation, fun, server management, and DM management commands. The bot uses slash commands for modern Discord interactions and includes features like kick/ban moderation, dice rolling, joke fetching, user information display, server statistics, comprehensive DM messaging system with reply tracking, custom bot messages, and triggered responses. The architecture follows a cog-based design pattern for modular command organization.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Discord.py Library**: Uses discord.py with slash commands support for modern Discord API interactions
- **Cog-Based Architecture**: Commands are organized into separate modules (cogs) for utility, moderation, fun, and server management
- **Async/Await Pattern**: All operations use asynchronous programming for non-blocking execution

## Configuration Management
- **Centralized Config**: Bot settings, API endpoints, colors, and rate limits are managed in a central config.py file
- **Environment Variables**: Sensitive data like Discord tokens are stored in environment variables with dotenv support
- **Structured Settings**: Configuration includes embed colors, API endpoints for external services, rate limiting parameters, and logging settings

## Command Structure
- **Slash Commands**: All user-facing commands use Discord's slash command system via app_commands
- **Permission Checks**: Moderation commands include proper permission validation and role hierarchy checks
- **Error Handling**: Commands include comprehensive error handling for permission issues and API failures

## External API Integration
- **HTTP Client**: Uses aiohttp for async HTTP requests to external APIs
- **Fallback Data**: Local fallback data for quotes and jokes when external APIs are unavailable
- **API Endpoints**: Configured endpoints for jokes, quotes, and facts services

## Logging and Monitoring
- **Structured Logging**: Comprehensive logging system with file and console output
- **Log Rotation**: Configurable log file rotation with size limits and backup counts
- **Performance Monitoring**: Latency tracking and response time measurement built into utility commands

## Security and Permissions
- **Role Hierarchy**: Moderation commands respect Discord's role hierarchy and permission system
- **Input Validation**: User inputs are validated for safety and proper formatting
- **Rate Limiting**: Built-in rate limiting configuration to prevent abuse

# External Dependencies

## Core Dependencies
- **discord.py**: Main Discord API wrapper library for bot functionality
- **aiohttp**: Async HTTP client for external API requests
- **python-dotenv**: Environment variable management for configuration
- **psutil**: System information gathering for bot statistics

## External APIs
- **Official Joke API** (official-joke-api.appspot.com): Provides random jokes for fun commands
- **Quotable API** (api.quotable.io): Supplies inspirational quotes
- **Useless Facts API** (uselessfacts.jsph.pl): Source for random facts

## Discord Platform
- **Discord Gateway**: Real-time communication with Discord servers
- **Discord Slash Commands**: Modern command interface requiring application registration
- **Discord Permissions System**: Integrated with bot's moderation features for proper access control