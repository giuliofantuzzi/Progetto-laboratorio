"""
////////////////////////////////////////////////////////////////////////////////
>>Laboratorio di Programmazione, progetto d'esame
>>Corso di laurea: Statistica
>>Autore: Fantuzzi Giulio (id: EC2100728)
>>Data consegna: 09/02/2021
>>Contatto: GIULIO.FANTUZZI@studenti.units.it
////////////////////////////////////////////////////////////////////////////////
"""
################################################################################
#Classe per la gestione degli errori
class ExamException(Exception):
    pass
################################################################################
#Classe serie storica
class CSVTimeSeriesFile():
    #----------------------------------------------------------------------------
    #istanzio la classe sul nome
    #metto di default None per gestire il caso in cui il nome non venga inserito
    def __init__(self,name=None):
        self.name=name
    #----------------------------------------------------------------------------
    #metodo che ritorna una lista di liste del tipo
    #lista= [...,...,[epoch,temperature],...,...]
    def get_data(self):
        lista_dati = []#lista in cui memorizzo i dati del file data.csv

        #***ECCEZIONI funzione get_data()***
        #provo ad aprire il file con i dati
        #CASO 1: non ho inserito il nome del file
        if self.name is None:
            raise ExamException('>> file csv non inserito!')
        #CASO 2: ho inserito il parametro,ma non e' stringa
        if not isinstance(self.name,str):
            raise ExamException('>> il nome del file csv deve essere stringa!')
        #CASO 3: ho inserito il nome del file...provo(try) ad aprirlo
        try:
            my_file = open(self.name, 'r')#modalita' lettura dei dati
        except:
            raise ExamException('>> file csv inesistente. Impossibile aprirlo!')
            #NB:se non apre il file non fa neanche il resto!

        #Ok,il file esiste. Leggo linea per linea
        for line in my_file:
            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')
            #NB:se non c'e'una virgola, elements e' una lista di 1 elemento solo
            #considero la linea solo se dopo lo split ci sono due elementi
            if len(elements)==2:
                # SETTAGGIO epoch e temperature
                epoch  = elements[0]
                temperature = elements[1]
                try:
                    # CONVERSIONE epoch e temperature da specifiche
                    #epoch deve essere int. Se e' float devo convertirlo ad int
                    #NB: nel file csv epoch e' una stringa
                    #prima converto a float,poi posso fare il cast ad int()
                    epoch = int(float(epoch))
                    #temperature dev'essere numerico,non importa se int o float
                    #NB: converto a float,dato che i float contengono gli int
                    temperature= float(temperature)
                except:
                    #se la conversione non avviene continuo, senza alzare eccezioni
                    continue
                #ora viene valutato il tipo di carattere
                #se il tipo e' idoneo viene inserito, altrimenti si va al prossimo
                #in questo modo non vengono alzate eccezioni,come da consegna
                if (isinstance(temperature,int)or isinstance(temperature,float) ) and temperature!=0:
                    #creo una lista temporanea in cui inserire epoch e temperature
                    lista_da_aggiungere=[]
                    lista_da_aggiungere.append(epoch)
                    lista_da_aggiungere.append(temperature)
                    #aggiungo la lista temporanea alla lista iniziale
                    #Prima di aggiungerla verifico se puo' essere inserita. 2 vincoli:
                    #1)serie temporale ordinata (un epoch non puo' essere > del successivo)
                    #2)non devono esserci duplicati tra gli echo
                    #Questo puo' essere riassunto in una sola condizione: epoch>epoch precedente
                    #ATTENTO!AL PRIMO GIRO NON C'E' UN EPOCH precedente
                    if not lista_dati: #se lista_dati e' ancora vuota
                        lista_dati.append(lista_da_aggiungere)
                    else:
                        lista_precedente=lista_dati[-1]
                        #NB: lista precedente e' del tipo [epoch,temperature]
                        #facendo lista_precedente[0] accedo a epoch
                        if not epoch>lista_precedente[0]:
                            raise ExamException('>> timestamp fuori ordine o duplicato! Il valore non rispetta le specifiche(epoch <= al precedente.)')
                        else:
                            lista_dati.append(lista_da_aggiungere)
            else:#se la lunghezza della riga non e' 2
                continue #salta la riga,senza alzare eccezioni
        #chiudo il file
        my_file.close()
        #ULTIMO CHECK:E se il file CSV che ho importato fosse vuoto?
        #oppure se non fosse vuoto, ma non contenesse valori validi?
        #il programma funzionerebbe, e get_data ritornerebbe una lista vuota
        #Non avrebbe senso continuare con una lista vuota, scelgo io di alzare un'eccezione
        if not lista_dati:#lista vuota
            raise ExamException('>> nessun dato importato: file vuoto o nessun valore accettabile')
        #ritorno la lista con dentro le liste del tipo[epoch,temperature]
        return lista_dati
    #----------------------------------------------------------------------------

