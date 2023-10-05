# Full code for Eos Discord bot with Notification System
# This code assumes that the bot has permissions to read and send messages in multiple channels or servers.

# Importing the required libraries
import discord
from discord.ext import commands, tasks

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store user profiles and opt-in status
user_profiles = {}
opt_in_users = set()

# Mock project database
projects = [
    {"name": "Climate Change Data Analysis", "skills": ["Python", "Data Science"]},
    {"name": "E-commerce Platform", "skills": ["JavaScript", "React"]},
    {"name": "Machine Learning for Healthcare", "skills": ["Python", "Machine Learning"]},
]

# Bot ready event
@bot.event
async def on_ready():
    print(f"Eos bot is ready. Username: {bot.user.name}, ID: {bot.user.id}")

# Start command to authenticate user
@bot.command()
async def start(ctx):
    await ctx.author.send("Welcome to Eos! Please authenticate with your GitHub account.")
    await ctx.author.send("Enter your GitHub username:")

# Handle GitHub username and profile setup
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        github_username = message.content
        user_profiles[message.author.id] = {"github_username": github_username}
        await message.channel.send(f"Thanks, {github_username}! Now, please list your skills (e.g., Python, JavaScript).")

    await bot.process_commands(message)

# Set user skills and find matching projects
@bot.command()
async def set_skills(ctx, *, skills):
    skills_list = skills.split(", ")
    user_profiles[ctx.author.id]["skills"] = skills_list
    await ctx.author.send("Skills updated! Now discovering projects for you...")

    matching_projects = [project for project in projects if any(skill in skills_list for skill in project["skills"])]

    if matching_projects:
        await ctx.author.send("Here are some projects that match your skills:")
        for project in matching_projects:
            await ctx.author.send(f"- {project['name']} (Skills: {', '.join(project['skills'])})")
    else:
        await ctx.author.send("No matching projects found. Please update your skills or check back later.")

# Join a project and create a new Discord channel for it
@bot.command()
async def join_project(ctx, *, project_name):
    project = next((project for project in projects if project["name"].lower() == project_name.lower()), None)

    if project:
        guild = ctx.guild
        channel = await guild.create_text_channel(project_name.replace(" ", "-").lower())
        await ctx.author.send(f"You've joined {project_name}! A new Discord channel has been created for collaboration.")
    else:
        await ctx.author.send("Project not found. Please enter a valid project name.")

# Opt-in for notifications
@bot.command()
async def opt_in(ctx):
    opt_in_users.add(ctx.author.id)
    await ctx.author.send("You've opted in for project notifications.")

# Send a notification (for demonstration, this will send a DM to all opt-in users)
@bot.command()
async def send_notification(ctx, *, message):
    for user_id in opt_in_users:
        user = await bot.fetch_user(user_id)
        await user.send(f"Project Notification: {message}")

# Uncomment the line below when running this in your local environment
# bot.run('YOUR_DISCORD_BOT_TOKEN')
