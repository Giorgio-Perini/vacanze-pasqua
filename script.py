import random
import pandas as pd

dati_carte = pd.read_csv('pokemon.csv')

carte_disponibili = []

for i in range(len(dati_carte)):
    nome = dati_carte.loc[i, 'Nome']
    rarita = dati_carte.loc[i, 'Rarità']
    
    carte_disponibili.append(
        {'Nome': nome, 'Rarità': rarita}
    )

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

def estrai_carta(carte):
    rarita_estratta = random.choices(
        list(probabilita_rarita.keys()),
        list(probabilita_rarita.values())
    )[0]
    
    carte_possibili = []

    for carta in carte:
        if carta['Rarità'] == rarita_estratta:
            carte_possibili.append(carta)
    
    if len(carte_possibili) > 0:
        return random.choice(carte_possibili)
    else:
        carte_comuni = []

        for carta in carte:
            if carta['Rarità'] == 'Comune':
                carte_comuni.append(carta)

        return random.choice(carte_comuni)

def apri_pacchetto(punti, collezione, carte):
    if punti < 10:
        print("Non hai abbastanza punti per aprire un pacchetto!")
        return punti, collezione
    
    punti = punti - 10

    nuove_carte = []

    print("Hai aperto un pacchetto! Carte trovate:")

    for _ in range(5):
        carta = estrai_carta(carte)
        nuove_carte.append(
            {'Nome': carta['Nome'], 'Rarità': carta['Rarità']}
        )
        punti = punti + punti_per_rarita.get(carta['Rarità'], 0)
        print(carta['Nome'], "-", carta['Rarità'])

    df_nuove_carte = pd.DataFrame(nuove_carte)

    collezione = pd.concat(
        [collezione, df_nuove_carte],
        ignore_index=True
    )

    print("Punti attuali:", punti)

    return punti, collezione

def mostra_collezione(collezione):
    if len(collezione) == 0:
        print("Non hai ancora nessuna carta!")
    else:
        print("Collezione:")
        print(collezione.to_string(index=True))

def mostra_punti(punti):
    print("Punti attuali:", punti)

def salva_collezione(collezione):
    collezione.to_csv('collezione_salvata.csv', index=False)
    print("Collezione salvata su 'collezione_salvata.csv'")

def menu():
    punti = 100
    collezione = pd.DataFrame(columns=['Nome', 'Rarità'])

    while True:
        print("=== MENU PRINCIPALE ===")
        print("1. Apri pacchetto (10 punti)")
        print("2. Mostra collezione")
        print("3. Mostra punti")
        print("4. Salva collezione (opzionale)")
        print("5. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == '1':
            punti, collezione = apri_pacchetto(punti, collezione, carte_disponibili)
        elif scelta == '2':
            mostra_collezione(collezione)
        elif scelta == '3':
            mostra_punti(punti)
        elif scelta == '4':
            salva_collezione(collezione)
        elif scelta == '5':
            print("Grazie per aver giocato! Alla prossima!")
            break
        else:
            print("Scelta non valida. Riprova.")

menu()
