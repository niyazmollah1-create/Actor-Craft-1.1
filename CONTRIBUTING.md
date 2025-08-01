# Contributing to Multi-Purpose Discord Bot

Thank you for your interest in contributing to this Discord bot project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Basic knowledge of Discord.py
- Understanding of async/await programming
- A Discord account for testing

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/discord-bot.git
   cd discord-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r github_requirements.txt
   ```

3. **Set up your bot token**
   ```bash
   cp .env.example .env
   # Edit .env and add your bot token
   ```

4. **Test the bot**
   ```bash
   python main.py
   ```

## 📋 How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/discord-bot/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Bot logs (if relevant)

### Suggesting Features

1. Check [Discussions](https://github.com/yourusername/discord-bot/discussions) for similar ideas
2. Create a new discussion with:
   - Clear description of the feature
   - Use cases and benefits
   - Implementation suggestions (if any)

### Code Contributions

1. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   - Ensure the bot starts without errors
   - Test new commands thoroughly
   - Verify existing functionality still works

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/amazing-feature
   ```

## 🎯 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Use type hints where appropriate

```python
async def example_command(interaction: discord.Interaction, user: discord.Member) -> None:
    """
    Example command that demonstrates proper style.
    
    Args:
        interaction: The Discord interaction object
        user: The target user
    """
    # Your code here
```

### Cog Organization

- Place related commands in the same cog
- Use descriptive cog names and docstrings
- Keep cogs focused on a single responsibility

```python
class ExampleCog(commands.Cog):
    """Cog for example commands and functionality"""
    
    def __init__(self, bot):
        self.bot = bot
```

### Error Handling

- Always handle potential errors gracefully
- Provide meaningful error messages to users
- Log errors for debugging purposes

```python
try:
    # Your code here
    await interaction.response.send_message("Success!")
except discord.Forbidden:
    await interaction.response.send_message("I don't have permission to do that.", ephemeral=True)
except Exception as e:
    logging.error(f"Error in command: {e}")
    await interaction.response.send_message("An error occurred.", ephemeral=True)
```

### Command Design

- Use slash commands for all new commands
- Include helpful descriptions and parameter hints
- Set appropriate permissions
- Use embeds for rich responses

```python
@app_commands.command(name="example", description="An example command")
@app_commands.describe(user="The user to target")
async def example(self, interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title="Example", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Bot starts without errors
- [ ] All commands respond correctly
- [ ] Error handling works as expected
- [ ] Permissions are properly enforced
- [ ] No console errors during normal operation

### Testing New Features

1. Test the happy path (normal usage)
2. Test edge cases and error conditions
3. Test with different permission levels
4. Verify the feature works in different servers

## 📝 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include parameter descriptions and return types
- Explain complex logic with comments

### README Updates

- Update command tables for new commands
- Add usage examples for new features
- Update setup instructions if needed

## 🏷️ Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tested manually
- [ ] All existing features still work
- [ ] Added appropriate error handling

## Screenshots (if applicable)
Add screenshots of new commands or features
```

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Focus on the code, not the person

## 📞 Getting Help

If you need help with contributing:

1. Check the [Discussions](https://github.com/yourusername/discord-bot/discussions) page
2. Look at existing code for examples
3. Ask questions in your pull request
4. Join the Discord.py community for general help

## 🎉 Recognition

Contributors will be acknowledged in:
- GitHub contributors list
- README acknowledgments section
- Release notes for significant contributions

Thank you for contributing to make this Discord bot better! 🚀