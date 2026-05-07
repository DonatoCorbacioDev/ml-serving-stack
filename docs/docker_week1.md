# Docker Week 1 — Fondamenti

## Obiettivo

Capire come creare ed eseguire un container Docker
per un training ML semplice.

Il progetto utilizza un container Python per addestrare
un modello RandomForest sul dataset Iris
e salvare il modello serializzato con joblib.

---

## Concetti principali studiati

- Docker image
- Container runtime
- Dockerfile
- Layer cache
- CMD
- ENTRYPOINT
- Container filesystem
- Runtime arguments
- Training container

---

## Dockerfile utilizzato

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY train.py .

CMD ["python", "train.py"]
```

---

## Perché l'ordine COPY requirements.txt → RUN pip install → COPY . è importante?

Docker utilizza un sistema di layer cache.

Separando `requirements.txt` dal resto del codice,
Docker evita di reinstallare tutte le dipendenze
quando cambia solo `train.py`.

Questo rende le build molto più veloci
e ottimizza il workflow di sviluppo.

---

## Differenza tra CMD e ENTRYPOINT

`CMD` definisce il comando di default del container.

Può essere sovrascritto a runtime.

Esempio:

```bash
docker run --rm ml-training bash
```

oppure:

```bash
docker run --rm ml-training python train.py --help
```

`ENTRYPOINT` invece rende il container più rigido
e viene usato quando il container deve comportarsi
come un eseguibile specifico.

---

## Come entrare dentro un container?

```bash
docker run --rm -it ml-training bash
```

Questo apre una shell interattiva dentro il container.

Comandi utili:

```bash
ls
pwd
python train.py
```

---

## Runtime arguments con argparse

Il training script utilizza `argparse`
per supportare parametri runtime.

Esempio:

```bash
docker run --rm ml-training python train.py --help
```

Output:

```text
usage: train.py [-h] [--output-dir OUTPUT_DIR]
```

Questo permette di configurare il comportamento
del training container senza modificare il codice.

---

## Osservazione importante sul filesystem del container

Il modello viene salvato dentro:

```text
/data/models/model.joblib
```

Attualmente il file viene creato
nel filesystem interno del container.

Quando il container termina,
il filesystem viene distrutto.

Per mantenere i dati persistenti
sarà necessario utilizzare Docker volumes.

---

## Comandi utilizzati

Build immagine:

```bash
docker build -t ml-training ./training
```

Esecuzione container:

```bash
docker run --rm ml-training
```

Help runtime:

```bash
docker run --rm ml-training python train.py --help
```

Shell interattiva:

```bash
docker run --rm -it ml-training bash
```

---

## Risultato ottenuto

È stato creato un training workload containerizzato
capace di:

- installare dipendenze Python
- addestrare un modello ML
- salvare un artifact
- eseguire runtime arguments
- essere eseguito in modo isolato e riproducibile