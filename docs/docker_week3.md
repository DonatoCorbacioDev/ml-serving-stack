# Docker Week 3 — Security, Healthchecks e Production Practices

## Obiettivo

Migliorare il workflow ML containerizzato
introducendo pratiche più vicine
a un ambiente production-oriented.

Il focus della settimana è stato:

* sicurezza dei container
* osservabilità
* runtime behavior
* ottimizzazione del serving
* vulnerability scanning

---

# Architettura Week 3

```text
training container
↓
persistent model artifact
↓
FastAPI serving container
↓
Docker HEALTHCHECK
↓
runtime monitoring
```

---

# Concetti principali studiati

* Non-root containers
* Docker HEALTHCHECK
* `.dockerignore`
* Vulnerability scanning
* Runtime monitoring
* Production-oriented serving
* Startup model loading

---

# Model loading a startup

Nella versione iniziale del progetto
il modello ML veniva caricato
ad ogni richiesta HTTP.

Approccio iniziale:

```python
model = joblib.load(MODEL_PATH)
```

all'interno dell'endpoint `/predict`.

Questo comportamento:

* aumenta l'I/O su disco
* rallenta le richieste
* non è ottimale per produzione

Il caricamento del modello
è stato spostato nello startup dell'API.

Nuovo approccio:

```python
@app.on_event("startup")
def load_model():
```

In questo modo:

* il modello viene caricato una sola volta
* l'API mantiene il modello in memoria
* le richieste successive sono più efficienti

---

# Non-root user

Di default molti container Docker
eseguono il processo come utente `root`.

Nel progetto è stato creato
un utente dedicato:

```dockerfile
RUN useradd --create-home appuser
```

e il container API viene eseguito con:

```dockerfile
USER appuser
```

Questo approccio riduce i privilegi
del processo FastAPI
e segue il principio:

```text
least privilege
```

ovvero concedere soltanto
i permessi strettamente necessari.

---

# Docker HEALTHCHECK

L'API FastAPI espone:

```text
/health
```

È stato configurato un healthcheck Docker:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

Docker controlla periodicamente
lo stato reale dell'applicazione.

Questo permette di distinguere:

```text
container running
```

da:

```text
container healthy
```

---

# Stato unhealthy

Se l'healthcheck fallisce
3 volte consecutive:

```text
--retries=3
```

Docker marca il container come:

```text
unhealthy
```

Il processo principale può continuare
a essere attivo,
ma il servizio non viene più considerato sano.

In ambienti reali questo può attivare:

* restart automatici
* monitoring alert
* failover
* rimozione dal load balancer

---

# .dockerignore

Sono stati introdotti file:

```text
api/.dockerignore
training/.dockerignore
```

per evitare di inviare file inutili
nel build context Docker.

Esempi:

```text
__pycache__/
.venv/
.vscode/
*.log
```

Vantaggi:

* build più leggere
* build più veloci
* cache più stabile
* minore rischio di includere file sensibili

---

# Build context

Docker invia al daemon
il contenuto della cartella definita come:

```yaml
context:
```

Nel progetto:

```yaml
context: ./api
context: ./training
```

Per questo motivo
ogni servizio utilizza
il proprio `.dockerignore`.

---

# Vulnerability scanning con Docker Scout

È stato utilizzato Docker Scout
per analizzare vulnerabilità
nell'immagine API.

Comando utilizzato:

```bash
docker scout cves ml-api
```

Docker Scout controlla:

* base image
* pacchetti di sistema
* dipendenze Python
* CVE note

Risultato ottenuto:

```text
0 critical vulnerabilities
0 high vulnerabilities
```

Sono presenti alcune vulnerabilità
medium e low
legate principalmente
a pacchetti della base image Debian.

Questo dimostra l'importanza
del vulnerability scanning
nei workflow containerizzati.

---

# Multi-stage build

Nel progetto attuale
non è stato ancora implementato
un multi-stage build completo.

Tuttavia il concetto studiato consiste nel separare:

* fase di build/installazione
* fase runtime finale

In progetti più complessi
(frontend React, Java build, PyTorch GPU)
il multi-stage permette di:

* ridurre dimensione immagini
* eliminare strumenti di build
* migliorare sicurezza runtime

---

# Comandi utilizzati

Build API:

```bash
docker compose build api
```

Avvio API:

```bash
docker compose up -d api
```

Verifica utente container:

```bash
docker run --rm ml-api whoami
```

Verifica healthcheck:

```bash
docker ps
```

Vulnerability scan:

```bash
docker scout cves ml-api
```

---

# Domande finali Week 3

## Quanti MB risparmia il multi-stage rispetto a un Dockerfile single-stage?

Nel progetto attuale
non è stato ancora implementato
un multi-stage build completo.

La riduzione della dimensione dell'immagine
è stata ottenuta principalmente tramite:

* `python:3.12-slim`
* `.dockerignore`
* `--no-cache-dir`
* separazione dei servizi Docker

---

## Perché girare come root dentro un container è un problema?

Anche se il container è isolato,
un processo root possiede privilegi elevati.

In caso di vulnerabilità dell'applicazione,
questo può aumentare il rischio di sicurezza.

Per questo motivo
l'API viene eseguita come:

```text
appuser
```

seguendo il principio:

```text
least privilege
```

---

## Cosa succede se l'healthcheck fallisce 3 volte di fila?

Docker marca il container come:

```text
unhealthy
```

Il processo può rimanere attivo,
ma il servizio non viene più considerato sano.

In ambienti reali questo può attivare:

* restart automatici
* failover
* alert monitoring
* rimozione dal traffico

---

# Risultato ottenuto

Il progetto implementa ora
un workflow ML containerizzato
più vicino a scenari reali di produzione.

Sono stati introdotti:

* runtime monitoring
* security best practices
* vulnerability scanning
* startup model loading
* health monitoring
* non-root execution

Questa rappresenta una base concreta
per deployment, CI/CD e MLOps foundations.
