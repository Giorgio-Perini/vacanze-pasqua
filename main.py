import random
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
punti = 100
dati_carte = pd.read_csv('pokemon.csv')

carte_disponibili = []
for i in range(len(dati_carte)):
    carta = {'Nome': dati_carte.loc[i, 'Nome'], 'Rarità': dati_carte.loc[i, 'Rarità']}
    carte_disponibili.append(carta)

probabilita_rarita = {
    'Comune': 0.70,
    'Non Comune': 0.20,
    'Rara': 0.09,
    'Ultra Rara': 0.01
}

punti_per_rarita = {
    'Comune': 1,
    'Non Comune': 3,
    'Rara': 6,
    'Ultra Rara': 15
}

def leggi_collezione():
    df = pd.read_csv('collezione.csv')
    return df.to_dict(orient='records')


def scrivi_collezione(collezione):
    df = pd.DataFrame(collezione)
    df.to_csv('collezione.csv', index=False)

def calcola_punti(collezione):
    totale = 0
    for carta in collezione:
        rarita = carta['Rarità']
        totale += punti_per_rarita.get(rarita, 0)
    return totale

def estrai_carta():
    rarita_estratta = random.choices(
        list(probabilita_rarita.keys()),
        list(probabilita_rarita.values())
    )[0]
    
    carte_possibili = []
    for carta in carte_disponibili:
        if carta['Rarità'] == rarita_estratta:
            carte_possibili.append(carta)

    if carte_possibili:
        return random.choice(carte_possibili)
    else:
        carte_comuni = []
        for carta in carte_disponibili:
            if carta['Rarità'] == 'Comune':
                carte_comuni.append(carta)
        return random.choice(carte_comuni)

@app.route('/')
def menu():
    collezione = leggi_collezione()
    if not collezione:
        collezione = [{'Nome': 'Inizio', 'Rarità': 'Comune'}]
        scrivi_collezione(collezione)
    return render_template('menu.html', punti=punti)

@app.route('/apri_pacchetto')
def apri_pacchetto():
    collezione = leggi_collezione()
    punti = calcola_punti(collezione)

    if punti < 10:
        return render_template('errore.html', messaggio="Non hai abbastanza punti per aprire un pacchetto!")

    nuove_carte = []
    
    for _ in range(5):
        carta = estrai_carta()
        nuove_carte.append({'Nome': carta['Nome'], 'Rarità': carta['Rarità']})
        punti += punti_per_rarita.get(carta['Rarità'], 0)

    punti -= 10

    nuova_collezione = collezione + nuove_carte

    scrivi_collezione(nuova_collezione)

    return render_template('apri_pacchetto.html', carte=nuove_carte, punti=calcola_punti(nuova_collezione))

@app.route('/mostra_collezione')
def mostra_collezione():
    collezione = leggi_collezione()
    return render_template('mostra_collezione.html', collezione=collezione)

@app.route('/mostra_punti')
def mostra_punti():
    collezione = leggi_collezione()
    punti = calcola_punti(collezione)
    return render_template('mostra_punti.html', punti=punti)

@app.route('/salva_collezione')
def salva_collezione():
    return render_template('salva_collezione.html')

@app.route('/reset')
def reset():
    scrivi_collezione([])
    return render_template('reset.html')

if __name__ == '__main__':
    app.run(debug=True)
