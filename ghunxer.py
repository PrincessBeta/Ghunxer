
import interactions
from random import randrange

SERVER_ID = 830127177869426699
token = ""
with open("./token.txt",encoding='utf8') as f:
    token = f.read()
bot = interactions.Client(token=token)
#-----------------------------------------------------------------------------#
#                                Core Commands                                #
#-----------------------------------------------------------------------------#

@bot.command(
    name="stop",
     description="shuts the bot down.",
     scope=SERVER_ID
)
async def stop(ctx:interactions.CommandContext) :
    await ctx.send("ghunxer died")
    await bot._stop()



#-----------------------------------------------------------------------------#
#                              Discord Commands                               #
#-----------------------------------------------------------------------------#

@bot.command(
    name="roll",
    description="rolls dice.",
    scope=SERVER_ID,
    options=[
        interactions.Option(
            name="dice",
            description="usage : <n1>d<n2>",
            type=interactions.OptionType.STRING,
            required=True
        ),interactions.Option(
            name="bonus",
            description="an integer",
            type=interactions.OptionType.INTEGER,
            required=False
        ),interactions.Option(
            name="malus",
            description="an integer",
            type=interactions.OptionType.INTEGER,
            required=False,

        ),
    ]
)
async def roll(ctx:interactions.CommandContext,dice: str,bonus: int = 0,malus: int = 0):
    dice = dice
    string = ""
    total = bonus - malus
    n,die = dice.split("d")
    n,die = int(n),int(die)
    for i in range(n):
        val = randrange(1,die+1)
        string += f"[{val}] "
        total += val
    message = f"total = {total} \ndetail : {string}"
    if bonus : message+=f" + {bonus}"
    if malus : message+=f" + {malus}"
    await ctx.send(message)

@bot.command(
    name="test",
    scope=SERVER_ID
)
async def test(ctx:interactions.CommandContext):
    channel = ctx.channel
    await channel.send(embeds=interactions.Embed(
        name="Naruto Character Sheet",
        description="Owned by <@278291770855522317>",
        fields=[
            interactions.EmbedField(name="bank",value="112 shmeckles"),
            interactions.EmbedField(name="power",value="1500/2"),
            interactions.EmbedField(name="bank",value="112 shmeckles")
        ]
    ))

#-----------------------------Sheet Manipulation------------------------------#

@bot.command(
    name="displaysheet",
    description="shows a character's sheet",
    scope=SERVER_ID,
)
@interactions.option()
async def displaysheet(ctx:interactions.CommandContext,character : str):
    sheet = get_sheet(character)
    stats = sheet.splitlines()
    stats[3] = stats[3].split(" ")
    statsDisplay = f"Force : {stats[3][0]}\n Agilit?? : {stats[3][1]}\n Maitrise : {stats[3][2]}"
    await ctx.send(embeds=interactions.Embed(
        title= character+"'s Character Sheet",
        description= "owned by <@"+stats[0][:-1]+">",
        fields=[
            interactions.EmbedField(name="Banque",value=stats[2]+"??"),
            interactions.EmbedField(name="Stats",value = statsDisplay),
            interactions.EmbedField(name="Puissance",value= stats[4]),
            interactions.EmbedField(name="Inventaire",value= "".join(stats[5:])),
        ]
    ))

@bot.command(
    description="adds a charater's sheet to the bot",
    scope=SERVER_ID,
    )
@interactions.option()
@interactions.option()
@interactions.option()
@interactions.option()
@interactions.option()
@interactions.option()
@interactions.option()
async def addsheet(
    ctx:interactions.CommandContext,
    name:str,
    channel:str,
    bank:int,
    strength:int,
    agility:int,
    mastery:int,
    power:int,
    ):
    create_character_sheet(name,str(ctx.author.id),channel,bank,[strength,agility,mastery,power])
    await ctx.send("character successfully created")

@bot.command(
    name="addmoney",
    description="adds money to a character's bank.",
    scope=SERVER_ID
)
@interactions.option()
@interactions.option()
async def addmoney(ctx:interactions.CommandContext,character : str,amount:int) :
    sheet = get_sheet(character)
    lines = sheet.splitlines()
    lines[2] = str(int(lines[2])+amount)
    sheet = "\n".join(lines)
    set_sheet(character,sheet)



#-----------------------------------------------------------------------------#
#                             File manipulation                               #
#-----------------------------------------------------------------------------#

def create_character_sheet(
    name:str,
    user:str,
    channel:str,
    bank:int,
    stats:list,
    inventory:dict={}
    ):
    """
    creates a character sheet using the provided information, inventory and powers can be empty
    """
    with open(f"characters/{name}.csv","x") as sheet :
        stats_string = f"{stats[0]} {stats[1]} {stats[2]}"
        sheet.write(user+"\n"+channel+"\n"+str(bank)+
            "\n"+stats_string+"\n"+str(stats[3])+"/"+str(stats[3])+"\n")

        for item in inventory.keys() :
            sheet.write(str(inventory[item]) + " * " +item +"\n")

def get_sheet(character) -> str:
    """
    returns the raw sheet file of the specified character
    """
    string = ""
    with open("characters/"+character+".csv","r") as sheet :
        string = sheet.read()
    return string

def set_sheet(character : str,sheet) :
    with open("characters/"+character+".csv","w") as f :
        f.write(sheet)

#-----------------------------------------------------------------------------#
#                             Launching the bot                               #
#-----------------------------------------------------------------------------#


bot.start()