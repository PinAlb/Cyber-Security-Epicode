from scapy.all import sniff, wrpcap, get_if_list
from scapy.layers.inet import IP, TCP, UDP, ICMP

def gestore_pacchetti(pacchetto):
    if IP in pacchetto:
        ip_sorgente = pacchetto[IP].src
        ip_destinazione = pacchetto[IP].dst

        if TCP in pacchetto:
            protocollo = "TCP"
            porta_sorgente = pacchetto[TCP].sport
            porta_destinazione = pacchetto[TCP].dport
        elif UDP in pacchetto:
            protocollo = "UDP"
            porta_sorgente = pacchetto[UDP].sport
            porta_destinazione = pacchetto[UDP].dport
        elif ICMP in pacchetto:
            protocollo = "ICMP"
            porta_sorgente = None
            porta_destinazione = None
        else:
            protocollo = "Altro"
            porta_sorgente = None
            porta_destinazione = None

        print(f"Protocollo: {protocollo}, IP Sorgente: {ip_sorgente}, IP Destinazione: {ip_destinazione}, "
              f"Porta Sorgente: {porta_sorgente}, Porta Destinazione: {porta_destinazione}")
        
        
def cattura_pacchetti(interfaccia, filtro_protocollo, nome_file, numero_pacchetti=0):
    
    if filtro_protocollo in["tcp","udp","icmp"]:
        print(f"Avvio Cattura Pacchetti Su Interfaccia: {interfaccia} Con Filtro: {filtro_protocollo}")
    else:
        filtro_protocollo = None
        print(f"Avvio Cattura Pacchetti Su Interfaccia: {interfaccia} Senza Filtri:")


    pacchetti_catturati = sniff(iface=interfaccia, filter=filtro_protocollo, prn=gestore_pacchetti, count=numero_pacchetti)
    
    if not nome_file.endswith((".pcap")):
        nome_file = nome_file + ".pcap"
    wrpcap(nome_file, pacchetti_catturati)
    print(f"Pacchetti catturati salvati in: {nome_file}")


interfacce = get_if_list()
print("Interfacce Disponibili:")
for interfaccia in interfacce:
    print(f"- {interfaccia}")
while True:
    interfaccia = input("Inserisci l'interfaccia di rete: ").strip()
    if interfaccia in interfacce:
        break
    print("Inserire Un Interfaccia Disponibile")
    
filtro_protocollo = input("Inserisci il protocollo da filtrare (TCP/UDP/ICMP).\nQualunque Altro Valore Non Avvierà Nessun Filtro: ").strip().lower()
nome_file = input("Inserisci il nome del file di output: ").strip()

while True:
    numero_pacchetti = input("Inserisci il numero di pacchetti da catturare (0 per cattura illimitata): ")
    if numero_pacchetti.isdigit():
        numero_pacchetti = int(numero_pacchetti)
        if numero_pacchetti >= 0:
            break
        else:
            print("Inserire Un Numero Maggiore o Uguale a 0")
    else:
        print("Inserire Un Numero")

cattura_pacchetti(interfaccia, filtro_protocollo, nome_file, numero_pacchetti)
