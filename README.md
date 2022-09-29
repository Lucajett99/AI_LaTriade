#Progetto Intelligenza Artificiale
##Dropout Accademico
##Gruppo: La Triade
###Marco Benito Tomasone
###Luca Genova
###Simone Boldrini
###2021-2022


emphDropout è un termine con il quale vengono indicati i ragazzi che
decidono di abbandonare un percorso di studio prima della fine dello
stesso. Il fenomeno del Dropout può avere ripercussioni molto importanti
sulla vita dello studente ed è anche un fenomeno economicamente
rilevante nella vita delle università. L'Alma Mater Studiorum -
Università di Bologna ha raccolto i dati degli iscritti dal 2016 al 2018
per effettuare una ricerca relativa al fenomeno di abbandono degli
studi. Lo studio ha lo scopo di andare a valutare se è possibile predire
l'abbandono degli studi da parte di uno studente in modo tale da
proporre agli studenti delle misure a sostegno di essi (come corsi di
potenziamento) per aiutare i ragazzi ed evitare il fenomeno del Dropout.
Il lavoro proposto vuole valutare la possibilità di predire
anticipatamente in vari momenti la possibilità che uno studente
abbandoni gli studi. I momenti principali sui quali ci andremo a
concentrare saranno tre

1.  Al momento dell'immatricolazione, non tenendo quindi conto degli
    esami svolti durante l'anno, ma considerando solo i dati personali
    ed economici del ragazzo ed eventuali OFA

2.  Dopo la sessione invernale del primo anno, quindi considerando gli
    esami svolti al primo Marzo

3.  Dopo il primo anno di corso, considerando quindi tutti gli esami
    svolti durante il primo anno di corso.

Questo ci permetterà di andare a valutare con che grado di accuratezza
sarà possibile andare a predire la possibilità dell'abbandono da parte
di uno studente durante il suo primo anno di studi, per cercare tramite
delle misure di sostegno al ragazzo di scongiurare il fenomeno. Abbiamo
per i tre momenti precedentemente descritti utilizzato tre modelli di
Machine Learning diversi la emphRegressione Logistica (LR), il
emphRandom Forest (RF) e la emphSupport Vector Machine (SVM). Abbiamo
inoltre provato a combinare i risultati di questi tre modelli tramite lo
emphStacking Algorithm.

