import discord, apiFetch, urllib, urllib.parse, os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# Server id
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID_DEV"))

STEAM_LISTING_URL="https://steamcommunity.com/market/listings/730/"

GUNS_KNIVES_GLOVES = sorted([
    "AK-47", "AUG", "AWP", "CZ75-Auto", "Desert Eagle", "Dual Berettas",
    "FAMAS", "Five-SeveN", "G3SG1", "Galil AR", "Glock-18", "M249", "M4A1-S",
    "M4A4", "MAC-10", "MAG-7", "MP5-SD", "MP7", "MP9", "Negev", "Nova",
    "P2000", "P250", "PP-Bizon", "R8 Revolver", "SCAR-20", "SG 553", "SSG 08",
    "Tec-9", "UMP-45", "USP-S", "XM1014", "Zeus x27",
    "★ Bayonet", "★ Bowie Knife", "★ Butterfly Knife", "★ Falchion Knife",
    "★ Flip Knife", "★ Huntsman Knife", "★ Karambit", "★ M9 Bayonet",
    "★ Navaja Knife", "★ Nomad Knife", "★ Paracord Knife", "★ Shadow Daggers",
    "★ Skeleton Knife", "★ Stiletto Knife", "★ Survival Knife", "★ Talon Knife",
    "★ Ursus Knife",
    "★ Bloodhound Gloves", "★ Broken Fang Gloves", "★ Driver Gloves", "★ Hand Wraps",
    "★ Hydra Gloves", "★ Moto Gloves", "★ Specialist Gloves", "★ Sport Gloves"
], key=lambda x: x.lstrip("★ ").lower())

# Class to suggest autocomplete to user for gun name
class GunAutoComplete(app_commands.Transformer):
    async def autocomplete(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=item, value=item)
            for item in GUNS_KNIVES_GLOVES if current.lower() in item.lower()
        ][:25]

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        # Force sync command to guild
        try:
            guild_id = discord.Object(id = os.getenv("GUILD_ID_DEV"))
            synced = await self.tree.sync(guild = guild_id)
            print(f'Synced {len(synced)} commands to guild {guild_id.id}')

        except Exception as e:
            print(f'Error on sync command: {e}')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix = "!", intents = intents)

@client.tree.command(name = "price_check", description = "Check the price of a skin on CSFloat", guild = GUILD_ID)

#Gun choices
@app_commands.describe(gun = 'Choose the gun', skin  = 'Choose the skin', wear = "Choose the wear of the skin")
@app_commands.autocomplete(gun=GunAutoComplete().autocomplete)

#Wear choices
@app_commands.choices(wear = [
        app_commands.Choice(name = "Factory New", value = "FN"),
        app_commands.Choice(name = "Minimal Wear", value = "MW"),
        app_commands.Choice(name = "Field-Tested", value = "FT"),
        app_commands.Choice(name = "Well-Worn", value = "WW"),
        app_commands.Choice(name = "Battle-Scarred", value = "BS")
    ])


async def priceCheck(interaction:discord.Interaction, gun: str, skin: str, wear: app_commands.Choice[str]):
    item = gun + ' | ' + skin 
    listing_url=STEAM_LISTING_URL+urllib.parse.quote(item+" ("+wear.name+")")

    embed = discord.Embed(title = 'Link', url = listing_url,
                          color = discord.Color.darker_grey())
    
    embed.add_field(name = 'Item', value = item)
    embed.add_field(name = 'Wear', value = wear.value, inline=True)
    embed.add_field(name = 'Price', value = '$'+str(apiFetch.fetchLatestPrice(item+" ("+wear.name+")")), inline=False)
    embed.set_thumbnail(url = apiFetch.fetchImage(item))

    await interaction.response.send_message(embed = embed)

client.run(os.getenv("DISCORD_TOKEN"))
