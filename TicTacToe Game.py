"""
import librerie necessarie (numeri random, gui toolkit)
"""
import random 
from tkinter import *
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = None
    
#parametri di default: mappature dei punteggi per le sequenze
DEFAULT_MAP_PUNTEGGIO = {2: 1, 3: 2, 4: 10, 5: 25}

def get_segmenti_contigui(linea, simbolo):
    """
    data una linea e un simbolo, restituisce una lista con le lunghezze
    delle sequenze continue del simbolo in quella linea
    -esamina ogni cella della linea fornita e conta le sequenze del simbolo passato
    -quando trova simboli uguali, conta la sequenza e la memorizza nella lista segmenti
    """
    segmenti = []
    count = 0
    for cella in linea:
        if cella == simbolo:
            count += 1
        else:
            if count > 0:
                segmenti.append(count)
                count = 0
    if count > 0:
        segmenti.append(count)
    return segmenti

def punteggio_linea(segmenti, mappa_punteggi):
    """
    calcola il punteggio complessivo per una linea dato l'elenco delle lunghezze delle
    sequenze e la mappa dei punteggi
    -somma i punteggi delle sequenze contigue di simboli in una linea utilizzando la mappa dei punteggi per determinare il punteggio
    -sequenza inferiore a 3, non viene conteggiata - lunghezza 5 o superiore, viene assegnato il punteggio associato alla sequenza di lunghezza 5
    """
    punteggio = 0
    for seg in segmenti:
        if seg < 3:
            continue
        elif seg >= 5:
            punteggio += mappa_punteggi[5]
        elif seg in mappa_punteggi:
            punteggio += mappa_punteggi[seg]
    return punteggio


def get_linee_board(board, dimensione):
    """
    data la mappa di gioco (board) e la sua dimensione, restituisce una lista di tutte le linee da controllare:
    - righe, colonne, diagonali e antidiagonali
    """
    linee = []
    N = dimensione
    #righe
    for r in range(N):
        linee.append(board[r])
    #colonne
    for c in range(N):
        col = [board[r][c] for r in range(N)]
        linee.append(col)
    #diagonali principali
    for k in range(N):
        diag1 = [board[i][i - k] for i in range(k, N)]
        if diag1:
            linee.append(diag1)    
        if k != 0:
            diag2 = [board[i - k][i] for i in range(k, N)]
            if diag2:
                linee.append(diag2)
    #diagonali antidiagonali
    for k in range(N):
        anti1 = [board[i][N - 1 - (i - k)] for i in range(k, N)]
        if anti1:
            linee.append(anti1)
        if k != 0:
            anti2 = [board[i - k][N - 1 - i] for i in range(k, N)]
            if anti2:
                linee.append(anti2)
    return linee



def calcolo_punteggio_board(board, simbolo, dimensione, mappa_punteggi):
    """
    calcola il punteggio per il simbolo data la situazione attuale del board di gioco
    -scorre le linee del board
    -calcola richiamndo la funzione per trovare i segmenti di simboli
    -calcola il punteggio totale sommando i punteggi delle linee
    """
    punteggio_totale = 0
    for linea in get_linee_board(board, dimensione):
        segmenti = get_segmenti_contigui(linea, simbolo)
        punteggio_totale += punteggio_linea(segmenti, mappa_punteggi)
    return punteggio_totale



