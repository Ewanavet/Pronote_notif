import pandas as pd
import pronotepy
from pronotepy.ent import l_normandie

from config_token import id_ent


def connection():
    client = pronotepy.Client(
        "https://0760090k.index-education.net/pronote/eleve.html?identifiant=eZGp6R7F4C8rg4G6",
        username=id_ent[0],
        password=id_ent[1],
        ent=l_normandie,
    )
    if not client.logged_in:
        exit(1)
    else:
        return client


def get_gardes_current_period(client):
    grade_list = []
    for grade in client.current_period.grades:
        grade_list.append(grade)
    return grade_list


def equivalent_name(name):
    long_name = [
        "ANGLAIS LV1",
        "ALLEMAND LV2",
        "FRANCAIS",
        "HISTOIRE-GEOGRAPHIE",
        "ENS. MORAL & CIVIQUE",
        "ED.PHYSIQUE & SPORT.",
        "ENSEIGN.SCIENTIFIQUE > ENS SC PHYSIQUE",
        "ENSEIGN.SCIENTIFIQUE > ENS SC SVT",
        "NUMERIQUE SC.INFORM.",
        "PHYSIQUE-CHIMIE",
        "CINEMA-AUDIOVISUEL",
        "MATHEMATIQUES",
        "MATHS SPECIFIQUES",
    ]
    short_name = [
        "ANGLAIS",
        "ALLEMAND",
        "FRANCAIS",
        "HISTOIRE-GEO",
        "EMC",
        "EPS",
        "ENS PHYSIQUE",
        "ENS SVT",
        "NSI",
        "PHYSIQUE-CHIMIE",
        "CAV",
        "MATHS",
        "MATHS OPTION",
    ]
    i = 0
    while name != long_name[i] and i <= len(long_name):
        i += 1
    return short_name[i]


def creat_df(grades):
    # create dataframe with new grade(s)
    added_old_grades = pd.DataFrame(
        [
            [
                grade.date,
                equivalent_name(grade.subject.name),
                grade.coefficient,
                grade.grade.replace(",", "."),
                grade.out_of.replace(",", "."),
                grade.comment,
                grade.average.replace(",", "."),
                grade.id,
            ]
            for grade in grades
        ],
        columns=["date", "sujet", "coef", "note", "sur", "comment", "class", "id"],
    )
    return added_old_grades


def find_new_grades(df1, df2):
    added_grades = pd.DataFrame(None, columns=df2.columns.values)
    for i in range(df2.shape[0]):
        if df2["id"].iloc[i] not in df1["id"].values:
            added_grades.loc[i] = df2.iloc[i]
    return added_grades
