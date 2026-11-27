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

Oggi il server espone quattro strumenti in sola lettura (verifica dell'accesso, elenco degli impianti, elenco delle luci, stato di una luce) su un impianto simulato. L'adattatore verso le KNX IoT 3rd Party API è ancora da implementare.

## Tecnologie

- Python 3.14.
- FastMCP 4.2.0 per il server e il client MCP, con la versione fissata in `pyproject.toml`.
- Docker e Docker Compose.
- pytest, pytest-cov e ruff per i test, la copertura e il controllo dello stile.

## Avvio del PoC

### Con Docker

```bash
docker compose up --build
```

Il server MCP risponde su `http://localhost:8000/mcp` e usa un impianto simulato con tre luci. Per cambiare la configurazione si copia `config.env.example` in `config.env` e lo si modifica: `config.env` è escluso da git e dall'immagine Docker.

### Senza Docker, per lo sviluppo

Serve Python 3.14.

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
aura-server
```

In un altro terminale, con lo stesso ambiente attivo, il client MCP da riga di comando chiama gli strumenti del server:

```bash
aura-client tools
aura-client call list_installations
aura-client call list_lights --arg installation_id=kit-demo
aura-client call get_light_state --arg installation_id=kit-demo --arg light_id=luce-1
```

### Controlli e test

```bash
ruff check .
ruff format --check .
pytest
```

`pytest` misura anche la copertura e fallisce sotto il 75%, la soglia minima del capitolato. Gli stessi controlli, più la build dell'immagine Docker, li esegue la GitHub Action **CI** a ogni pull request.

## Struttura del codice

```
src/aura/
├── server.py         server MCP: gli strumenti esposti al servizio AI
├── gateway.py        interfaccia verso l'impianto, l'unica da cui dipende il server
├── fake_gateway.py   impianto simulato in memoria, per lo sviluppo e i test
├── knx_gateway.py    adattatore verso le KNX IoT 3rd Party API (da implementare)
├── bootstrap.py      sceglie l'implementazione in base ad AURA_BACKEND
├── config.py         configurazione dalle variabili d'ambiente
├── domain.py         modello: impianti, luci, stato delle luci
├── errors.py         errori del dominio
├── client.py         client MCP da riga di comando (aura-client)
└── __main__.py       avvio del server (aura-server)
tests/                test con pytest
```

Il server riceve l'implementazione dell'impianto dall'esterno (dependency injection): per passare dall'impianto simulato a quello reale basta cambiare `AURA_BACKEND` in `config.env`.

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
