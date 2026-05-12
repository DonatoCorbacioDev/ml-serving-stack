# Docker Week 4 — CI/CD, GitHub Actions e Container Registry

## Obiettivo

Collegare Docker a un workflow più vicino
al contesto reale di sviluppo e deployment.

Il focus della settimana è stato:

* automazione della build Docker
* GitHub Actions
* pubblicazione immagine su GitHub Container Registry
* verifica dell'immagine pubblicata
* separazione tra immagine applicativa e artifact ML
* introduzione concettuale a GPU e Kubernetes

---

# Architettura Week 4

```text
codice locale
↓
git push
↓
GitHub Actions
↓
Docker build automatica
↓
GitHub Container Registry
↓
docker pull
↓
run immagine pubblicata
↓
FastAPI ML serving
```

---

# Concetti principali studiati

* CI/CD basics
* GitHub Actions
* Workflow YAML
* GitHub Container Registry (GHCR)
* Docker image publishing
* Docker image pulling
* Container portability
* Artifact mounting
* GPU/CUDA overview
* Kubernetes overview

---

# CI/CD

CI/CD significa automatizzare
alcune fasi del workflow di sviluppo.

Nel progetto `ml-serving-stack`,
la parte implementata riguarda:

```text
Continuous Integration
+
container image publishing
```

Ogni volta che viene fatto un push
sul branch `main`, GitHub Actions
esegue automaticamente la pipeline.

---

# GitHub Actions

GitHub Actions è il sistema CI/CD
integrato in GitHub.

Permette di definire workflow automatici
all'interno della cartella:

```text
.github/workflows/
```

Nel progetto è stato creato il file:

```text
.github/workflows/ci.yml
```

Questo file descrive:

* quando deve partire la pipeline
* su quale sistema operativo deve girare
* quali comandi devono essere eseguiti
* dove deve essere pubblicata l'immagine Docker

---

# File ci.yml

Workflow utilizzato:

```yaml
name: CI Docker API

on:
  push:
    branches:
      - main

jobs:
  build-api:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build Docker image
        run: |
          docker build -t ghcr.io/donatocorbaciodev/ml-api:latest ./api

      - name: Push Docker image
        run: |
          docker push ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Trigger della pipeline

La sezione:

```yaml
on:
  push:
    branches:
      - main
```

significa che il workflow parte automaticamente
quando viene eseguito un push sul branch `main`.

Esempio:

```bash
git push
```

Dopo il push, GitHub Actions
avvia automaticamente il workflow.

---

# Runner GitHub Actions

La sezione:

```yaml
runs-on: ubuntu-latest
```

indica che GitHub crea una macchina Linux temporanea
su cui eseguire la pipeline.

Questa macchina:

* viene creata automaticamente
* clona il repository
* esegue gli step del workflow
* viene eliminata al termine della pipeline

---

# Checkout repository

Lo step:

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

serve a scaricare il codice del repository
all'interno del runner GitHub Actions.

È equivalente, a livello concettuale, a:

```bash
git clone <repository>
```

---

# Login su GitHub Container Registry

Lo step:

```yaml
- name: Log in to GitHub Container Registry
  uses: docker/login-action@v3
```

permette alla pipeline
di autenticarsi su GHCR.

Il token utilizzato è:

```yaml
secrets.GITHUB_TOKEN
```

Questo token viene gestito automaticamente da GitHub
ed è usato per pubblicare immagini Docker
nel registry del repository/account.

---

# Build immagine Docker

Lo step:

```bash
docker build -t ghcr.io/donatocorbaciodev/ml-api:latest ./api
```

costruisce l'immagine Docker dell'API FastAPI
usando come build context:

```text
./api
```

L'immagine viene taggata come:

```text
ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Push immagine Docker

Lo step:

```bash
docker push ghcr.io/donatocorbaciodev/ml-api:latest
```

pubblica l'immagine Docker
su GitHub Container Registry.

In questo modo l'immagine
non esiste più soltanto localmente,
ma può essere scaricata da altre macchine.

---

# GitHub Container Registry

GitHub Container Registry è un registry Docker
integrato in GitHub.

