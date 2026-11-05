# ====================================================================
#  DO NOT REMOVE THESE LINES
# © 2026 the-awesome-noob
# Licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)
# Contact: @theawesomenoob_ on Discord
# You can edit this code all you want, but don't claim it as your own.
# ====================================================================
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import random
import os
import json
from typing import Optional

intents = discord.Intents.default()
intents.message_content = True

class NoobBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time: Optional[datetime] = None

    async def setup_hook(self):
        await self.tree.sync()

bot = NoobBot(command_prefix="!", intents=intents)

bread_lock = asyncio.Lock()

def _read_bread_file():
    if os.path.exists("bread.json"):
        try:
            with open("bread.json", "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _write_bread_file(data):
    with open("bread.json", "w") as f:
        json.dump(data, f, indent=4)

async def get_user_points(uid: str) -> int:
    async with bread_lock:
        data = await asyncio.to_thread(_read_bread_file)
        return data.get(uid, 0)

async def adjust_user_points(uid: str, amount: int) -> tuple[int, bool]:
    async with bread_lock:
        data = await asyncio.to_thread(_read_bread_file)
        current = data.get(uid, 0)
        if amount < 0 and current <= 0:
            return 0, False
        new_total = max(0, current + amount)
        data[uid] = new_total
        await asyncio.to_thread(_write_bread_file, data)
        return new_total, True

@bot.event
async def on_message(message: discord.Message):
    return

@bot.event
async def on_ready():
    bot.start_time = datetime.now()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.CommandOnCooldown):
        cd = error.retry_after
        await ctx.send(f"Hey there buddy, slow down! You can use this command again in {cd:.1f}s.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You must be an Administrator to use this command.", ephemeral=True)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Unhandled error: {error}")