################################################################################

#======================
# Corpo del programma
#======================

################################################################################
#Funzione per le statistiche giornaliere
def daily_stats(time_series=None):
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #ECCEZIONI funzione daily_stats():
    #1)argomento della funzione non inserito
    if time_series is None: #ecco perche' sopra avevo posto di default time_series=None
        raise ExamException (">> parametro daily_stats non inserito!")
    #2)argomento non e' una lista
    if not isinstance(time_series,list):
        raise ExamException(">> parametro daily_stats inserito, ma non e' una lista!")
    #3)argomento e' di tipo lista, ma e'una lista vuota
    if not time_series:
        raise ExamException (">> inserita una lista vuota in daily_stats!")
    #4)controllo il tipo di elementi che contiene la lista
    #NB:la lista in input e' una lista di liste!
    for item in time_series:
        if not isinstance(item,list):
            raise ExamException('>> daily_stats deve ricevere in input una lista di liste')
    #5)la lista e' effettivamente una lista di liste
    #pero' la lunghezza delle sottoliste deve essere 2
    #ricordo che le "sottoliste" erano del tipo [epoch,temperature]
    for item in time_series:
        if isinstance(item,list) and len(item) !=2:
            raise ExamException('>> le sottoliste non sono di 2 elementi come richiesto')
    #6)OK,supponiamo che le sottoliste abbiano lunghezza 2
    #Nella classe CSVTimeSeriesFile  mi assicuravo che epoch e temperature fossero adatti
    #Se in daily_stats()inserisco una lista casuale potrebbero esserci problemi di tipo!
    #vincoli: item[0] sono epoch-->interi, ordinati, non duplicati
    #item[1] e' una temperatura-->numerico, non deve essere vuoto o nullo
    #NB:Nella classe gestivo questi errori mentre li importavo
    #Qui nella funione decido di considerarli UNRECOVERABLE
    for i in range(len(time_series)):
        #Controllo vincoli epoch
        if isinstance(time_series[i][0],float):#se epoch float
            time_series[i][0]= int(time_series[i][0])#allora converto
        #a questo punto se epoch non e' intero non va bene
        if not isinstance(time_series[i][0],int):
            raise ExamException('>> ho trovato un epoch non numerico!')
        if i>0:#ovviamente il primo epoch non mi da problemi di ordinamento
            if not time_series[i][0]> time_series[i-1][0]:
                raise ExamException('>> epoch non ordinati o duplicati!')
        #Controllo vincoli temperature
        if not (isinstance(time_series[i][1],int) or isinstance(time_series[i][1],float)):
            raise ExamException('>> temperatura non numerica: non accettabile!')
        if time_series[i][1]==0:
            raise ExamException('>> temperatura nulla: non accettabile!')
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #Passiamo alla funzione vera e propria
    #inizializzo una lista vuota dove man mano si inseriscono le statistiche giornaliere
    lista_statistiche_totale=[]#questo sara' l'output
    #dal time_series prendo solo gli epoch
    #attraverso epoch-epoch%86400 ottengo l'inizio del giorno
    #cosi e' piu' facile vedere se due epoch sono nello stesso giorno
    #se epoch1 e epoch 2 nello stesso giorno, allora epoch1-epoch1%86400 = epoch2-epoch2%86400
    #-------------------------------------------------
    lista_giorni=[]
    for item in time_series:
        lista_giorni.append(item[0]-(item[0]%86400))
    #-------------------------------------------------
    i=0#indice che uso per muovermi in lista_giorni
    while i<len(lista_giorni):
        #creo lista in cui inserire le temperature del giorno
        #ci metto gia' il primo valore del giorno corrente
        lista_temperature=[time_series[i][1]]
        #lista in cui poi inseriro' i valori di min/max/media
        statistiche_giornaliere=[]
        j=i+1#fissato il giorno i-esimo,parto dal giorno successivo
        #confronto per vedere se giorno j-esimo==giorno i-esimo
        giorno_successivo=False#variabile che diventa vera appena cambio giorno
        while j<len(lista_giorni) and giorno_successivo is False:
            if lista_giorni[j]==lista_giorni[i]:
                lista_temperature.append(time_series[j][1])
                j+=1
            else:
                #lista_giorni[j] appartiene al giorno successivo
                i=j#cosi' lista_giorni[i] sara' il primo nuovo giorno
                giorno_successivo=True
                #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                #calcolo le statistiche giornaliere
                minimo=min(lista_temperature)
                massimo=max(lista_temperature)
                media=sum(lista_temperature)/len(lista_temperature)
                statistiche_giornaliere=[minimo,massimo,media]
                #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                #aggiungo le statistiche giornaliere alla lista_statistiche
                lista_statistiche_totale.append(statistiche_giornaliere)

        #Caso in cui sono arrivato all'ultimo elemento di lista_giorni
        #non potevo usare il while sopra:l'ultimo elemento non ha un successivo!
        if j==len(lista_giorni):
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            #calcolo le statistiche giornaliere
            minimo=min(lista_temperature)
            massimo=max(lista_temperature)
            media=sum(lista_temperature)/len(lista_temperature)
            statistiche_giornaliere=[minimo,massimo,media]
            #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            #aggiungo le statistiche giornaliere alla lista_statistiche
            lista_statistiche_totale.append(statistiche_giornaliere)
            i=j

    return lista_statistiche_totale
