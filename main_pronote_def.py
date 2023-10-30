import json
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


def actualise_json_grades(
    path_json="D:/TOUT/Documents/Programation/Projets/Python/pronote/notes.json",
):
    client = connection()
    if client.logged_in:  # check if client successfully logged in
        nom_utilisateur = client.info.name  # get users name
        print(f"Logged in as {nom_utilisateur}")
        subjects_names = [
            "ANGLAIS LV1",
            "ALLEMAND LV2",
            "FRANCAIS",
            "HISTOIRE-GEOGRAPHIE",
            "ENS. MORAL & CIVIQUE",
            "ED.PHYSIQUE & SPORT.",
            "ENSEIGN.SCIENTIFIQUE > ENS SC PHYSIQUE",
            "ENSEIGN.SCIENTIFIQUE > ENS SC SVT",
            "NUMERIQUE SC.INFORM. > NUMERIQUE SC.INFORM.",
            "PHYSIQUE-CHIMIE",
            "CINEMA-AUDIOVISUEL > CINEMA-AUDIOVISUEL",
            "MATHS SPECIFIQUES",
        ]
        dict_periods = []
        for period in client.periods:
            if len(period.grades) != 0:
                L = [{i: []} for i in subjects_names]
                for grade in period.grades:  # trimestre par trimestre
                    if grade.grade != "NonNote":
                        j = 0
                        while grade.subject.name != subjects_names[j]:
                            j += 1

                        if "," in grade.grade:
                            grade_float = list(grade.grade)
                            i = 0
                            while grade_float[i] != ",":
                                i += 1
                            grade_float[i] = "."
                            grade_float = "".join(grade_float)
                        else:
                            grade_float = grade.grade
                        if "," in grade.out_of:
                            out_float = list(grade.out_of)
                            i = 0
                            while out_float[i] != ",":
                                i += 1
                            out_float[i] = "."
                            out_float = "".join(out_float)
                        else:
                            out_float = grade.out_of

                        L[j][subjects_names[j]].append(
                            (float(grade_float), float(out_float))
                        )

                dict_periods.append({"period": period.name, "grades": L})
        dict_periods.append(
            {
                "coef_list": [
                    ("ANGLAIS LV1", 6),
                    ("ALLEMAND LV2", 6),
                    ("FRANCAIS", 6),
                    ("HISTOIRE-GEOGRAPHIE", 6),
                    ("ENS. MORAL & CIVIQUE", 1),
                    ("ED.PHYSIQUE & SPORT.", 6),
                    ("ENSEIGN.SCIENTIFIQUE > ENS SC PHYSIQUE", 6),
                    ("ENSEIGN.SCIENTIFIQUE > ENS SC SVT", 6),
                    ("NUMERIQUE SC.INFORM. > NUMERIQUE SC.INFORM.", 11),
                    ("PHYSIQUE-CHIMIE", 11),
                    ("CINEMA-AUDIOVISUEL > CINEMA-AUDIOVISUEL", 11),
                    ("MATHS SPECIFIQUES", 2),
                ]
            }
        )

        with open(path_json, "w") as fp:
            json.dump(dict_periods, fp)
        print("\nGrades saved as :", path_json, "\n")
    else:
        print("Failed to log in")
        exit()


def get_gardes():
    client = connection()
    if client.logged_in:  # check if client successfully logged in
        grade_list_all = []
        for period in client.periods:
            if not len(period.grades):
                break
            grade_list = []
            for grade in period.grades:
                grade_list.append(grade)
            grade_list_all.append(grade_list)
        return grade_list_all
    else:
        print("Failed to log in")
        exit()


def make_stats(
    path_json="D:/TOUT/Documents/Programation/Projets/Python/pronote/notes.json",
):
    return


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