def fine_partita(game, root, bottoni, vincitore):
    """
    gestisce la fine della partita mostrando un messaggio di vittoria e una finestra
    con opzioni per l'utente su come procedere (nuova partita, impostazioni, uscita)
    -se non esiste message_box mostrato nell'oggetto game viene creato e impostato a false
    -mostra il msg solo se non è già stato mostrato
    -se la partita non è già stata segnata come finita, mostra la finestra di fine partita
    -crea l'istanza della finestra e settaggio impostazioni grafiche e bottoni
    """
    
    if not hasattr(game, 'messagebox_mostrato'):
        game.messagebox_mostrato = False
        
    
    if not game.messagebox_mostrato:
        messagebox.showinfo("Vittoria", f"Ha vinto {vincitore['nome']} con {vincitore['score']} punti!")
        game.messagebox_mostrato = True

    
    if not hasattr(game, 'partita_finita') or not game.partita_finita:
        game.partita_finita = True
        finestra_fine = Toplevel(root)
        finestra_fine.title("Partita finita")  
        finestra_fine.geometry("450x300") 
        label1 = Label(finestra_fine, text = "Vuoi fare un'altra partita?")
        label1.pack()
        
        #bottoni con diverse opzioni
        button = Button(finestra_fine, text = "Si, con le stesse impostazioni",
                    command = lambda:reset_partita(game, finestra_fine, bottoni))
        
        button_impostazioni = Button(finestra_fine, text = "Si, con impostazioni diverse",
                    command = lambda:restart_impostazioni(root, game)) 
        
        button_exit = Button(finestra_fine, text = "No, esci",
                    command = lambda:chiudi_finestra(root, game)) 
        button.place(x = 30, y = 50)
        button_impostazioni.place(x = 170, y = 50)
        button_exit.place(x = 100, y = 100)
        
        

def reset_partita(game, root, bottoni):
    """    
    reimposta lo stato del gioco per iniziare una nuova partita con le stesse impostazioni:
    -azzera la griglia, i punteggi dei giocatori e il turno corrente
    -aggiorna l'interfaccia grafica rimuovendo i simboli dai bottoni 
    -infine chiude la finestra di fine partita
    """
    
    game.partita_finita = False
    
    game.board = [['.' for _ in range(game.dimensione)] for _ in range(game.dimensione)]
    for giocatore in game.giocatori:
        giocatore['score'] = 0
    game.turno = 0
    
    for r in range(game.dimensione):
        for c in range(game.dimensione):
            bottoni[r][c].config(text='')
            
    print("Nuova partita avviata con le stesse impostazioni!")
    chiudi_finestra(root)
    

def restart_impostazioni(root, game):
    """
    rermina la partita attuale e avvia una nuova finestra per scegliere impostazioni diverse
    """
    game.partita_finita = False  
    chiudi_finestra(root, game)
    print("Nuova partita con impostazioni diverse")
    run_gui()
    
    
def chiudi_finestra(root, game):
    """
    chiude la finestra corrente e imposta lo stato del gioco come non finito
    """
    game.partita_finita = False
    root.destroy()


   
