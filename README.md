# AURA – AI for Understanding, Reasoning and Automation

Repository del codice di **AURA**, realizzato dal gruppo **5ive Stars** (Gruppo 5) per il capitolato C1 proposto da Vimar S.p.A., nel progetto didattico di Ingegneria del Software dell'Università degli Studi di Padova, A.A. 2026/2027.

## Il prodotto

AURA permette a un servizio di intelligenza artificiale basato su LLM di interagire con un impianto domotico residenziale Vimar: l'utente chiede in linguaggio naturale, per esempio, lo stato di un ambiente o l'accensione di una luce, e il servizio AI esegue la richiesta sull'impianto.

Il cuore del progetto è un server MCP (Model Context Protocol), con il relativo client, che rende lo standard KNX IoT 3rd Party API (v2.1.0) utilizzabile dai servizi AI. L'accesso all'impianto avviene con l'account MyVimar dell'utente, tramite OAuth2.

Il capitolato prevede tre componenti:

1. un'infrastruttura cloud-ready basata su Docker e Docker Compose, che si avvia con un solo comando e si configura con un file di variabili d'ambiente;
2. il server MCP e il client MCP, che si interfacciano con le KNX IoT 3rd Party API;
3. un agente o modello AI esterno collegato al server MCP.

Il prodotto si prova con un kit portatile di impianto View Wireless fornito da Vimar.

## Stato del progetto

Il gruppo lavora alla prima revisione di avanzamento, la Requirements and Technology Baseline (RTB), prevista entro il 2027-01-15. Per la RTB realizza un Proof of Concept (PoC) sui casi base: accesso all'impianto, elenco degli impianti e stato di una luce.

Le istruzioni di installazione e di primo utilizzo saranno aggiunte a questo README insieme al codice del PoC.

## Documentazione di progetto

La documentazione del gruppo è pubblicata nel repository [5ivestars/docs](https://github.com/5ivestars/docs) e sul sito https://5ivestars.github.io/docs/.

## Regole per chi contribuisce

- Le regole di lavoro del gruppo (rami, commit, pull request e verifica) sono definite nelle Norme di Progetto.
- Credenziali, token e dati di accesso all'impianto non vanno mai inseriti nel repository, né nel codice né nei commit: si configurano solo nel file di variabili d'ambiente, e il file con i valori reali resta escluso dal versionamento.

## Gruppo

5ive Stars – Gruppo 5: Niccolò Bassan, Sofia Bortolotto, Lorenzo Cisco, Enrico Esperti, Laura Granese, Alessandro Monni, Eric Vanzetto.

## Licenza

Il codice è distribuito con licenza MIT: vedi il file [LICENSE](LICENSE).

## Contatti

5ive.stars.swe@gmail.com