Permette di conservare immagini containerizzate
associate a un account o repository.

Nel progetto è stata pubblicata l'immagine:

```text
ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Debugging della pipeline

Durante la configurazione iniziale
la pipeline è fallita.

Errore osservato:

```text
No event triggers defined in `on`
```

Questo errore indicava un problema
nella definizione del trigger YAML.

Dopo la correzione,
la pipeline è stata rilanciata automaticamente
con un nuovo push.

---

# Errore sul tag Docker

Un secondo errore osservato è stato:

```text
repository name must be lowercase
```

Il problema era legato al nome dell'immagine Docker.

Docker richiede nomi repository in lowercase.

Per risolvere il problema,
è stato usato un tag esplicito:

```text
ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Warning Node.js 20

Durante l'esecuzione della pipeline
GitHub Actions ha mostrato un warning relativo
a Node.js 20.

Questo warning non ha bloccato il workflow.

La pipeline è risultata corretta perché:

* il job `build-api` è diventato verde
* l'immagine è stata buildata correttamente
* l'immagine è stata pubblicata su GHCR

Il warning riguarda la futura migrazione
delle GitHub Actions verso Node.js 24.

---

# Pull dell'immagine pubblicata

Dopo la pubblicazione su GHCR,
l'immagine è stata scaricata localmente con:

```bash
docker pull ghcr.io/donatocorbaciodev/ml-api:latest
```

Questo passaggio verifica che l'immagine
sia realmente disponibile nel registry.

---

# Run dell'immagine pubblicata

L'immagine è stata eseguita localmente con:

```bash
docker run --rm -p 8000:8000 \
  -v "$(pwd)/data/models:/data/models:ro" \
  ghcr.io/donatocorbaciodev/ml-api:latest
```

Questo comando:

* avvia l'immagine pubblicata su GHCR
* espone la porta 8000
* monta il modello ML in read-only
* avvia FastAPI

---

# Errore porta già occupata

Durante il test è comparso l'errore:

```text
Bind for 0.0.0.0:8000 failed: port is already allocated
```

Questo significa che la porta 8000
sul computer host era già occupata
da un altro container o processo.

Soluzioni possibili:

```bash
docker compose down
```

oppure usare un'altra porta:

```bash
docker run --rm -p 8001:8000 ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Errore modello mancante

Eseguendo l'immagine senza volume,
l'API ha restituito:

```text
RuntimeError: Model file not found at /data/models/model.joblib
```

Questo errore è corretto e previsto.

L'immagine API contiene:

* codice FastAPI
* dipendenze Python
* runtime applicativo

ma non contiene:

```text
model.joblib
```

Il modello è un artifact ML esterno
che deve essere montato nel container.

---

# Separazione tra immagine e artifact ML

Un concetto importante della Week 4 è la separazione tra:

```text
Docker image
```

e:

```text
ML artifact
```

L'immagine contiene l'applicazione.

Il modello viene invece gestito
come artifact esterno persistente.

Questa separazione è importante perché permette di:

* aggiornare il codice senza includere il modello nell'immagine
* versionare i modelli separatamente
* montare modelli diversi nello stesso servizio API
* mantenere immagini più leggere
* rendere il serving più flessibile

---

# Test endpoint API

Dopo aver montato correttamente il modello,
l'API è partita con successo.

Endpoint testati:

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Il test ha confermato
che l'immagine pubblicata funziona correttamente
quando il modello viene montato come artifact esterno.

---

# GPU e NVIDIA Container Toolkit

La Week 4 include anche un'introduzione
al concetto di GPU nei container Docker.

Per usare GPU NVIDIA con Docker
serve NVIDIA Container Toolkit.

Comando concettuale:

```bash
docker run --gpus all
```

Nel computer aziendale utilizzato
è presente una GPU integrata Intel UHD,
non una GPU NVIDIA.

Per questo motivo CUDA e NVIDIA Container Toolkit
non sono stati installati.

Nel progetto attuale non servono,
perché il workflow usa:

* scikit-learn
* RandomForest
* FastAPI
* CPU

---

# Uso della GPU in azienda

In contesti aziendali,
quando serve potenza GPU,
solitamente vengono usate soluzioni come:

* server aziendali con GPU NVIDIA
* macchine remote accessibili via SSH
* servizi cloud GPU
* piattaforme ML gestite
* cluster condivisi gestiti da team DevOps/MLOps

Lo sviluppo locale avviene spesso su CPU,
mentre training o inference pesanti
vengono eseguiti su infrastrutture dedicate.

---

# Kubernetes overview

Kubernetes è stato considerato
solo a livello introduttivo.

Docker permette di creare ed eseguire container.

Kubernetes serve a orchestrare container
in ambienti più grandi e complessi.

Kubernetes può gestire:

* restart automatici
* scaling
* deployment
* service discovery
* load balancing
* rolling update

Nel progetto attuale non è stato implementato Kubernetes,
perché prima è più importante consolidare:

* Docker lifecycle
* API serving
* artifact management
* GitHub Actions
* GHCR
* CI/CD basics

---

# Comandi utilizzati

Controllo stato Git:

```bash
git status
```

Commit workflow CI/CD:

```bash
git add .
git commit -m "feat: add GitHub Actions CI workflow"
git push
```

Pull immagine da GHCR:

```bash
docker pull ghcr.io/donatocorbaciodev/ml-api:latest
```

Run immagine pubblicata:

```bash
docker run --rm -p 8000:8000 \
  -v "$(pwd)/data/models:/data/models:ro" \
  ghcr.io/donatocorbaciodev/ml-api:latest
