import socket
import re
import pandas as pd
import subprocess
import platform
def scelta_ip():
    ip_locali = ottieni_ip_locali()
    print("Indirizzi IP locali disponibili:")
    for ip in ip_locali:
        print(f"- {ip}")

    while True:
        ip = input("\nInserisci l'indirizzo IP da scansionare: ").strip()
        if validazione_ip(ip):
            if verifica_raggiungibilita(ip):
                print("Hai inserito un IP valido e raggiungibile.")
                return ip
            else:
                print("L'indirizzo IP inserito non è raggiungibile.")
        else:
            print("L'indirizzo IP non è valido. Assicurati di usare il formato xxx.xxx.xxx.xxx.")
    
def ottieni_ip_locali():
    ip_list = []
    hostname = socket.gethostname()
    try:
        ip_list = socket.gethostbyname_ex(hostname)[2]
    except Exception as e:
        print(f"Errore nell'ottenere gli IP locali: {e}")
    return ip_list

def validazione_ip(ip):
    ottetti = ip.split(".")
    if len(ottetti) != 4:
        return False
    for ottetto in ottetti:
        if not ottetto.isdigit() or not 0 <= int(ottetto) <= 255:
            return False
    return True

def verifica_raggiungibilita(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "1", ip]
    try:
        esito = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return esito.returncode == 0
    except Exception as e:
        print(f"Errore durante la verifica dell'IP: {e}")
        return False
    
def controllo_porte(porta):
    if porta.isdigit():
        porta = int(porta)
        if porta <= 65535:
            return porta
        else:
            print("Il valore massimo di una porta è 65535.")
    else:
        print("Inserisci una porta valida!")

def scelta_porta_iniziale():
    porta_iniziale = input("Inserisci la porta di inizio: ").strip()
    porta_iniziale = controllo_porte(porta_iniziale)
    if porta_iniziale:
        return porta_iniziale
    return scelta_porta_iniziale()

def scelta_porta_finale(porta_iniziale):
    porta_finale = input("Inserisci la porta di fine: ").strip()
    porta_finale = controllo_porte(porta_finale)
    if porta_finale:
        if porta_finale >= porta_iniziale:
            return porta_finale
        else:
            print("La porta di inizio non può essere maggiore della porta di fine!")
    return scelta_porta_finale(porta_iniziale)

def scelta_porte():
    lista_porte = input("Inserire le porte che si vogliono controllare lasciando uno spazio tra ogni porta: ").strip()
    lista_porte = re.sub(r"[^\d\s]", "", lista_porte)
    lista_porte = lista_porte.split(sep=" ")

    for i in range(len(lista_porte)):
        lista_porte[i] = controllo_porte(lista_porte[i])
        if not lista_porte[i]:
            print(f"Eliminata {i+1}° porta inserita perché non valida.")

    lista_porte = [porta for porta in lista_porte if porta is not None]
    lista_porte.sort()
    return lista_porte


def portscanner_range(ip, porta_iniziale, porta_finale):
    risultato_scanner = {}
    for porta in range(porta_iniziale, porta_finale + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  
        risultato = sock.connect_ex((ip, porta))
        if risultato == 0:
            risultato_scanner[porta] = "Aperta"
        else:
            risultato_scanner[porta] = "Chiusa"
        sock.close()
    return risultato_scanner

def portscanner_lista(ip, porte):
    risultato_scanner = {}
    for porta in porte:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  
        risultato = sock.connect_ex((ip, porta))
        if risultato == 0:
            risultato_scanner[porta] = "Aperta"
        else:
            risultato_scanner[porta] = "Chiusa"
        sock.close()
    return risultato_scanner




ip = scelta_ip()
while True:
    scelta_funzionamento = input("Digitare 1 se si vuole controllare per un range di porte\nDigitare 2 per controllare per una lista di porte: ").strip()
    if scelta_funzionamento in ["1", "2"]:
        break
    print("Inserire un valore valido! (1 o 2)")

if scelta_funzionamento == "1":
    porta_iniziale = scelta_porta_iniziale()
    porta_finale = scelta_porta_finale(porta_iniziale)
    porte_risultato = portscanner_range(ip, porta_iniziale, porta_finale)
    print(f"\nPorte nel range {porta_iniziale} - {porta_finale}:")

elif scelta_funzionamento == "2":
    lista_porte = scelta_porte()
    porte_risultato = portscanner_lista(ip, lista_porte)
    print(f"Porte nella lista {lista_porte}:")

if porte_risultato:
    df = pd.DataFrame(list(porte_risultato.items()), columns=["Porta", "Stato"])
    print("\nLista Porte:\n")
    print(df.to_string(index=False))
else:
    print("Non sono state inserite porte valide!")
