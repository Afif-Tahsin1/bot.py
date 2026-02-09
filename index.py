#---------Import
import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import asyncio
import json

#------Setting up client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix=None, intents=intents)

#---------Functions
load_dotenv()
#If client ready
@client.event
async def on_ready():
    print(f"Bot is online!\nLogged in as {client.user.name}.")
    synched = await client.tree.sync()
    lenth = len(synched)
    try:
        if lenth == 0:
            print("No commands found!")
        else:
            print(f"Successfully loaded {lenth} commands!")
    except Exception as e:
        print(f"Something went wrong! Error:\n{e}")
#------Variable
fruits = ["rocket", "spin", "blade", "spring", "bomb", "smoke", "spike", "flame", "dark", "sand", "ice", "rubber", "eagle", "ghost", "light", "diamond", "quake", "magma", "love", "spider", "sound", "phoenix", "creation", "blizzard", "buddha", "portal", "shadow", "venom", "spirit", "mammonth", "gravity", "trex", "pain", "dough", "lightning", "tiger", "gas", "yeti", "kitsune", "control", "dragon", "dragoneast", "dragonweast"]

weights = [
    100, 95, 90, 85, 80, 75, 70,  # ১-৭ নম্বর ফল (খুবই কমন)
    65, 60, 55, 50, 45, 40, 35,   # ৮-১৪ নম্বর ফল
    30, 28, 26, 24, 22, 20, 18,   # ১৫-২১ নম্বর ফল
    16, 14, 12, 10, 9, 8, 7,      # ২২-২৮ নম্বর ফল
    6, 5, 4, 3.5, 3, 2.5, 2,      # ২৯-৩৫ নম্বর ফল
    1.5, 1.2, 1, 0.8, 0.5, 0.3, 0.2, 0.1 # ৩৬-৪৩ নম্বর ফল (Mythical/Dragonweast)
]

price = {"rocket": 500, "spin": 1500, "blade": 3000, "spring": 5000, "bomb": 8000, 
    "smoke": 12000, "spike": 15000, "flame": 25000, "dark": 30000, "sand": 35000, 
    "ice": 45000, "rubber": 60000, "eagle": 75000, "ghost": 90000, "light": 110000, 
    "diamond": 130000, "quake": 150000, "magma": 180000, "love": 200000, 
    "spider": 220000, "sound": 250000, "phoenix": 300000, "creation": 350000, 
    "blizzard": 400000, "buddha": 500000, "portal": 600000, "shadow": 700000, 
    "venom": 850000, "spirit": 1000000, "mammonth": 1200000, "gravity": 1400000, 
    "trex": 1700000, "pain": 1800000, "dough": 200000, "lightning": 2200000, 
    "tiger": 2500000, "gas": 2800000, "yeti": 3200000, "kitsune": 4000000, 
    "control": 4500000, "dragon": 5000000, "dragoneast": 6000000, "dragonweast": 8000000}
#-------Class
class Trade_button(discord.ui.View):
    def __init__(self, sender, reciever, fruit, data_func, save_func):
        super().__init__(timeout=60)
        self.sender = sender
        self.reciever = reciever
        self.fruit = fruit
        self.load_data = data_func
        self.save_data = save_func

    @discord.ui.button(label="accept", style=discord.ButtonStyle.green)
    async def accept_callback(self, interaction: discord.Interaction, button:discord.ui.Button):
        if interaction.user.id != self.reciever.id:
            await interaction.response.send_message("This is not for you!", ephemeral=True)
            return
        data = await self.load_data()
        s_id, r_id = str(self.sender.id), str(self.reciever.id)

        if self.fruit not in data[s_id].get("fruits", []):
            return await interaction.response.send_message("Gift failed!")
        data[s_id]["fruits"].remove(self.fruit)
        data[r_id]["fruits"].append(self.fruit)
        await self.save_data(data)
        await interaction.response.edit_message(f"Gift was successfull!")

        
#------Function
#------JSON
#------User
#------Loading
async def load_user_data():
    try:
        with open("user.json", "r") as f: 
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

#---------Saving
async def save_user_data(user):
    try:
        with open("user.json", "w") as f:
            json.dump(user, f, indent=4)
    except FileNotFoundError:
        print("File not found!")

