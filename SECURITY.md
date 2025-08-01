# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this Discord bot, please report it responsibly:

### How to Report

1. **Do not** open a public issue for security vulnerabilities
2. Email the maintainers directly or use GitHub's private vulnerability reporting
3. Include as much detail as possible:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### What to Expect

- **Response Time**: We aim to respond within 48 hours
- **Updates**: We'll keep you informed of our progress
- **Credit**: If you'd like, we'll acknowledge your contribution in the fix

### Security Best Practices

When using this bot:

1. **Protect Your Token**
   - Never commit your bot token to version control
   - Use environment variables or secure config files
   - Regenerate tokens if accidentally exposed

2. **Permissions**
   - Only grant necessary permissions to the bot
   - Regularly review and audit bot permissions
   - Use role hierarchy properly for moderation commands

3. **Server Security**
   - Keep your server software updated
   - Use proper file permissions
   - Monitor logs for suspicious activity

4. **Code Security**
   - Validate all user inputs
   - Use proper error handling
   - Keep dependencies updated

### Common Security Issues

- **Token Exposure**: Always use `.env` files and never commit tokens
- **Permission Escalation**: Ensure proper permission checks in commands
- **Input Validation**: Sanitize user inputs to prevent injection attacks
- **Rate Limiting**: Implement proper rate limiting to prevent abuse

## Scope

This security policy applies to:
- The main bot code and all cogs
- Configuration files and templates
- Documentation and setup guides

For questions about this policy, please open a discussion or contact the maintainers.