import csv
from _pyrepl import reader


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open( file_path , 'r') as file:
            #ho provato a usare un dizionario di liste di dizionari
            anni={}
            for line in file:
                reader = csv.DictReader(file) #leggo come un dizionario
                foto={"codice":reader.codice,"titolo":reader.titolo,"autore":reader.autore,"mese":reader.mese,}
                if reader.anno not in anni: #se non c'è l'anno lo aggiungo
                    anni[reader.anno] = [] #prima creo la lista
                    anni[reader.codice].append(foto)# poi aggiungo i dati della foto
                else:
                    anni[reader.anno].append(foto)#se invece l'anno c'è aggiungo solo il dizionario coi dati
        return anni
    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

       with open(file_path, 'a') as file: #sulla falsa riga della creazione dell'album
           writer = csv.writer(file)
            if anno not in album: #controllo di esistenza dell'anno
                album[anno] = []
                foto={"codice":codice,"titolo":titolo,"autore":autore,"mese":mese}
                album[anno].append(foto) #aggiunta della foto secondo le specifiche fornite
            else:
                foto = {"codice": codice, "titolo": titolo, "autore": autore, "mese": mese}
                album[anno].append(foto)
            writer.writerow([codice, titolo, autore, mese, anno])
            nuova_foto="{codice} ,{titolo} ,{autore}, {mese}, {anno}"
            return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    for anno in album:
        for foto in album[anno]:
            if foto["codice"] == codice:
                print(foto["codice"], foto["titolo"], foto["autore"], foto["mese"], album["anno"])


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    titoli = []
    for anno in album:
        for foto in album[anno]:
            titoli.append(foto["titolo"])
    titoli.sort()
    for titolo in titoli:
        print(titolo, end=" ")



def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