class Game:
    def __init__(self, dimensione, giocatori, mappa_punteggi=DEFAULT_MAP_PUNTEGGIO, win_threshold=70):
        """
        inizializza la classe gioco-game con:
          - dimensione: lato della matrice NxN
          - giocatori: lista di dizionari contenenti { 'nome', 'simbolo', 'score', 'tipo' } -- per i computer, è aggiunto anche 'difficolta'
          - score_map: mappa dei punteggi per lunghezze di sequenze
          - turno: turno di gioco
          - board di gioco
          - win_threshold: punteggio per vincere la partita
        """ 
        self.dimensione = dimensione
        self.board =  [['.' for _ in range ( dimensione ) ] for _ in range ( dimensione ) ]
        self.giocatori = giocatori 
        self.mappa_punteggi = mappa_punteggi
        self.win_threshold = win_threshold
        self.turno = 0
        
        
    def stampa_board(self):
        """
        stampa il tabellone in maniera formattata
        -scorre il board stampa gli elementi della riga separati da uno spazio " " 
        """
        print("\nTabellone:")
        for riga in self.board:
            print(" ".join(riga))
        print()
        
    
    def mossa_valida(self, r, c):
        """
        verifica se la mossa (r, c) è valida
        -controlla se r e c sono dentro i limiti del board 
        -se r e c sono validi e la casella è vuota ritorna True 
        """
        r_valida = 0 <= r < self.dimensione
        c_valida = 0 <= c < self.dimensione
        casella_vuota = self.board[r][c] == '.'
        if r_valida and c_valida and casella_vuota:
            return True
        else:
            return False
    
    def giocatore_corrente(self):
        """
        restituisce il giocatore a cui tocca
        """
        return self.giocatori[self.turno]
    
       
    def mossa(self, r, c):
        """
        effettua la mossa per il giocatore corrente assegnando il simbolo nella posizione della griglia
        """
        giocatore = self.giocatore_corrente()
        self.board[r][c] = giocatore['simbolo']
        

    def prossimo_turno(self):
        """
        passa il turno al giocatore successivo -- % per far si che quando si arrivi a turno == giocatori il resto dia 0 e si rinizi dal turno del primo giocatore
        """
        self.turno = (self.turno + 1) % len(self.giocatori)
        
        
    def get_tutte_linee(self):
        """
        restituisce tutte le linee (righe, colonne, diagonali e antidiagonali) del board richiamando la funzione get_linee_board
        """
        return get_linee_board(self.board, self.dimensione)
    
    
    def calcolo_punteggio(self, simbolo):
        """
        calcola il punteggio per il simbolo dato esaminando tutte le linee del board
        -si scorrono tutte le linee del board
        -si calcolano i segmenti di simboli 
        -si sommano i punteggi totali sulla base dei segmenti di simboli 
        """
        punteggio_totale = 0
        for linea in self.get_tutte_linee():
            segmenti = get_segmenti_contigui(linea, simbolo)
            punteggio_totale += punteggio_linea(segmenti, self.mappa_punteggi)
        return punteggio_totale
    

    def aggiorna_punteggio(self):
        """
        aggiorna punteggio di ogni giocatore
        """
        for giocatore in self.giocatori:
            giocatore['score'] = self.calcolo_punteggio(giocatore['simbolo'])
    
    
    def check_vincitore(self):
        """
        verifica se un giocatore ha raggiungo il punteggio necessario per vincere
        """
        for giocatore in self.giocatori:
            if giocatore['score'] >= self.win_threshold:
                return giocatore
            
        return None
    
"""
funzioni per il funzionamento del computer nel gioco 
"""
def mossa_computer(game, player):
    celle_libere = []
    for i in range(game.dimensione):
        for j in range(game.dimensione):
            if game.board[i][j] == '.':
                celle_libere.append((i, j))

    if len(celle_libere) == 0:
        return None

    difficolta = player.get('difficolta', 'facile')

    if difficolta == 'facile':
        return random.choice(celle_libere)

    elif difficolta == 'difficile':
        miglior_mossa = None
        miglior_guadagno = -1000

        punteggio_attuale = calcolo_punteggio_board(game.board, player['simbolo'], game.dimensione, game.mappa_punteggi)

        for mossa in celle_libere:
            i = mossa[0]
            j = mossa[1]

            board_simulata = []
            for riga in game.board:
                nuova_riga = []
                for cella in riga:
                    nuova_riga.append(cella)
                board_simulata.append(nuova_riga)


            board_simulata[i][j] = player['simbolo']

            nuovo_punteggio = calcolo_punteggio_board(board_simulata, player['simbolo'], game.dimensione, game.mappa_punteggi)
            guadagno = nuovo_punteggio - punteggio_attuale

            if guadagno > miglior_guadagno:
                miglior_guadagno = guadagno
                miglior_mossa = (i, j)

        if miglior_mossa is not None:
            return miglior_mossa
        else:
            return random.choice(celle_libere)

    else:
        return random.choice(celle_libere)



