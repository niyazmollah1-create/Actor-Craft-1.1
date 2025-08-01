import discord
from discord.ext import commands
from discord import app_commands
import random
import aiohttp
import json

class Fun(commands.Cog):
    """Fun commands for entertainment"""
    
    def __init__(self, bot):
        self.bot = bot
        
        # 8-ball responses
        self.eight_ball_responses = [
            "🎱 It is certain",
            "🎱 It is decidedly so",
            "🎱 Without a doubt",
            "🎱 Yes definitely",
            "🎱 You may rely on it",
            "🎱 As I see it, yes",
            "🎱 Most likely",
            "🎱 Outlook good",
            "🎱 Yes",
            "🎱 Signs point to yes",
            "🎱 Reply hazy, try again",
            "🎱 Ask again later",
            "🎱 Better not tell you now",
            "🎱 Cannot predict now",
            "🎱 Concentrate and ask again",
            "🎱 Don't count on it",
            "🎱 My reply is no",
            "🎱 My sources say no",
            "🎱 Outlook not so good",
            "🎱 Very doubtful"
        ]
        
        # Inspirational quotes (fallback)
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
            "The purpose of our lives is to be happy. - Dalai Lama",
            "Life is really simple, but we insist on making it complicated. - Confucius",
            "The only thing necessary for the triumph of evil is for good men to do nothing. - Edmund Burke",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        ]
        
        # Jokes (fallback)
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't programmers like nature? It has too many bugs!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus!",
            "Why did the bicycle fall over? Because it was two tired!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!"
        ]
    
    @app_commands.command(name="joke", description="Get a random joke")
    async def joke(self, interaction: discord.Interaction):
        """Get a random joke from an API or fallback list"""
        try:
            # Try to get joke from API
            async with aiohttp.ClientSession() as session:
                async with session.get('https://official-joke-api.appspot.com/random_joke', timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        joke_text = f"{data['setup']}\n\n||{data['punchline']}||"
                        
                        embed = discord.Embed(
                            title="😂 Random Joke",
                            description=joke_text,
                            color=discord.Color.gold()
                        )
                        await interaction.response.send_message(embed=embed)
                        return
        except:
            pass  # Fall back to local jokes
        
        # Fallback to local jokes
        joke_text = random.choice(self.jokes)
        embed = discord.Embed(
            title="😂 Random Joke",
            description=joke_text,
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="quote", description="Get an inspirational quote")
    async def quote(self, interaction: discord.Interaction):
        """Get an inspirational quote from an API or fallback list"""
        try:
            # Try to get quote from API
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.quotable.io/random', timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        quote_text = f'"{data["content"]}" - {data["author"]}'
                        
                        embed = discord.Embed(
                            title="💭 Inspirational Quote",
                            description=quote_text,
                            color=discord.Color.purple()
                        )
                        await interaction.response.send_message(embed=embed)
                        return
        except:
            pass  # Fall back to local quotes
        
        # Fallback to local quotes
        quote_text = random.choice(self.quotes)
        embed = discord.Embed(
            title="💭 Inspirational Quote",
            description=f'"{quote_text}"',
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roll", description="Roll dice")
    @app_commands.describe(
        sides="Number of sides on the dice (default: 6)",
        count="Number of dice to roll (default: 1)"
    )
    async def roll(self, interaction: discord.Interaction, sides: int = 6, count: int = 1):
        """Roll dice with specified sides and count"""
        if sides < 2:
            await interaction.response.send_message(
                "❌ Dice must have at least 2 sides!",
                ephemeral=True
            )
            return
        
        if sides > 1000:
            await interaction.response.send_message(
                "❌ Dice cannot have more than 1000 sides!",
                ephemeral=True
            )
            return
        
        if count < 1:
            await interaction.response.send_message(
                "❌ Must roll at least 1 die!",
                ephemeral=True
            )
            return
        
        if count > 20:
            await interaction.response.send_message(
                "❌ Cannot roll more than 20 dice at once!",
                ephemeral=True
            )
            return
        
        # Roll the dice
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)
        
        embed = discord.Embed(
            title="🎲 Dice Roll",
            color=discord.Color.blue()
        )
        
        if count == 1:
            embed.description = f"You rolled a **{rolls[0]}** on a {sides}-sided die!"
        else:
            rolls_str = ", ".join(map(str, rolls))
            embed.description = f"You rolled: {rolls_str}"
            embed.add_field(name="Total", value=f"**{total}**", inline=True)
            embed.add_field(name="Dice", value=f"{count}d{sides}", inline=True)
        
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        """Flip a coin and get heads or tails"""
        result = random.choice(["Heads", "Tails"])
        emoji = "🪙" if result == "Heads" else "🥇"
        
        embed = discord.Embed(
            title=f"{emoji} Coin Flip",
            description=f"The coin landed on **{result}**!",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Flipped by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    @app_commands.describe(question="The question you want to ask")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        """Ask the magic 8-ball a question"""
        if len(question) < 3:
            await interaction.response.send_message(
                "❌ Please ask a proper question!",
                ephemeral=True
            )
            return
        
        response = random.choice(self.eight_ball_responses)
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=response, inline=False)
        embed.set_footer(text=f"Asked by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="choose", description="Let the bot choose between options")
    @app_commands.describe(options="Options separated by commas (e.g., 'option1, option2, option3')")
    async def choose(self, interaction: discord.Interaction, options: str):
        """Choose randomly between provided options"""
        # Split options by comma and clean them
        choices = [option.strip() for option in options.split(',') if option.strip()]
        
        if len(choices) < 2:
            await interaction.response.send_message(
                "❌ Please provide at least 2 options separated by commas!",
                ephemeral=True
            )
            return
        
        if len(choices) > 20:
            await interaction.response.send_message(
                "❌ Please provide no more than 20 options!",
                ephemeral=True
            )
            return
        
        chosen = random.choice(choices)
        
        embed = discord.Embed(
            title="🤔 Choice Made",
            description=f"I choose: **{chosen}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Options", value=", ".join(choices), inline=False)
        embed.set_footer(text=f"Chosen for {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="fact", description="Get a random fun fact")
    async def fact(self, interaction: discord.Interaction):
        """Get a random fun fact from an API or fallback list"""
        try:
            # Try to get fact from API
            async with aiohttp.ClientSession() as session:
                async with session.get('https://uselessfacts.jsph.pl/random.json?language=en', timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        fact_text = data['text']
                        
                        embed = discord.Embed(
                            title="🧠 Random Fact",
                            description=fact_text,
                            color=discord.Color.orange()
                        )
                        await interaction.response.send_message(embed=embed)
                        return
        except:
            pass  # Fall back to local facts
        
        # Fallback facts
        facts = [
            "Bananas are berries, but strawberries aren't!",
            "Octopuses have three hearts and blue blood.",
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old.",
            "A group of flamingos is called a 'flamboyance'.",
            "Wombat poop is cube-shaped.",
            "There are more possible games of chess than there are atoms in the observable universe.",
            "Butterflies taste with their feet.",
            "A shrimp's heart is in its head.",
            "Elephants are afraid of bees.",
            "The shortest war in history lasted only 38-45 minutes."
        ]
        
        fact_text = random.choice(facts)
        embed = discord.Embed(
            title="🧠 Random Fact",
            description=fact_text,
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="meme", description="Get a random programming meme")
    async def meme(self, interaction: discord.Interaction):
        """Get a random programming meme from Reddit API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://meme-api.com/gimme/programmerhumor', timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        embed = discord.Embed(
                            title=data.get('title', 'Programming Meme'),
                            color=discord.Color.blurple(),
                            url=data.get('postLink', '')
                        )
                        embed.set_image(url=data.get('url', ''))
                        embed.set_footer(text=f"👍 {data.get('ups', 0)} upvotes | r/{data.get('subreddit', 'programmerhumor')}")
                        
                        await interaction.response.send_message(embed=embed)
                        return
        except:
            pass
        
        # Fallback message
        embed = discord.Embed(
            title="😅 Meme Service Unavailable",
            description="Sorry, I couldn't fetch a meme right now. Try again later!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rps", description="Play Rock Paper Scissors with the bot")
    @app_commands.describe(choice="Your choice: rock, paper, or scissors")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors")
    ])
    async def rock_paper_scissors(self, interaction: discord.Interaction, choice: app_commands.Choice[str]):
        """Play Rock Paper Scissors with the bot"""
        user_choice = choice.value.lower()
        bot_choice = random.choice(['rock', 'paper', 'scissors'])
        
        # Determine winner
        if user_choice == bot_choice:
            result = "It's a tie!"
            color = discord.Color.yellow()
            emoji = "🤝"
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            result = "You win!"
            color = discord.Color.green()
            emoji = "🎉"
        else:
            result = "You lose!"
            color = discord.Color.red()
            emoji = "😔"
        
        # Emojis for choices
        choice_emojis = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
        
        embed = discord.Embed(
            title=f"{emoji} Rock Paper Scissors",
            description=f"**{result}**",
            color=color
        )
        embed.add_field(name="Your Choice", value=f"{choice_emojis[user_choice]} {user_choice.title()}", inline=True)
        embed.add_field(name="My Choice", value=f"{choice_emojis[bot_choice]} {bot_choice.title()}", inline=True)
        embed.set_footer(text=f"Played by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
