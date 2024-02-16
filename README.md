### Initialisation du projet

Copiez ce répertoire sur votre machine local :

```bash
git clone ...
```

Exécutez les commandes suivantes :

```bash
cd ..
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