#Creating acc slash commands
@client.tree.command(name="createacc", description="create a account")
@app_commands.describe(user_name="pls select username")
async def createacc(interaction: discord.Interaction, user_name : str):
    data = await load_user_data()
    user_id = str(interaction.user.id)
    all_names = [user.get("username", "").lower() for user in data.values()]
    if user_name.lower() in all_names:
        await interaction.response.send_message("The name is already in the data!")
        return
    elif user_id in data:
        await interaction.response.send_message("You already created an account")
        return
    elif " " in user_name:
        await interaction.response.send_message("Username can't contain space!")
        return
    elif len(user_name) > 20 or len(user_name) < 3:
        await interaction.response.send_message("Username must be greater than 3 and less that 20!")
        return
    elif not user_name.isalnum():
        await interaction.response.send_message("Username cannot contain any emojoi or anything!")
        return
    elif user_name.isdigit():
        await interaction.response.send_message("Username cannot be only numbers!")
        return
    else:
        data[user_id] = {}
        data[user_id]["username"] = user_name
        data[user_id]["cash"] = 0
        data[user_id]["fruits"] = []
        data[user_id]["xp"] = 0
        data[user_id]["level"] = 1
        data[user_id]["title"] = []
        data[user_id]["equippedtitles"] = ""
        await interaction.response.send_message(f"Successfully created account!")
    await save_user_data(data)

#Roll slash commands
@client.tree.command(name="roll", description="roll a fruits")
async def roll(interaction: discord.Interaction):
    data = await load_user_data()
    randomF = random.choices(fruits, weights=weights, k=1)[0]
    user_id = str(interaction.user.id)
    if user_id not in data:
        await interaction.response.send_message("First make accounts!")
        return
    else:
        data[user_id]["fruits"].append(randomF)
        await interaction.response.send_message(f"You've rolled **{randomF}!**")
    await save_user_data(data)
    
#Sell slash commands
@client.tree.command(name="sell", description="sell a fruits")
@app_commands.describe(fruit="pls type a frtuits you want to sell")
async def sell(interaction: discord.Interaction, fruit:str):
    data = await load_user_data()
    user_id = str(interaction.user.id)
    fruit_low = fruit.lower()
    prices = price.get(fruit_low, 0)
    if user_id not in data:
        await interaction.response.send_message("First make an account")
        return
    
    elif fruit_low not in data[user_id]["fruits"]:
        await interaction.response.send_message("You don't have this fruits!")
        return
    else:
        data[user_id]["fruits"].remove(fruit_low)
        data[user_id]["cash"] += prices
        await interaction.response.send_message(f"Successfully sold **{fruit}!**")
    await save_user_data(data)

#Inventory
@client.tree.command(name="inventory", description="show inventory")
@app_commands.describe(user="pls enter user id")
async def inventory(interaction: discord.Interaction, user:str | None = None):
    user_id = str(interaction.user.id)
    data = await load_user_data()
    if user == None:
        if user_id not in data:
            await interaction.response.send_message("First make accounts!")
            return
        elif data[user_id]["fruits"] == []:
            await interaction.response.send_message("You don't have any fruits!")
            return
        else:
            fruit = ",\n🍎".join(data[user_id]["fruits"])
            await interaction.response.send_message(f"Your inventory: \n {fruit}")
            return
    else:
        if user not in data:
            await interaction.response.send_message("Can't find the user!")
            return
        elif not data[user]["fruits"]:
            await interaction.response.send_message("He don't have any fruits!")
            return
        else:
            fruit = "🍎"+",\n🍎".join(data[user]["fruits"])
            await interaction.response.send_message(f"Inventory:\n{fruit}")

#Cash slash commands
@client.tree.command(name="balance", description="show balance")
@app_commands.describe(user="pls enter user id")
async def balance(interaction: discord.Interaction, user : str | None = None):
    user_id = str(interaction.user.id)
    data = await load_user_data()
    if user == None:
        if user_id not in data:
            await interaction.response.send_message("First make accounts!")
            return
        else:
            balances = data[user_id]["cash"]
            await interaction.response.send_message(f"You earned total {balances}$")
            return
    else:
        if user not in data:
            await interaction.response.send_message("Can't find user!")
            return
        else:
            balances = data[user]["cash"]
            await interaction.response.send_message(f"Balances: {balances}")
            return