"""
funzionamento modalità da riga di comando
"""
def run_cli():
    """
    modalità da linea di comando - command line interface
    -l'utente inserisce la dimensione della matrice di gioco (NxN), il numero di giocatori e per ogni giocatore fornisce:
        -umano o computer
        -nome del giocatore
        -simbolo
        -per giocatore computer si sceglie anche la difficolta
    -viene creato l'oggetto game contenente le informazioni e avviato il gioco
    -alternanza dei turni: per ogni turno, viene stampata la griglia attuale e i punteggi, 
       quindi viene chiesta la mossa al giocatore corrente
    -verifica della validità della mossa
    -aggiornamento della griglia e dei punteggi: la mossa viene applicata e, se un giocatore vince, 
       viene stampato il nome del vincitore e il gioco termina
    """
    
    print("Benvenuto nel gioco Filetto (modalità CLI)!")
    try:
        dimensione = int(input("Inserisci dimensione della matrice NxN: "))
    except ValueError:
        print("Valore non valido per la dimensione.")
        return

    try:
        k = int(input("Inserisci il numero di giocatori: "))
    except ValueError:
        print("Valore non valido per il numero di giocatori.")
        return
    

    giocatori = []
    for i in range(k):
        tipo = input(f"Giocatore {i+1}. è 'umano' o 'computer'? (u/c): ").strip().lower()
        nome = input(f"Inserisci il nome del giocatore {i+1}: ").strip()
        simbolo = input(f"Inserisci il simbolo per {nome} (es. x, 0, *): ").strip()
        if tipo == 'c' or tipo == 'computer':
            difficolta = input("Seleziona difficoltà per il computer (facile/difficile): ").strip().lower()
            if difficolta not in ['facile', 'difficile']:
                difficolta = 'facile'
            giocatori.append({
                'nome': nome,
                'simbolo': simbolo,
                'score': 0,
                'tipo': 'computer',
                'difficolta': difficolta
            })
        else:
            giocatori.append({
                'nome': nome,
                'simbolo': simbolo,
                'score': 0,
                'tipo': 'umano'
            })

    game = Game(dimensione, giocatori)
    
    while True: 
        game.stampa_board()
        game.aggiorna_punteggio()
        print("Punteggio:")
        for giocatore in game.giocatori:
            print(f"{giocatore['nome']}: {giocatore['score']} punti")
        
        vincitore = game.check_vincitore()
        if vincitore:
            print(f"Ha vinto {vincitore['nome']}!")
            break
        
        giocatore_corrente = game.giocatore_corrente()
        print(f"Turno di {giocatore_corrente['nome']} ({giocatore_corrente['simbolo']})")
        if giocatore_corrente['tipo'] == 'umano':
            mossa_input = input("Inserisci mossa (riga colonna, separate da spazio): ")
            try:
                r, c = map(int, mossa_input.split())
            except:
                print("Mossa non valida.")
                continue
        else:
            r, c = mossa_computer(game, giocatore_corrente)
            print(f"Il computer ({giocatore_corrente.get('difficolta', 'facile')}) ha scelto la mossa {r} {c}")
        
        if not game.mossa_valida(r,c):
            print("Mossa non valida o cella già occupata, Riprova.")
            continue
        game.mossa(r,c)
        game.prossimo_turno()

