
import pandas as pd

def aggiungi_spesa():
    articolo = input("Inserire Articolo Da Aggiungere Alla Spesa: ").capitalize().strip()
    while True:
        quantita = input("Inserire quantita dell'articolo: ")
        try:
            quantita = int(quantita)
            if quantita >= 0:
                if articolo in lista_spesa:
                    scelta = input("L'articolo sembra gia presente nella lista della spesa\n"
				"Digita 1 Se lo si vuole sovrascrivere\n"
				"Digita 2 Se si vogliono sommare le quantità\n"
				"Digita 3 per Bloccare l'inserimento\n")
                    if scelta == "2":
                        lista_spesa[articolo] += quantita
                        print(f"è stato aggiunto una quantità di {quantita} all'articolo {articolo} per un totale di {lista_spesa[articolo]}")
                        return
                    elif scelta == "3":
                        print(f"Inserimento bloccato al momento per l'articolo {articolo} la quantità è {lista_spesa[articolo]}")
                        return
                    else:
                        print("Scelta non valida di default si sovrascrivera la quantità dell'articolo")

                lista_spesa[articolo] = quantita
                print(f"é stato aggiunto alla lista l'articolo {articolo} in {quantita} quantità")
                return
            else:
                print("quantità non valida")
        except ValueError:
            print("La quantità inserita non è valida inserire un numero intero positivo")


def rimozione_spesa():
    articolo = input("Inserire l'articolo da eliminare: ").capitalize().strip()
    if articolo not in lista_spesa:
        print("Articolo non presente")
    else:
        del lista_spesa[articolo]
        print(f"Eliminato con successo l'articolo {articolo} dalla lista della spesa")



def visualizza_spesa():
    print("Lista Della Spesa:")
    if lista_spesa:

        df = pd.DataFrame(list(lista_spesa.items()), columns=["Articolo", "Quantità"])
        df = df.sort_values(by="Articolo")
        df = df.reset_index(drop=True)
        print(df)
    else:
        print("La Lista è Ancora Vuota")

def salva_spesa(lista_spesa):
    lista_spesa = {chiave: lista_spesa[chiave] for chiave in sorted(lista_spesa)}
    with open("lista_della_spesa.txt", "w") as file:

        for chiave, valore in lista_spesa.items():
            file.write(f"{chiave}: {valore}\n")

    print("La lista della spesa è stata salvata con nome lista_della_spesa.txt")

def importa_spesa():
    with open("lista_della_spesa.txt", "r") as file:
        for linea in file:
            chiave, valore = linea.split(":")
            lista_spesa[chiave] = int(valore)

    print("La lista della spesa è stata importata da lista_della_spesa.txt")
    visualizza_spesa()

lista_spesa = {}
print("Programma Per Creare Una lista Della Spesa\n")
print("Digita 1: Per Aggiungere Un Elemento Alla Lista\n"
      "Digita 2: Per Rimuovere Un Elemento Dalla Lista\n"
      "Digita 3: Per Visualizzare La Lista\n"
      "Digita 4: Per Salvare La Lista In Un File txt\n"
      "Digita 5: Per Importare Una Lista Già Creata\n"
      "Digita Qualsiasi Altra Cosa Per Chiudere Il Programma")

while True:
    scelta = input("\nDigita Il Numero Per L'Operazione Che Si Vuole Compiere: ")
    if scelta == "1":
        aggiungi_spesa()
    elif scelta == "2":
        rimozione_spesa()
    elif scelta == "3":
        visualizza_spesa()
    elif scelta== "4":
        salva_spesa(lista_spesa)
    elif scelta == "5":
        importa_spesa()
    else:
        scelta = input("Sicuro Di Voler Chiudere Il Programma: Y/N").lower()
        if scelta == "y":
            print("Grazie Per Aver Usato Il Programma")
            break