################################################################################

#Ora testo le classi e la funzione che ho implementato
#--------------------------------------------------------------------------------
try:
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # I) Importo i dati dal file data.csv
    print('\n...apertura del file csv in corso...\n')
    time_series_file = CSVTimeSeriesFile("data.csv")
    time_series=time_series_file.get_data()
    #time_series e' una lista di liste del tipo [epoch,temperature]
    #i dati importati potrebbero essere(e sono) tanti:non li stampo tutti.
    #dico solo che l'operazione e' avvenuta e il numero di dati importati
    print('>> Operazione avvenuta con successo!')
    print('>> Rilevazioni importate: {}'.format(len(time_series)))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # II) Chiamata della funzione daily_stats
    print('\n...analizzo i dati...\n')
    statistiche=daily_stats(time_series)
    #il return di daily_stats e' una lista di liste del tipo [Tmin,Tmax,Tmedia]
    #stampo in modo ordinato le statistiche giornaliere()
    stringa= '>>Stampa delle statistiche giornaliere:'
    print(stringa)
    print('-'*len(stringa))
    print('T min \t T max \t  T media')
    print('-'*len(stringa))
    for item in statistiche:
        #per un output piu' uniforme,stampo solo due cifre decimali
        print('{:.2f} \t {:.2f} \t  {:.2f}'.format(item[0],item[1],item[2]))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
except ExamException as e:
    print("\nOPS, qualcosa e' andato storto:\n{}".format(e))
#--------------------------------------------------------------------------------
