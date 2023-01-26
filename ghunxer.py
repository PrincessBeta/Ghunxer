
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
async def roll(ctx,dice: str,bonus: int = 0,malus: int = 0):
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
        stats_string = " ".join([str(k) for k in stats])
        sheet.write(name+"\n"+user+"\n"+channel+"\n"+str(bank)+"\n"+stats_string)

        for item in inventory.keys() :
            sheet.write("\n"+item + ":" + str(inventory[item]))
        

        
create_character_sheet("naruto","123","321",50,[1,2,3,4],{"saucisse":12,"tomate":14,"amour propre" : 0})
#-----------------------------------------------------------------------------#
#                             Launching the bot                               #
#-----------------------------------------------------------------------------#


bot.start()