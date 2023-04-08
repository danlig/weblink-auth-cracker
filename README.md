# Descrizione breve
Si propone di individuare la password di un sito web che usa il sistema di autenticazione client-side specificato in: https://www.web-link.it/scripting/B4_passwordmultiple.htm

# Descrizione analitica
## Funzionamento del sistema
Il sistema di autenticazione è basato su uno script di autenticazione client-side "pswd.js" che contiene, hard-coded, l'hash delle password. Nel momento del login, si verifica l'hash della password inserita dall'utente e, se corretta, si viene reindirizzati ad una pagina html situata in un path nascosto. Quest'ultimo è calcolato con una funzione di encoding custom sulla password stessa.

## Analisi
Dopo varie analisi, è stato effettuato il reverse-engineering del codice di generazione dell'hash e dell'encoder. Si può notare come ci siano innumerevoli collisioni: password anche di diversa lunghezza/forma con lo stesso hash. Trovare password che collidono è banale come dimostrato dallo script in allegato. Tuttavia, il problema principale è individuare la giusta password da cui si ricava, data in input all'encoder, il corretto path segreto.

## Conclusioni
Il metodo più sensato e semplice per lo scopo proposto è il bruteforcing delle path utilizzando una wordlist di possibili password il cui hash corrisponde. Dunque, l'autenticazione presa in analisi si presenta vulnerabile a questo tipo di attacchi e, in particolar modo, per password deboli.
