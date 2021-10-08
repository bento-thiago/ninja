import os
import shutil

for f in os.listdir("F:\\Trabalho\\DiarioUnico\\database"):
    if f[-3:] == "php" and f.split(".")[0] > "Version201909161214":
        nome = f.split(".")[0]
        os.system(
            "python manage.py makemigrations diario_unico --empty -n " + f.split(".")[0])

counter = 43
for f in os.listdir("F:\\Trabalho\\DiarioUnico\\database"):
    if f[-3:] == "php" and f.split(".")[0] > "Version201909161214":
        nome = "{:04d}".format(counter) + "_" + f.split(".")[0] + ".py"
        arq_old = open(os.path.join(
            "F:\\Trabalho\\DiarioUnico\\database", f), "r", encoding="utf-8").read()
        open("F:\\Trabalho\\PastasContabeis\\diario_unico\\migrations\\" +
             nome, "a").write(arq_old)
        counter += 1
