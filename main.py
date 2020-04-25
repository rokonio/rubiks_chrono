import datetime as dt
import os
import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import simpledialog as sd
from string import whitespace

# Chemin du dossier dans lequelle le fichier se trouve, les \ sont remplacer par des /
this_path = "/".join((os.path.abspath(os.path.split(__file__)[0]).split("\\")))

# Liste des average à afficher
AO_LIST = [5, 12, 50, 100, 500, 1000]
ao_label_list = []

start = 0
run = False
final_time = 0


def scramble():
    total = ""
    moves = ["R", "L", "F", "B", "U", "D"]
    for i in range(random.randint(19, 22)):
        b = random.choice(moves)
        while i > 0 and b == d:
            b = random.choice(moves)
        d = b
        total += b + random.choice(["'", "2", ""]) + " "
    return total


# Récupere l'average des nb dernier temps
def aoN(nb):
    total = []
    count = 0
    with open(session_name + "/times.txt", "r") as f:
        for line in reversed(f.read().split("\n")):
            if not (line in whitespace) and count < nb:
                count += 1
                total.append(float(line.split(":")[1]) + float(line.split(":")[0]) * 60)
    try:
        return (sum(total) - min(total) - max(total)) / (nb - 2)
    except:
        return 0


# Mettre à jour les ao
def update_ao():
    for ao in range(len(AO_LIST)):
        ao_actual = aoN(AO_LIST[ao])
        if (
            len(
                list(
                    filter(
                        lambda x: not x in whitespace,
                        open(session_name + "/times.txt", "r").read().split("\n"),
                    )
                )
            )
            >= AO_LIST[ao]
        ):
            ao_label_list[ao]["text"] = (
                "ao"
                + str(AO_LIST[ao])
                + " = "
                + (str(ao_actual)[:5] if len(str(ao_actual)) > 5 else str(ao_actual))
            )
        else:
            ao_label_list[ao]["text"] = "ao" + str(AO_LIST[ao]) + " = " + "..."


# Met à jour l'affichage de chrono
def update_chrono():
    time = dt.datetime.now() - start
    chrono["text"] = (
        ((str(time.seconds // 60) + ":") if time.seconds > 59 else "")
        + str(time.seconds % 60)
        + "."
        + str(time.microseconds)[:2]
    )


# Ecrire un temps dans le fichier
def write_time():
    time = dt.datetime.now() - start
    time = dt.timedelta(seconds=time.seconds, microseconds=float(chrono["text"][-2:]))
    with open(session_name + "/times.txt", "a") as f:
        f.write(
            str(time.seconds // 60)
            + ":"
            + str(time.seconds % 60)
            + "."
            + str(time.microseconds)[:2]
            + "\n"
        )


# Trouver le pb
def pb():
    times = []
    with open(session_name + "/times.txt", "r") as f:
        for line in f.read().split("\n"):
            if not line in whitespace:
                times.append(float(line.split(":")[1]) + int(line.split(":")[0]))
    try:
        return str(int(min(times) // 60)) + ":" + str(min(times) % 60)
    except:
        return "0:0.0"


# Faire la moyenne de tout les temps
def mean():
    times = []
    ratio = 0
    with open(session_name + "/times.txt", "r") as f:
        for line in f.read().split("\n"):
            if not line in whitespace:
                times.append(float(line.split(":")[1]) + int(line.split(":")[0]))
                ratio += 1
    try:
        return str(int((sum(times) / ratio) // 60)) + (
            str((sum(times) / ratio) % 60)
            if len(str((sum(times) / ratio) % 60)) < 4
            else str((sum(times) / ratio) % 60)[:4]
        )
    except:
        return "0:0.0"


# Demander à créer une nouvel session
create_session = mb.askquestion(
    "Nouvel session ?", "Voulez vous choisir une session(oui) ou en créer une (non)"
)

if create_session == "no":
    session_name = (
        this_path
        + "/Sessions/"
        + sd.askstring("Nom de session", "Entrez un nom de session :")
    )
elif create_session == "yes":
    session_name = fd.askdirectory(initialdir=this_path)

# Création de la fenêtre
root = tk.Tk()
root.config(background="#ccccff")
root.geometry("1200x500")


if not os.path.exists(session_name):
    os.makedirs(session_name)
    open(session_name + "/times.txt", "x").close()

# Frame pour les average
ao_frame = tk.Frame(root, background="#270083")
ao_frame.pack(side="right")

# Label de melange
scramble_label = tk.Label(
    root, text=str(scramble()), font=("Comic", 25), bg=root["bg"], fg="#4E4E4E"
)
scramble_label.pack(side="top")

# Faire afficher tout les ao de la liste
for ao in AO_LIST:
    ao_label_list.append(
        tk.Label(
            ao_frame,
            text="ao" + str(ao) + " = " + str(aoN(ao)),
            font=("Helvetica", 20),
            bg=ao_frame["bg"],
            fg="white",
        )
    )
    ao_label_list[-1].pack()

# Le chrono
chrono = tk.Label(root, text="0.00", font=("Helvetica", 35), bg=root["bg"], fg="black")
chrono.pack(pady=100)

# Infos de la session en bas à gauche
infos_session = tk.Frame(root, background=root["bg"])
infos_session.pack(side="left", padx=100)

nb_solve = tk.Label(
    infos_session,
    background=infos_session["bg"],
    text="Vous avez fait "
    + str(
        len(
            list(
                filter(
                    lambda x: not x in whitespace,
                    open(session_name + "/times.txt", "r").read().split("\n"),
                )
            )
        )
    )
    + " solve(s)",
    font=("Helvetica", 25),
)
nb_solve.pack()

pb_label = tk.Label(
    infos_session,
    background=infos_session["bg"],
    text="Pb : " + pb(),
    font=("Helvetica", 25),
)
pb_label.pack()

mean_label = tk.Label(
    infos_session,
    background=infos_session["bg"],
    text="Moyenne : " + mean(),
    font=("Helvetica", 25),
)
mean_label.pack()


def update():
    if run:
        update_chrono()
    root.after(10, update)


def go(*useless):
    global run, start
    if run:
        write_time()
        scramble_label["text"] = str(scramble())
        run = False
        nb_solve["text"] = (
            "Vous avez fait "
            + str(
                len(
                    list(
                        filter(
                            lambda x: not x in whitespace,
                            open(session_name + "/times.txt", "r").read().split("\n"),
                        )
                    )
                )
            )
            + " solve(s)"
        )
        pb_label["text"] = "Pb : " + pb()
        mean_label["text"] = "Moyenne : " + mean()
        update_ao()
    else:
        nb_solve["text"] = (
            "Vous avez fait "
            + str(
                len(
                    list(
                        filter(
                            lambda x: not x in whitespace,
                            open(session_name + "/times.txt", "r").read().split("\n"),
                        )
                    )
                )
            )
            + " solve(s)"
        )
        pb_label["text"] = "Pb : " + pb()
        mean_label["text"] = "Moyenne : " + mean()
        run = True
        start = dt.datetime.now()


update()
update_ao()
root.bind("<KeyRelease-space>", go)

root.mainloop()
