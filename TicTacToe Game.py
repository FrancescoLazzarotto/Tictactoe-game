import random 

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = None
    
#Parametri di default: mappature dei punteggi per le sequenze

DEFAULT_MAP_PUNTEGGIO = {3: 2, 4: 10, 5: 50}

def get_segmenti_contigui(line, simbolo):
    """
    Data una lista (linea) e un simbolo, restituisce una lista con le lunghezze
    delle sequenze contigue del simbolo in quella linea.
    """
    segmenti = []
    count = 0
    for cella in line:
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
    Calcola il punteggio complessivo per una linea dato l'elenco delle lunghezze delle
    sequenze e la mappa dei punteggi.
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
    Dato un board e la sua dimensione, restituisce una lista di tutte le linee da controllare:
    - righe, colonne, diagonali e antidiagonali.
    """
    linee = []
    N = dimensione
    # Righe
    for r in range(N):
        linee.append(board[r])
    # Colonne
    for c in range(N):
        col = [board[r][c] for r in range(N)]
        linee.append(col)
    # Diagonali principali
    for k in range(N):
        diag1 = [board[i][i - k] for i in range(k, N)]
        if diag1:
            linee.append(diag1)    
        if k != 0:
            diag2 = [board[i - k][i] for i in range(k, N)]
            if diag2:
                linee.append(diag2)
    # Diagonali antidiagonali
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
    Calcola il punteggio per il simbolo dato lo stato del board passato come parametro.
    """
    punteggio_totale = 0
    for linea in get_linee_board(board, dimensione):
        segmenti = get_segmenti_contigui(linea, simbolo)
        punteggio_totale += punteggio_linea(segmenti, mappa_punteggi)
    return punteggio_totale

class FilettoGame:
    def __init__(self, dimensione, giocatori, mappa_punteggi=DEFAULT_MAP_PUNTEGGIO, win_threshold=50):
        """
        Inizializza il gioco con:
          - dimensione: lato della matrice NxN
          - giocatori: lista di dizionari contenenti { 'nome', 'simbolo', 'score', 'tipo' }
            (per i computer, è aggiunto anche 'difficolta')
          - score_map: mappa dei punteggi per lunghezze di sequenze
          - win_threshold: punteggio per vincere la partita
        """ 
        self.dimensione = dimensione
        self.board = [['.' for _ in range(dimensione)] for _ in range(dimensione)]
        self.giocatori = giocatori 
        self.mappa_punteggi = mappa_punteggi
        self.win_threshold = win_threshold
        self.turno = 0
        
        
    def stampa_board(self):
        """Stampa il tabellone in maniera formattata"""
        print("\nTabellone:")
        for riga in self.board:
            print(" ".join(riga))
        print()
        
    
    def mossa_valida(self, r, c):
        """Verifica se la mossa (r, c) è valida"""
        return 0 <= r < self.dimensione and 0 <= c < self.dimensione and self.board[r][c] == '.'
    
    
    def mossa(self, r, c):
        """Effettua la mossa per il giocatore corrente"""
        giocatore = self.giocatore_corrente()
        self.board[r][c] = giocatore['simbolo']
        
    
    def giocatore_corrente(self):
        """Restituisce il giocatore corrente"""
        return self.giocatori[self.turno]
    
    
    def prossimo_turno(self):
        """Passa il turno al giocatore successivo"""
        self.turno = (self.turno + 1) % len(self.giocatori)
        
    def get_all_lines(self):
        """
        Restituisce tutte le linee (righe, colonne, diagonali e antidiagonali) del board.
        """
        return get_linee_board(self.board, self.dimensione)
    
    def calcolo_punteggio(self, simbolo):
        """
        Calcola il punteggio per il simbolo dato esaminando tutte le linee del board.
        """
        punteggio_totale = 0
        for linea in self.get_all_lines():
            segmenti = get_segmenti_contigui(linea, simbolo)
            punteggio_totale += punteggio_linea(segmenti, self.mappa_punteggi)
        return punteggio_totale

    def aggiorna_punteggio(self):
        """Aggiorna punteggio di ogni giocatore"""
        for giocatore in self.giocatori:
            giocatore['score'] = self.calcolo_punteggio(giocatore['simbolo'])
    
    
    def check_vincitore(self):
        """Verifica se un giocatore ha raggiungo il punteggio necessario per vincere"""
        for giocatore in self.giocatori:
            if giocatore['score'] >= self.win_threshold:
                return giocatore
            
        return None