#Gift slash commands
@client.tree.command(name="gift", description="gift a fruits to someone")
@app_commands.describe(fruit="pls select a fruits", user="pls enter user id")
async def gift(interaction: discord.Interaction, fruit:str, user:discord.Member):
    s_id = str(interaction.user.id)
    data = await load_user_data()
    r_id = str(user.id)
    fruitss = fruit.lower()
    if s_id not in data:
        await interaction.response.send_message("First make accounts!")
    elif r_id not in data:
        await interaction.response.send_message("Something went wrong!")
        return
    elif fruitss not in data[s_id].get("fruits", []):
        await interaction.response.send_message("Something went wrong!")
        return
    else:
        view = Trade_button(interaction.user, user, fruitss, load_user_data, save_user_data)
        await interaction.response.send_message(f"Hey **{user.mention}!** {interaction.user.mention} want to give you **{fruitss}**!", view=view)
    await save_user_data(data)

#Bet slash commands
@client.tree.command(name="bet", description="bet your money")
@app_commands.describe(choice="pls select head or tail", money="pls select money")
@app_commands.choices(choice=[
    app_commands.Choice(name="head", value="head"),
    app_commands.Choice(name="tail", value="tail")
])
async def bet(interaction: discord.Interaction, choice : app_commands.Choice[str], money : int):
    user_id = str(interaction.user.id)
    data = await load_user_data()
    items = ["head", "tail"]
    radnomC = random.choice(items)
    if user_id not in data:
        await interaction.response.send_message("Fist make an accounts!")
        return
    elif money < 0:
        await interaction.response.send_message("Crazy man!")
        return
    elif money > data[user_id].get("cash", 0):
        await interaction.response.send_message("Do you really have that much money?")
        return
    if choice.value == radnomC:
        await interaction.response.defer()
        await interaction.followup.send("Not again! You win!")
        data[user_id]["cash"] += money
    else:
        await interaction.response.defer()
        await interaction.followup.send("Gotchu! You lose!")
        data[user_id]["cash"] -= money
    await save_user_data(data)

#Training slash
@client.tree.command(name="train", description="train to earn xp")
@app_commands.checks.cooldown(1, 60.0, key=lambda i: (i.user.id))
async def train(interaction: discord.Interaction):
    data = await load_user_data()
    user_id = str(interaction.user.id)
    
    if user_id not in data:
        await interaction.response.send_message("Make an account first!")
        return
    if "title" not in data[user_id]:
        data[user_id]["title"] = []

    xp_needed = data[user_id]["level"] * 100
    xp_per = data[user_id]["level"] * 5
    data[user_id]["xp"] += xp_per

    msg = f"⚔️ You worked hard! Your xp: {data[user_id]['xp']}"
    
    if data[user_id]["xp"] >= xp_needed:
        data[user_id]["xp"] = 0
        data[user_id]["level"] += 1
        level = data[user_id]["level"]
        msg = f"🆙 Level up! Your level: {level}"

        new_title = None
        if level == 100: new_title = "blox master"
        elif level == 50: new_title = "grand admiral"
        elif level == 25: new_title = "veteran"
        elif level == 10: new_title = "pirate"
        if new_title and new_title not in data[user_id]["title"]:
            data[user_id]["title"].append(new_title)
            msg += f"\n🏆 New Title Unlocked: **{new_title}**!"
    await interaction.response.send_message(msg)
    await save_user_data(data)

#Error training
@train.error
async def train_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Slow down! Retry after {error.retry_after:.2f}seconds", ephemeral=True)

#Showing title
@client.tree.command(name="titles", description="show titles")
async def titlse(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = await load_user_data()
    if user_id not in data:
        await interaction.response.send_message("First make an accounts!")
        return
    elif data[user_id]["title"] == []:
        await interaction.response.send_message("You don't have any titles!")
        return
    
    titles = f"🎴,\n".join(data[user_id]["title"])
    await interaction.response.send_message(f"Titles:\n{titles}, \nEquipped titles: \n{data[user_id]["equippedtitles"]}")
    return

#Eqquiping titles
@client.tree.command(name="equiptitle", description="equip a title")
@app_commands.describe(titles = "pls select a title")
async def equiptitle(interaction: discord.Interaction, titles:str):
    user_id = str(interaction.user.id)
    data = await load_user_data()
    titlesL = titles.lower()
    if user_id not in data:
        await interaction.response.send_message("First create an accounts!")
        return
    elif titlesL not in data[user_id]["title"]:
        await interaction.response.send_message("You don't have that titles!")
        return
    else:
        data[user_id]["equippedtitles"] = titlesL
        await interaction.response.send_message(f"Successfully equippeed {titlesL}Title!")

#Stats check commands
#Running bot
token = os.getenv("TOKEN")
if token:
    print("Token found! Attempting to join...")
    client.run(token)
else:
    print("Can't found token! Check the env")