"""
funzionamento modalità grafica
"""       
def run_gui():
    """
    modalità grafica
    -gestisce l'interfaccia grafica di gioco, inclusa la creazione della finestra, della griglia di gioco e dei pulsanti
    -consente ai giocatori di interagire con la griglia tramite clic sui pulsanti, che corrispondono alle mosse del gioco
    -gestisce turni alternati tra giocatori umani e computer
    -controlla la validità delle mosse e aggiorna la griglia e il punteggio
    -aggiornamento della griglia e dei punteggi: la mossa viene applicata e, se un giocatore vince, 
       viene stampato il nome del vincitore e il gioco termina

    """
    if tk is None:
        print("Il modulo tkinter non è disponibile.")
        print("Verrà avviata la versione CLI")
        run_cli()
        return
        
    print("Modalità GUI attivata")
        
    try: 
        dimensione = int(input(" Inserisci dimensione della matrice NxN: "))
    except ValueError:
        print("Valore non valido per la dimensione.")
        return
        
    try:
        k = int(input(" Inserisci il numero di giocatori: "))
    except ValueError:
        print("Valore non valido per il numero di giocatori.")
        return
    
    giocatori = []
    for i in range(k):
        tipo = input(f"Giocatore {i+1} è 'umano' o 'computer'? (u/c): ").strip().lower()
        nome = input(f"Inserisci il nome del giocatore {i+1}: ").strip()
        simbolo = input(f"Inserisci il simbolo per {nome} (es. x, 0, *): ").strip()
        if tipo == 'c':
            difficolta = input("Seleziona difficoltà per il computer (facile/difficile): ").strip().lower()
            if difficolta not in ['facile', 'difficile']:
                difficolta = 'facile'
            giocatori.append({
                    'nome': nome,
                    'simbolo': simbolo,
                    'score': 0,
                    'tipo': 'computer',
                    'difficolta': difficolta
                })
        else: 
                giocatori.append({
                    'nome': nome,
                    'simbolo': simbolo,
                    'score': 0,
                    'tipo': 'umano'
                })
        
    game = Game(dimensione, giocatori)
    root = tk.Tk()
    root.title("Gioco Filetto")
        
    bottoni = [[None for _ in range(dimensione)] for _ in range(dimensione)]
    label_punteggio = tk.Label(root, text="Punteggio:", font=("Helvetica", 12))
    label_punteggio.grid(row=dimensione, column=0, columnspan=dimensione, pady=10)
        
    def aggiorna_board():
        """
        aggiorna la visualizzazione della griglia e dei punteggi nel gioco, aggiorna il testo dei bottoni con i valori correnti del game board
        aggiornna il puntegggio e verifica se c'è un vincitore, se si termina la partita
        """
        for i in range(dimensione):
            for j in range(dimensione):
                bottoni[i][j]['text'] = game.board[i][j]
        game.aggiorna_punteggio()
        testo_punteggio = "Punteggi:\n" + "\n".join([f"{g['nome']} ({g['simbolo']}): {g['score']}" for g in game.giocatori])
        label_punteggio.config(text=testo_punteggio)
        vincitore = game.check_vincitore()
        if vincitore:
            
            fine_partita(game, root, bottoni, vincitore)

           
    def click(i, j):
        """
        gestisce l'evento di clic su una cella della griglia, verifica se la mossa (i,j) è valida richiamando la funzione mossa_valida esegue la mossa
        aggiorna il board (aggiorna_board) e passa al turno successivo, se il giocatore è computer avvia mossa computer con delay di 0,35 secondi
        """
        giocatore_corrente = game.giocatore_corrente()
        if not game.mossa_valida(i, j):
            messagebox.showwarning("Mossa non valida", "Mossa non valida o cella occupata, Riprova.")
            return
        game.mossa(i, j)
        aggiorna_board()
        game.prossimo_turno()
            
        if game.giocatore_corrente()['tipo'] == 'computer':
                root.after(350, mossa_computer_gui)
    
    def mossa_computer_gui():
        corrente = game.giocatore_corrente()
        mossa = mossa_computer(game, corrente)
        if mossa is None:
            messagebox.showinfo("Pareggio, tabellone pieno")
            root.destroy()
            return 
        r, c = mossa
        game.mossa(r, c)
        aggiorna_board()
        game.prossimo_turno()
    
    for i in range(dimensione):
        for j in range(dimensione):
            btn = tk.Button(root, text=game.board[i][j], width=4, height=2,
                            font=("Helvetica", 14),
                            command=lambda i=i, j=j: click(i, j))
            btn.grid(row=i, column=j, padx=2, pady=2)
            bottoni[i][j] = btn

    root.mainloop()
              
def main():
    """
    main - avvio del gioco e scelta della modalità
    """
    print("----- Gioco Filetto -----")

    modalita = input("Scegli modalità di gioco: (1) CLI, (2) GUI: ").strip()
    if modalita == '2':
        run_gui()
    else:
        run_cli()

if __name__ == "__main__":
    main()
