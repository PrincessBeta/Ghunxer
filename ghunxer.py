
import interactions
from random import randrange
import csv


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
#                                Misc Commands                                #
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
    
@bot.command(
    name="displaysheet",
    description="shows a character's sheet",
    scope=SERVER_ID,
)
@interactions.option()
async def displaysheet(ctx:interactions.context,character : str):
    with open("characters/"+character+".csv","r") as sheet :
        stats = sheet.readlines()
        await ctx.send(embeds=interactions.Embed(
            title= character+"'s Character Sheet",
            description= "owned by <@"+stats[0][:-1]+">",
            fields=[
                interactions.EmbedField(name="Bank",value=stats[2][:-1]+"ω"),
                interactions.EmbedField(name="Stats",value = stats[3][:-1]),
                interactions.EmbedField(name="Puissance",value= stats[4][:-1]),
                interactions.EmbedField(name="Inventaire",value= "".join(stats[5:])),
            ]
        ))

#-----------------------------------------------------------------------------#
#                              CSV manipulation                               #
#-----------------------------------------------------------------------------#

def create_character_sheet(
    name:str,
    user:str,
    channel:str,
    bank:int,
    stats:list,
    inventory:dict={}
    ) :
    with open(f"characters/{name}.csv","x") as sheet :
        stats_string = f"Force : {stats[0]}, Agilité : {stats[1]}, Maitrise : {stats[2]}"
        sheet.write(user+"\n"+channel+"\n"+str(bank)+"\n"+stats_string+"\n"+str(stats[3])+"/"+str(stats[3]))

        for item in inventory.keys() :
            sheet.write("\n"+ str(inventory[item]) + " * " +item )
        

        
create_character_sheet("naruto","278291770855522317","1015574682088509480",500,[1,2,3,4],{"saucisse":12,"tomate":14,"amour propre" : 0})

#-----------------------------------------------------------------------------#
#                             Launching the bot                               #
#-----------------------------------------------------------------------------#


bot.start()