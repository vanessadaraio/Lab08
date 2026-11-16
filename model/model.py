from database.distributore_DAO import DistributoreDAO
from model.distributore_DTO import Distributore
from model.prezzo_DTO import Prezzo

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        risultato=[] # creo una lista vuota
        for distributore in self._distributori: #scorro i distributori
            prezzi=distributore.get_prezzi() # recupero i prezzi
            somma=0
            conteggio=0

            for prezzo in prezzi:
                if prezzo.data.month==mese: # seleziono quelli del mese richiesto
                    somma+=prezzo.prezzo_litro
                    conteggio+=1

            if conteggio >0:
                media=somma/conteggio
            else:
                media=0

            risultato.append((distributore.nome, media))  #inserisco una tupla (nome,media) nella lista
        return risultato

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno==8: # caso terminale
            if self.__costo_ottimo==-1 or costo_corrente< self.__costo_ottimo:
                self.__costo_ottimo=costo_corrente
                self.__sequenza_ottima=sequenza_parziale.copy()
            return

        #provo tutti i distributori
        for id_distributore in prezzi_settimana:
            prezzo=prezzi_settimana[id_distributore][giorno -1]
            costo_giorno= prezzo * 100

            #costo dello spostamento
            if ultimo_distributore is not None and ultimo_distributore != id_distributore:
                costo_giorno+=5

            #aggiungo il distributore alla sequenza
            sequenza_parziale.append(id_distributore)

            #chiamata ricorsiva
            self.__ricorsione(sequenza_parziale,
                              giorno +1,
                              id_distributore,
                              costo_corrente + costo_giorno,
                              prezzi_settimana
                              )
            sequenza_parziale.pop() # elimina l'ultima scelta per poter provare l'altra possibilita




    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        risultato={}
        for distributore in self._distributori:
            prezzi=distributore.get_prezzi()

            lista_prezzi=[None]*7
            for prezzo in prezzi:
                if prezzo.data.month==mese and 1<=prezzo.data.day<=7: #selezioniamo i prezzi del mese richiesto e selezioniamo i primi 7 giorni
                    lista_prezzi[prezzo.data.day-1]=prezzo.prezzo_litro
            risultato[distributore.id]=lista_prezzi

        return risultato