```

Test health endpoint:

```bash
curl http://localhost:8000/health
```

Test predict endpoint:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

# Domande finali Week 4

## A cosa serve GitHub Actions?

GitHub Actions serve ad automatizzare
operazioni di build, test e deployment.

Nel progetto è stato usato per buildare automaticamente
l'immagine Docker dell'API
ogni volta che viene fatto un push su `main`.

---

## A cosa serve GHCR?

GitHub Container Registry serve a pubblicare
e conservare immagini Docker.

Nel progetto permette di scaricare l'immagine API
anche fuori dal computer locale.

---

## Perché l'immagine API non contiene model.joblib?

Perché il modello ML è trattato come artifact esterno.

Questa scelta permette di separare:

* codice applicativo
* runtime API
* modello addestrato

In sistemi reali questa separazione aiuta
a gestire versioni diverse di modelli
e a mantenere immagini più leggere.

---

## Perché non è stata usata la GPU?

Il computer utilizzato non dispone
di GPU NVIDIA compatibile con CUDA.

Inoltre il progetto attuale usa scikit-learn
e un modello RandomForest,
che può essere eseguito tranquillamente su CPU.

La GPU è stata studiata solo come concetto
per capire come viene utilizzata
in workflow ML più pesanti.

---

## Perché Kubernetes non è stato implementato?

Kubernetes è utile in ambienti complessi
con molti container e necessità di scaling.

Nel progetto attuale è più utile
consolidare prima Docker, FastAPI,
artifact management, CI/CD e registry.

Per questo Kubernetes è stato trattato
solo come panoramica introduttiva.

---

# Risultato ottenuto

Il progetto ora include
un workflow CI/CD base per ML serving.

È stato possibile:

* fare push del codice su GitHub
* attivare automaticamente GitHub Actions
* buildare l'immagine Docker dell'API
* pubblicare l'immagine su GHCR
* scaricare l'immagine pubblicata
* eseguire l'immagine localmente
* montare l'artifact ML esterno
* testare gli endpoint FastAPI

Questo completa una base concreta
per comprendere Docker nel contesto ML,
serving API e CI/CD basics.

---

# Conclusione

La Week 4 ha trasformato il progetto
da workflow locale manuale
a workflow automatizzato e distribuibile.

Il passaggio principale è stato:

```text
funziona sul mio PC
↓
può essere buildato automaticamente
↓
può essere pubblicato su un registry
↓
può essere eseguito da immagine remota
```

Questo è un passaggio fondamentale
verso un approccio più vicino
al lavoro reale di ML Engineering.
