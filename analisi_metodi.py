import requests

def invio_richiesta(metodo, url, data=None):
    try:
        risposta = requests.request(metodo, url, json=data, timeout=5)
        print(f"{metodo.upper()} {url} - Status Code: {risposta.status_code}")
        return risposta
    except requests.exceptions.ConnectionError:
        print(f"{metodo.upper()} {url} - Connessione rifiutata. Verifica che il server sia attivo.")
    except requests.exceptions.Timeout:
        print(f"{metodo.upper()} {url} - Timeout. Il server non ha risposto in tempo.")
    except requests.exceptions.RequestException as e:
        print(f"{metodo.upper()} {url} - Errore durante la richiesta: {e}")
    return None

descrizione_codice = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable"
}


def inserisci_url():
    while True:
        url = input("Inserisci l'URL (es. www.esempio.com): ").strip()
        
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        try:
            if requests.head(url, allow_redirects=True, timeout=1).ok:
                print(f"URL valido e raggiungibile: {url}")
                return url
            else:
                print("URL non raggiungibile. Riprovare.")
        except requests.RequestException:
            print("Errore nel raggiungere l'URL. Riprovare.")


url= inserisci_url()

data = {
    "chiave": "valore",
}

print("Inizio delle richieste HTTP\n")

get_response = invio_richiesta("get", url)
post_response = invio_richiesta("post", url, data=data)
put_response = invio_richiesta("put", url, data=data)
delete_response = invio_richiesta("delete", url)

print("\nRiepilogo delle risposte:")
risposte = {
    "GET": get_response,
    "POST": post_response,
    "PUT": put_response,
    "DELETE": delete_response
}

for metodo, risposta in risposte.items():
    if risposta is not None:
        code = risposta.status_code
        descrizione = descrizione_codice.get(code, risposta.reason)
    else:
        code = "N/A"
        descrizione = "N/A"
    print(f"{metodo} - Status Code: {code} ({descrizione})")
