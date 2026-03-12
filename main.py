import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/calcul")
def calcul(a: int, b: int):
    time.sleep(5)  # Simulation d'un calcul lourd
    return {"resultat": a + b}
