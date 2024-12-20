import socket
import subprocess
import platform

def ottieni_ip_locali():
    ip_list = []
    try:
        hostname = socket.gethostname()
        ip_list = socket.gethostbyname_ex(hostname)[2]
    except Exception as e:
        print(f"Errore nell'ottenere gli IP: {e}")
    return ip_list

def validazione_ip(ip):
    ottetti = ip.split(".")
    if len(ottetti) != 4:
        return False
    for ottetto in ottetti:
        if not ottetto.isdigit() or not 0 <= int(ottetto) <= 255:
            return False
    return True


def scelta_ip():
    ip_disponibili = ottieni_ip_locali()
    print("Indirizzi IP disponibili:")
    for ip in ip_disponibili:
        print(f"- {ip}")

    while True:
        ip = input("\nInserisci l'indirizzo IP da utilizzare: ").strip()
        if validazione_ip(ip):
            if verifica_raggiungibilita(ip):
                print("Hai inserito un IP valido e raggiungibile.")
                return ip
            else:
                print("L'indirizzo IP inserito non è raggiungibile.")
        else:
            print("L'indirizzo IP non è valido. Assicurati di usare il formato xxx.xxx.xxx.xxx.")

def controllo_porte(porta):
    if porta.isdigit():
        porta = int(porta)
        if porta <= 65535:
            return porta
        else:
            print("Il valore massimo di una porta è 65535.")
    else:
        print("Inserisci una porta valida!")

def scelta_porta():
    while True:
        porta = input("Inserisci la porta da utilizzare: ").strip()
        porta = controllo_porte(porta)
        if porta:
            return porta

def verifica_raggiungibilita(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    comando = ["ping", param, "1", ip]
    try:
        esito = subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return esito.returncode == 0
    except Exception as e:
        print(f"Errore durante la verifica dell'IP: {e}")
        return False

def avvio_socket(ip, porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, porta))
    s.listen(1)
    print("Server avviato! In attesa di connessioni...")

    connection, address = s.accept()
    print("Client connesso con indirizzo:", address)

    while True:
        data = connection.recv(1024)
        if not data:
            break

        print(data.decode('utf-8'))

    connection.close()


ip = scelta_ip()
porta = scelta_porta()
avvio_socket(ip, porta)
