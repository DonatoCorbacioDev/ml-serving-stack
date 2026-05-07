# Docker Week 2 — Volumi, Networking e Compose

## Obiettivo

Capire come condividere dati persistenti tra container
e orchestrare più servizi Docker tramite Compose.

Il progetto utilizza:

- un container di training
- un container API FastAPI
- un artifact ML condiviso (`model.joblib`)

Workflow:

```text
training container
↓
model.joblib
↓
API container
↓
prediction endpoint
```

---

# Concetti principali studiati

- Bind mount
- Persistenza dati
- Artifact ML
- Container filesystem
- Docker Compose
- Port mapping
- Read-only mount
- API serving
- Networking base Docker

---

# Persistenza del modello

Il training container salva il modello ML in:

```text
/data/models/model.joblib
```

Senza volumi Docker, il file esisterebbe solo
nel filesystem interno del container.

Quando il container termina, il file verrebbe eliminato.

Per evitare questo problema è stato utilizzato un bind mount.

---

# Bind mount

Comando utilizzato:

```bash
docker run --rm \
  -v $(pwd)/data/models:/data/models \
  ml-training \
  python train.py --output-dir /data/models
```

Il bind mount collega:

```text
HOST (PC locale)
$(pwd)/data/models
```

con:

```text
CONTAINER
/data/models
```

In questo modo il file `model.joblib`
rimane persistente sul filesystem locale
anche dopo la terminazione del container.

---

# Artifact ML

Il file:

```text
model.joblib
```

rappresenta un artifact ML:

- modello serializzato
- output del training
- riutilizzabile dall'API

Questo permette di separare:

- training
- serving

in due container distinti.

---

# API FastAPI

L'API carica il modello salvato
e fornisce endpoint REST per inferenza.

Endpoint implementati:

```text
/health
/predict
/docs
```

---

# Read-only mount

L'API monta il volume in modalità read-only:

```text
:ro
```

Esempio:

```bash
-v $(pwd)/data/models:/data/models:ro
```

Questo permette all'API di leggere il modello
senza poterlo modificare.

Vantaggi:

- maggiore sicurezza
- isolamento migliore
- riduzione errori accidentali

---

# Docker Compose

Docker Compose permette di orchestrare
più servizi Docker tramite un singolo file YAML.

File utilizzato:

```text
docker-compose.yml
```

Servizi definiti:

- training
- api

---

# docker-compose.yml

```yaml
services:
  training:
    build:
      context: ./training
    image: ml-training
    volumes:
      - ./data/models:/data/models
    profiles:
      - train
    command: python train.py --output-dir /data/models

  api:
    build:
      context: ./api
    image: ml-api
    ports:
      - "8000:8000"
    volumes:
      - ./data/models:/data/models:ro
```

---

# Comandi utilizzati

Training:

```bash
docker compose --profile train run --rm training
```

Avvio API:

```bash
docker compose up api
```

Healthcheck:

```bash
curl http://localhost:8000/health
```

Prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Documentazione FastAPI:

```text
http://localhost:8000/docs
```

---

# Networking Docker

Docker Compose crea automaticamente
una rete bridge interna dedicata al progetto.

I container possono comunicare
tramite il nome del servizio
senza usare indirizzi IP manuali.

---

# Differenza tra image e container

Image:

```text
template immutabile
```

Container:

```text
istanza in esecuzione dell'image
```

---

# Differenza tra bind mount e volume Docker

Bind mount:

- collega cartelle reali del filesystem host
- utile in sviluppo
- visibile direttamente sul PC

Volume Docker:

- gestito da Docker
- più isolato
- più comune in produzione

---

# Domande finali Week 2

## Perché l'API monta il volume in modalità `:ro` (read-only)?

L'API deve soltanto leggere il file `model.joblib`
per eseguire inferenza.

Montare il volume in modalità read-only:

```text
:ro
```

impedisce modifiche accidentali al modello.

Vantaggi:

- maggiore sicurezza
- migliore isolamento
- protezione degli artifact ML
- riduzione del rischio di corruzione dati

---

## Cosa succede al modello se eseguo `docker compose down -v`? E senza `-v`?

Comando:

```bash
docker compose down
```

ferma e rimuove i container,
ma mantiene i volumi Docker.

Gli artifact persistenti rimangono disponibili.

Comando:

```bash
docker compose down -v
```

rimuove anche i volumi Docker associati.

In quel caso i dati persistenti vengono eliminati.

Nel progetto attuale viene utilizzato un bind mount
(`./data/models:/data/models`),
quindi il modello rimane comunque salvato
sul filesystem locale del PC.

---

## Come fanno due container a parlarsi per nome invece che per IP?

Docker Compose crea automaticamente
una rete bridge interna.

Ogni servizio Compose diventa automaticamente
un hostname DNS interno.

Esempio:

```yaml
services:
  api:
  db:
```

Il container `api`
può comunicare con `db`
usando semplicemente:

```text
db
```

come hostname,
senza conoscere l'indirizzo IP reale.

Questo semplifica networking e orchestrazione
tra servizi containerizzati.

---

# Architettura finale Week 2

```text
training container
↓
model.joblib (persistente)
↓
FastAPI container
↓
/predict endpoint
```

Il sistema separa:

- training
- artifact persistence
- inference serving

utilizzando container Docker indipendenti
orchestrati tramite Docker Compose.

---

# Limiti attuali

Il modello viene caricato ad ogni richiesta
nell'endpoint `/predict`.

Questo approccio è semplice per apprendimento,
ma non è ottimale in produzione.

In sistemi reali il modello viene normalmente
caricato una sola volta all'avvio dell'API
e mantenuto in memoria.

---

# Osservazioni importanti

Il progetto ora implementa
un workflow ML containerizzato realistico:

```text
training
↓
artifact persistence
↓
API serving
↓
prediction endpoint
```

Questo rappresenta una base concreta
per deployment, CI/CD e MLOps basics.