@bot.hybrid_command(name="lockall", description="Lock down all text channels in the server.")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def lockall(ctx: commands.Context):
    if not ctx.guild:
        return

    await ctx.defer(ephemeral=True)

    target_role = ctx.guild.default_role

    async def lock_channel(channel: discord.TextChannel):
        overwrites = channel.overwrites_for(target_role)
        overwrites.send_messages = False
        await channel.set_permissions(target_role, overwrite=overwrites)

    tasks = [lock_channel(c) for c in ctx.guild.text_channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success_count = sum(1 for r in results if not isinstance(r, Exception))

    await ctx.send(f"🔒 Server locked down. **{success_count}** text channels closed to @everyone.", ephemeral=True)

@bot.hybrid_command(name="unlockall", description="Unlock all text channels in the server.")
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def unlockall(ctx: commands.Context):
    if not ctx.guild:
        return

    await ctx.defer(ephemeral=True)

    target_role = ctx.guild.default_role

    async def unlock_channel(channel: discord.TextChannel):
        overwrites = channel.overwrites_for(target_role)
        overwrites.send_messages = None
        await channel.set_permissions(target_role, overwrite=overwrites)

    tasks = [unlock_channel(c) for c in ctx.guild.text_channels]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    success_count = sum(1 for r in results if not isinstance(r, Exception))

    await ctx.send(f"🔓 Server unlocked! **{success_count}** text channels are open again.", ephemeral=True)

@bot.hybrid_command(name="givemebread", description="Gives the user a random bread")
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemebread(ctx: commands.Context):
    breads = [
        "🍞 White Bread", "🥖 Baguette", "🥯 Bagel", "🍞 Rye", "🥐 Croissant"
    ]
    roll = random.randint(1, 100)

    if roll == 1:
        chosen = "🌌🍞🤖 Holographic Bread"
    elif roll <= 5:
        chosen = "✨🍞⭐ Legendary Sourbread"
    else:
        chosen = random.choice(breads)

    await ctx.send(f"{chosen}, fresh and warm!")

@bot.hybrid_command(name="givemecheese", description="Gives the user a random cheese")
@commands.cooldown(1, 3, commands.BucketType.user)
async def givemecheese(ctx: commands.Context):
    roll = random.random()

    if roll < 0.005:
        chosen = "🌌🧀🤖 Holographic Cheese"
    elif roll < 0.04:
        chosen = "🌙🧀✨ Mythical Mooncheese"
    else:
        chosen = "🧀 Cheesy cheese!"

    await ctx.send(f"{chosen}")

@bot.hybrid_command(name="countdown", description="Starts a timer countdown")
@commands.cooldown(1, 3, commands.BucketType.user)
async def countdown(ctx: commands.Context, seconds: int):
    if seconds <= 0:
        return await ctx.send("Enter a number greater than 0.")
    if seconds > 300:
        return await ctx.send("Timer cannot exceed 300 seconds.")

    msg = await ctx.send(f"⏳ Timer: {seconds}s")
    while seconds > 0:
        await asyncio.sleep(1)
        seconds -= 1
        if seconds % 5 == 0 or seconds <= 3:
            await msg.edit(content=f"⏳ Timer: {seconds}s")

    await ctx.send("⏰ Time's up!")

@bot.hybrid_command(name="uptime", description="Shows how long the bot has been online")
@commands.cooldown(1, 3, commands.BucketType.user)
async def uptime(ctx: commands.Context):
    if not bot.start_time:
        return await ctx.send("Uptime unavailable.")
    delta = datetime.now() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, secs = divmod(remainder, 60)
    await ctx.send(f"🕒 Uptime: {hours}h {minutes}m {secs}s")

@bot.hybrid_command(name="version", description="Shows the bot version")
@commands.cooldown(1, 3, commands.BucketType.user)
async def version(ctx: commands.Context):
    await ctx.send("noob.bot Version: 1.0.1 (Rewritten)")

@bot.hybrid_command(name="ping", description="Checks the bot latency")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(ctx: commands.Context):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latency is {latency}ms.")

@bot.hybrid_command(name="coinflip", description="Guess heads or tails to win noob points!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def coinflip(ctx: commands.Context, guess: str):
    guess = guess.lower()
    if guess not in ("heads", "tails"):
        return await ctx.send("Pick `heads` or `tails`!")

    uid = str(ctx.author.id)
    result = random.choice(("heads", "tails"))
    won = guess == result

    if won:
        new_bal, _ = await adjust_user_points(uid, 1)
        await ctx.send(
            f"🪙 It's **{result}**! You guessed right! +1 Noob Point (You now have {new_bal} noob points)"
        )
    else:
        new_bal, changed = await adjust_user_points(uid, -1)
        if changed:
            await ctx.send(
                f"🪙 It's **{result}**! Wrong guess... -1 Noob Point (You now have {new_bal} noob points)"
            )
        else:
            await ctx.send(
                f"🪙 It's **{result}**! Wrong guess, but you have no noob points to lose. You're at 0 noob points, win some first!"
            )

@bot.hybrid_command(name="noobpoints", description="Check your noob points balance")
@commands.cooldown(1, 3, commands.BucketType.user)
async def noobpoints(ctx: commands.Context):
    uid = str(ctx.author.id)
    balance = await get_user_points(uid)
    await ctx.send(f"You have **{balance}** noob points!")

@bot.hybrid_command(name="bakerymenu", aliases=["cmds"], description="Shows the bot's command menu")
@commands.cooldown(1, 3, commands.BucketType.user)
async def bakerymenu(ctx: commands.Context):
    embed = discord.Embed(
        title="🥖 NOOB.BOT MENU 🧀",
        description="Available slash commands:",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="🍞 Main Kitchen",
        value=(
            "`/givemebread` – Get a random bread\n"
            "`/givemecheese` – Cheese time\n"
            "`/coinflip [heads/tails]` – Gamble noob points\n"
            "`/noobpoints` – Check your points balance\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚔️ Fun & Interaction",
        value=(
            "`/countdown [seconds]` – Start a timer\n"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ Utility & Moderation",
        value=(
            "`/lockall` – Lock down all text channels\n"
            "`/unlockall` – Unlock all text channels\n"
            "`/uptime` – Bot uptime\n"
            "`/version` – Show bot version\n"
            "`/ping` – Check bot latency\n"
            "`/bakerymenu` – Show this menu\n"
            "`/rewrite` – Why the bot was rewritten\n"
        ),
        inline=False
    )

    embed.set_footer(text="Use /bakerymenu anytime.")
    await ctx.send(embed=embed)

@bot.hybrid_command(name="rewrite", description="Shows the reason for the rewrite of the bot")
@commands.cooldown(1, 3, commands.BucketType.user)
async def rewrite(ctx: commands.Context):
    await ctx.send(
        "The bot was outdated, basically unreadable, and just overall a bad bot. Therefore, we have rewritten the bot from scratch, to turn it into a better, more reliable bot."
    )

from keep_alive import keep_alive
keep_alive()

bot.run(os.environ["BOT_TOKEN"])
