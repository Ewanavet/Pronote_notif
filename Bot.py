import main_pronote_def as pro
import pandas as pd
import json
from time import sleep
from Bot_Discord import sendMessage

print("\n\n30 mins after")
active = True
on = True

old_grades = pro.get_gardes()[2]

while on:
    pro.actualise_json_grades()

    # pro.get_gardes()[2] = trimestre 3
    grades = pro.get_gardes()[2]
    print(len(grades), len(old_grades))
    if len(grades) > len(old_grades):
        added_old_grades = pd.DataFrame(
            columns=["date", "sujet", "note", "sur"])
        for i in range(len(grades)):
            persent = False
            for j in range(len(old_grades)):
                if old_grades[j] == grades[i]:
                    persent = True
            if persent == False:
                added_old_grades.loc[len(added_old_grades)] = [
                    grades[i].date, grades[i].subject.name, grades[i].grade, grades[i].out_of]

        print(f"{len(grades) - len(old_grades)} note(s) ajoutée(s)")
        print(added_old_grades)
    else:
        print("no new grades")

    old_grades = grades

    config = json.load(
        open("D:\TOUT\Documents\Programation\Projets\Python\pronote\config.json", "r"))
    active = config["active"]
    on = config["on"]
    sendMessage(f"{active}, {on}")
    sleep(10)
    print(active, on)
print("Bot Of")
