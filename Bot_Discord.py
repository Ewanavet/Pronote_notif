import discord
from discord.ext import tasks, commands
import json
import main_pronote_def as pro
import pandas as pd


icon_url = "https://www.zupimages.net/up/23/19/zamy.png"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
trimestre = 2  # trimestre -1
rep_grades = "D:/TOUT/Documents/Programation/Projets/Python/pronote/notes.json"
old_grades = pro.get_gardes()[trimestre]


@bot.command()
async def test(ctx, arg):
    print("test", arg)
    await ctx.send("!test" + arg)


@bot.command()
async def set_trimestre(ctx, arg):
    global trimestre
    trimestre = int(arg) - 1
    await ctx.send(f"Le trimestre est maintenant {trimestre + 1}")


@bot.command()
async def current_trimestre(ctx):
    await ctx.send(f"Le trimestre actuel est {trimestre + 1}")


@bot.command()
async def stop_notifying(ctx):
    checkForNewGrades.stop()
    await ctx.send("Stop bot notification")


@bot.command()
async def start_notifying(ctx):
    checkForNewGrades.start()
    await ctx.send("Start bot notification")


@bot.event
async def on_ready():
    await bot.get_channel(1096499664146157578).send("Info : bot is online")
    checkForNewGrades.start()


@tasks.loop(seconds=60*1)  # toutes les 10 mins
async def checkForNewGrades():
    global old_grades
    grades = pro.get_gardes()[trimestre]
    pro.actualise_json_grades(path_json=rep_grades)

    print("Now :", len(grades), ", before :", len(old_grades))
    if len(grades) > len(old_grades):
        print(f"{len(grades) - len(old_grades)} note ajoutée" if len(grades) - len(old_grades) == 1 else f"{len(grades) - len(old_grades)} notes ajoutées")
        added_old_grades = pro.creat_df(grades, old_grades)
        print(added_old_grades)

        # Notification message
        pre_message = f"<@454920766698553354> {len(grades) - len(old_grades)} note ajoutée" if len(grades) - len(old_grades) == 1 else f"<@454920766698553354> {len(grades) - len(old_grades)} notes ajoutées"
        await bot.get_channel(1096499664146157578).send(pre_message)
        
        for i in range(len(added_old_grades)):
            grade_msg = added_old_grades.iloc[i]
            if grade_msg['comment']:
                message = f"- note : *{grade_msg['note']}/{grade_msg['sur']}*\n- sujet : {grade_msg['comment']}\n- coef : *{grade_msg['coef']}*\n- classe : *{grade_msg['class']}/{grade_msg['sur']}*"
            else:
                message = f"- note : *{grade_msg['note']}/{grade_msg['sur']}*\n- coef : *{grade_msg['coef']}*\n- classe : *{grade_msg['class']}/{grade_msg['sur']}*"
            
            # create embed
            embed = discord.Embed(
                title=f"__{grade_msg['sujet']} :__",
                description=f"Trimestre {trimestre+1}",
                color=0x77fe07
            )
            embed.set_author(name="pronote bot", icon_url=icon_url)
            embed.add_field(name=f"date : {grade_msg['date']}", value=message, inline=False)

            # send embed notification
            await bot.get_channel(1096499664146157578).send(embed=embed)
        
        old_grades = grades  # Mettre à jour old_grades avec les nouvelles notes
    else:
        print("no new grades")
        await bot.get_channel(1102644587073380352).send("No new grades,\n" + "Now : " + str(len(grades)) + ", before : " + str(len(old_grades)))

bot.run('OTYyNDM1MDI1MTU1MDE4ODQy.GtSicc.wuQuwD6jJR7WillEP6vpFQ4PBn1CcqzYauFTvs')
