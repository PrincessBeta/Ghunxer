
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

# def roll_all_dice(string :str):
#     pattern = re.compile("[0-9]+d[0-9]+")
#     dice = pattern.findall(string)
#     rolls = []
#     for roll in dice:
#         n,die = roll.split("d")
#         n,die = int(n),int(die)
#         value = 0
#         for i in range(n):
#             value+=randrange(1,die+1)
#         rolls.append(value) 
    
#     for die in range(len(dice)):
#         string = string.replace(dice[die],str(rolls[die]))
#     return string


# @bot.command(
#     name="my_first_command",
#     description="This is the first command I made!"
#     )
# async def my_first_command(ctx: interactions.CommandContext):
#     await ctx.send("Hi there!")

#-----------------------------------------------------------------------------#
#                              CSV manipulation                               #
#-----------------------------------------------------------------------------#

# def csv_add_row(filename : str,x : list) -> bool:
#     """
#     adds a row to a csv file if it isn't already in it.
#     returns true if the row was added, false if not.
#     """
#     with open(filename,"a+",encoding="utf-8",newline= "") as file:
#         file.seek(0) #we need to put the file pointer back at the start
#         reader = csv.reader(file,delimiter=",", quotechar='"')
#         writer = csv.writer(file,delimiter=",", quotechar='"')

#         #only write if sender's not already written
#         if not list(map(str,x)) in reader:
#             writer.writerow(x)
#             return True
#         return False

#-----------------------------------------------------------------------------#
#                             Launching the bot                               #
#-----------------------------------------------------------------------------#


bot.start()