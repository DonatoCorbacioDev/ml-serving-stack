# Docker Week 2 — Volumi, Networking e Compose

## Obiettivo

Capire come condividere dati persistenti tra container
e orchestrare più servizi Docker tramite Docker Compose.

Il progetto utilizza:

- un container di training
- un container API FastAPI
- un artifact ML condiviso (`model.joblib`)

---

# Architettura Week 2

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

tramite container Docker indipendenti.

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
- Networking Docker

---

# Persistenza artifact

Il training container salva il modello ML in:

```text
/data/models/model.joblib
```

Senza volumi Docker,
il file esisterebbe solo
nel filesystem interno del container.

Quando il container termina,
il file verrebbe eliminato.

Per mantenere persistente il modello
è stato utilizzato un bind mount.

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
HOST
$(pwd)/data/models
```

con:

```text
CONTAINER
/data/models
```

Questo permette ai container di training e API
di condividere lo stesso artifact ML persistente.

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

```bash
-v $(pwd)/data/models:/data/models:ro
```

Questo permette all'API di leggere il modello
senza poterlo modificare.

Vantaggi:

- maggiore sicurezza
- migliore isolamento
- protezione degli artifact ML

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

## Perché l'API monta il volume in modalità `:ro`?

L'API deve soltanto leggere il file `model.joblib`
per eseguire inferenza.

Il mount read-only impedisce modifiche accidentali
agli artifact ML.

---

## Cosa succede con `docker compose down -v`?

```bash
docker compose down
```

rimuove i container
ma mantiene i volumi Docker.

```bash
docker compose down -v
```

rimuove anche i volumi associati.

Nel progetto attuale viene utilizzato un bind mount,
quindi il modello rimane salvato
sul filesystem locale del PC.

---

## Come fanno due container a parlarsi per nome?

Docker Compose crea automaticamente
una rete bridge interna.

Ogni servizio diventa automaticamente
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

come hostname.

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

# Risultato ottenuto

Il progetto implementa un workflow ML containerizzato
capace di:

- eseguire training in container
- mantenere artifact persistenti
- esporre endpoint FastAPI
- orchestrare servizi tramite Compose
- separare training e serving

Questa rappresenta una base concreta
per deployment, CI/CD e MLOps basics.