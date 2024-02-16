### Initialisation du projet

Copiez ce répertoire sur votre machine local :

```bash
git clone https://github.com/SeRiice/flask-api_gomes-peixoto_bruno
```

Exécutez les commandes suivantes :

```bash
cd ./flask-api_gomes-peixoto_bruno/
docker compose up --build
```

Accédez au terminal du conteneur 'web' pour pouvoir y exécuter les commandes suivantes :

```bash
cd app/src/
flask db init
flask db migrate
flask db upgrade
```

Accèdez à l'API via l'url suivante http://localhost:5001/
