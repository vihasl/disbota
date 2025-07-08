import discord
from discord.ext import commands
import time
import sys
from datetime import datetime
from collections import defaultdict



# Store last reply date for each user
user_last_reply = defaultdict(lambda: None)


# Track bot start time
start_time = time.time()

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True
intents.guilds = True
intents.members = True

# Create bot
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# DM command
@bot.command()
async def dm(ctx, member: discord.Member, *, message):
    try:
        await member.send(message)
        await ctx.send(f"✅ DM sent to {member.name}")
    except discord.Forbidden:
        await ctx.send("❌ Cannot send DM to this user. They may have DMs disabled.")

# User info command
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"User Info - {member}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=False)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(
        name="Roles",
        value=", ".join([role.name for role in member.roles if role.name != "@everyone"]),
        inline=False
    )

    await ctx.send(embed=embed)

# Poll command
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(
        title="📊 New Poll",
        description=question,
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Poll started by {ctx.author.name}")
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("✅")
    await poll_message.add_reaction("❌")

# Uptime command
@bot.command()
async def uptime(ctx):
    now = time.time()
    delta = int(now - start_time)
    hours, remainder = divmod(delta, 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="⏱ Bot Uptime",
        description=f"{hours}h {minutes}m {seconds}s",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

# Handle direct messages to bot
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id
        today = datetime.utcnow().date()

        try:
            sys.stdout.buffer.write(f"📥 DM from {message.author}: {message.content}\n".encode('utf-8'))
        except Exception as e:
            print(f"Failed to print DM: {e}")

        # ✅ Forward to your log channel
        log_channel_id = 1259857750163325049  # Replace with your actual channel ID
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="New DM Received",
                description=message.content,
                color=discord.Color.red()
            )
            embed.set_footer(text=f"From: {message.author} (ID: {message.author.id})")
            await log_channel.send(embed=embed)

        # ✅ Reply only once per day per user
        if user_last_reply[user_id] != today:
            user_last_reply[user_id] = today
            await message.channel.send(
                "Thanks for your message! We'll get back to you soon. "
                "ඔබගේ පණිවුඩයට ස්තූතියි. කරුණාකර මදක් රැදී සිටින්න."
            )

    await bot.process_commands(message)


# Start the bot (keep your token private!)
bot.run('MTM5MTY5ODgwODI0ODg2NDg2OQ.G0eX3-.Lh101JQlYivm1opisNJ9qhoJo9Awr6-e9IZDlU')
