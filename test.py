import pronotepy
from pronotepy.ent import l_normandie

client = pronotepy.Client(
    "https://0760090k.index-education.net/pronote/eleve.html?identifiant=eZGp6R7F4C8rg4G6",
    username="e.frenel5",
    password="E.frenel5",
    ent=l_normandie,
)  # ent specific
if not client.logged_in:
    exit(1)  # the client has failed to log in

"""
# print all the grades the user had in this school year
for period in client.periods:
    # Iterate over all the periods the user has. This includes semesters and trimesters.
    print(period.start, period.name)
    for grade in period.grades:  # the grades property returns a list of pronotepy.Grade
        print(
            grade.grade
        )  # This prints the actual grade. Could be a number or for example "Absent" (always a string)
"""

import datetime

for i in range(7):
    homework = client.homework(datetime.date.today() + datetime.timedelta(days=i))
    print(homework.subject)
    print(homework.description)