def mossa_computer(game, player):
    """
    Restituisce la mossa (r, c) scelta dal computer in base alla difficoltà:
      - "facile": scelta casuale
      - "medio": mossa che massimizza il guadagno immediato in punti
      - "difficile": mossa che massimizza il guadagno immediato riducendo al contempo il potenziale vantaggio per l'avversario
    """  
    celle_libere = [(i,j) for i in range(game.dimensione) for j in range(game.dimensione) if game.board[i][j] == '.']
    if not celle_libere:
        return None
    diff = player.get('difficolta', 'facile')
    if diff == 'facile':
        return random.choice(celle_libere)
    elif diff == 'medio':
        miglior_mossa = None
        miglior_delta = -float('inf')
        punteggio_attuale = calcolo_punteggio_board(game.board, player['simbolo'], game.dimensione, game.mappa_punteggi)
        for mossa in celle_libere:
            simulated_board = [row[:] for row in game.board]
            simulated_board[mossa[0]][mossa[1]] = player['simbolo']
            nuovo_punteggio = calcolo_punteggio_board(simulated_board, player['simbolo'], game.dimensione, game.mappa_punteggi)
            delta = nuovo_punteggio - punteggio_attuale
            if delta > miglior_delta:
                miglior_delta = delta
                miglior_mossa = mossa
        return miglior_mossa if miglior_mossa is not None else random.choice(celle_libere)
    elif diff == 'difficile':
        miglior_mossa = None
        miglior_eval = -float('inf')
        punteggio_attuale = calcolo_punteggio_board(game.board, player['simbolo'], game.dimensione, game.mappa_punteggi)
        
        avversari = [g for g in game.giocatori if g['simbolo'] != player['simbolo']]
        punteggio_avversario = {avv['simbolo']: calcolo_punteggio_board(game.board, avv['simbolo'], game.dimensione, game.mappa_punteggi) for avv in avversari}
        for mossa in celle_libere:
            simulated_board = [row[:] for row in game.board]
            simulated_board[mossa[0]][mossa[1]] = player['simbolo']
            nuovo_punteggio = calcolo_punteggio_board(simulated_board, player['simbolo'], game.dimensione, game.mappa_punteggi)
            delta = nuovo_punteggio - punteggio_attuale
            
            #val potenziale guadagno degli avversarsi se avessero giocato in quella cella 
            avv_max_delta = 0
            for avv in avversari:
                avv_sim_board = [row[:] for row in game.board]
                avv_sim_board[mossa[0]][mossa[1]] = avv['simbolo']
                avv_nuovo_punteggio = calcolo_punteggio_board(avv_sim_board, avv['simbolo'], game.dimensione, game.mappa_punteggi)
                avv_delta = avv_nuovo_punteggio - punteggio_avversario[avv['simbolo']]
                if avv_delta > avv_max_delta:
                    avv_max_delta = avv_delta
            eval = delta - avv_max_delta
            if eval > miglior_eval:
                miglior_eval = eval
                miglior_mossa = mossa
        return miglior_mossa if miglior_mossa is not None else random.choice(celle_libere)
    else: 
        return random.choice(celle_libere)
    
# Modalità da linea di comando (CLI)
def run_cli():
    print("Benvenuto nel gioco Filetto (modalità CLI)!")
    try:
        dimensione = int(input("Inserisci dimensione della matrice NxN: "))
    except:
        print("Valore non valido per la dimensione.")
        return

    try:
        k = int(input("Inserisci il numero di giocatori: "))
    except:
        print("Valore non valido per il numero di giocatori.")
        return

    giocatori = []
    for i in range(k):
        tipo = input(f"Giocatore {i+1}. è 'umano' o 'computer'? (u/c): ").strip().lower()
        nome = input(f"Inserisci il nome del giocatore {i+1}: ").strip()
        simbolo = input(f"Inserisci il simbolo per {nome} (es. x, 0, *): ").strip()
        if tipo == 'c':
            difficolta = input("Seleziona difficoltà per il computer (facile/medio/difficile): ").strip().lower()
            if difficolta not in ['facile', 'medio', 'difficile']:
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

    game = FilettoGame(dimensione, giocatori)
    
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
        
def run_gui():
    if tk is None:
        print("Il modulo tkinter non è disponibile.")
        print("Verrà avviata la versione CLI")
        return
        
    print("Modalità GUI attivata")
        
    try: 
        dimensione = int(input(" Inserisci dimensione della matrice NxN: "))
    except:
        print("Valore non valido per la dimensione.")
        return
        
    try:
        k = int(input(" Inserisci il numero di giocatori: "))
    except:
        print("Valore non valido per il numero di giocatori.")
        return
        
    giocatori = []
    for i in range(k):
        tipo = input(f"Giocatore {i+1} è 'umano' o 'computer'? (u/c): ").strip().lower()
        nome = input(f"Inserisci il nome del giocatore {i+1}: ").strip()
        simbolo = input(f"Inserisci il simbolo per {nome} (es. x, 0, *): ").strip()
        if tipo == 'c':
            difficolta = input("Seleziona difficoltà per il computer (facile/medio/difficile): ").strip().lower()
            if difficolta not in ['facile', 'medio', 'difficile']:
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
        
    game = FilettoGame(dimensione, giocatori)
    root = tk.Tk()
    root.title("Gioco Filetto")
        
    bottoni = [[None for _ in range(dimensione)] for _ in range(dimensione)]
    label_punteggio = tk.Label(root, text="Punteggio:", font=("Helvetica", 12))
    label_punteggio.grid(row=dimensione, column=0, columnspan=dimensione, pady=10)
        
    def aggiorna_board():
        for i in range(dimensione):
            for j in range(dimensione):
                bottoni[i][j]['text'] = game.board[i][j]
        game.aggiorna_punteggio()
        testo_punteggio = "Punteggi:\n" + "\n".join([f"{g['nome']} ({g['simbolo']}): {g['score']}" for g in game.giocatori])
        label_punteggio.config(text=testo_punteggio)
        vincitore = game.check_vincitore()
        if vincitore:
            messagebox.showinfo("Vittoria", f"Ha vinto {vincitore['nome']} con {vincitore['score']} punti!")
            root.destroy()
            
    def click(i, j):
        giocatore_corrente = game.giocatore_corrente()
        if not game.mossa_valida(i, j):
            messagebox.showwarning("Mossa non valida", "Mossa non valida o cella occupata, Riprova.")
            return
        game.mossa(i, j)
        aggiorna_board()
        game.prossimo_turno()
            
        if game.giocatore_corrente()['tipo'] == 'computer':
                root.after(500, mossa_computer_gui)
    
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
    print("----- Gioco Filetto -----")

    modalita = input("Scegli modalità di gioco: (1) CLI, (2) GUI: ").strip()
    if modalita == '2':
        run_gui()
    else:
        run_cli()

if __name__ == "__main__":
    main()
