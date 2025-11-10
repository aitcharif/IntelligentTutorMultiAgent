# Guide de Déploiement Docker

Ce guide vous permet de déployer le système multi-agent avec Docker sur votre propre machine.

## Prérequis

### Installation de Docker

#### Sur Ubuntu/Debian:
```bash
# Mettre à jour les packages
sudo apt-get update

# Installer Docker
sudo apt-get install -y docker.io docker-compose

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter votre utilisateur au groupe docker (évite sudo)
sudo usermod -aG docker $USER

# Appliquer les changements (ou redémarrer)
newgrp docker
```

#### Sur macOS:
1. Télécharger Docker Desktop: https://www.docker.com/products/docker-desktop
2. Installer et démarrer Docker Desktop
3. Vérifier l'installation: `docker --version`

#### Sur Windows:
1. Télécharger Docker Desktop: https://www.docker.com/products/docker-desktop
2. Installer et démarrer Docker Desktop
3. Ouvrir PowerShell ou WSL2
4. Vérifier l'installation: `docker --version`

## Déploiement avec Docker Compose

### 1. Vérifier l'installation Docker

```bash
docker --version
docker compose version
```

### 2. Lancer le système complet

```bash
# Se placer dans le répertoire du projet
cd IntelligentTutorMultiAgent

# Lancer tous les services en arrière-plan
docker compose up -d
```

Cette commande va démarrer:
- **Backend**: API FastAPI sur le port 8000
- **Ollama**: Serveur LLM local sur le port 11434
- **Frontend**: Interface web sur le port 80

### 3. Télécharger le modèle Mistral dans Ollama

```bash
# Attendre que le service Ollama démarre (environ 10-15 secondes)
sleep 15

# Télécharger le modèle Mistral (4.4 GB - peut prendre plusieurs minutes)
docker exec -it moroccan-cs-ollama ollama pull mistral

# Vérifier que le modèle est bien téléchargé
docker exec -it moroccan-cs-ollama ollama list
```

### 4. Vérifier que tout fonctionne

```bash
# Vérifier les conteneurs en cours d'exécution
docker compose ps

# Vérifier les logs du backend
docker compose logs backend

# Vérifier les logs d'Ollama
docker compose logs ollama

# Tester l'API
curl http://localhost:8000/api/status
```

### 5. Accéder au système

- **Interface Web**: http://localhost (port 80)
- **API Backend**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434

## Commandes Utiles

### Voir les logs en temps réel

```bash
# Tous les services
docker compose logs -f

# Backend seulement
docker compose logs -f backend

# Ollama seulement
docker compose logs -f ollama
```

### Redémarrer les services

```bash
# Redémarrer tous les services
docker compose restart

# Redémarrer le backend seulement
docker compose restart backend
```

### Arrêter le système

```bash
# Arrêter tous les services
docker compose down

# Arrêter et supprimer les volumes (⚠️ efface les données)
docker compose down -v
```

### Reconstruire les images

```bash
# Reconstruire et redémarrer
docker compose up -d --build

# Reconstruire sans cache
docker compose build --no-cache
```

## Architecture Docker

### Services déployés

1. **backend**
   - Image: Construite depuis le Dockerfile local
   - Port: 8000
   - Dépend de: ollama
   - Variables d'environnement configurées dans `.env`

2. **ollama**
   - Image: ollama/ollama:latest
   - Port: 11434
   - Volume persistant pour les modèles

3. **frontend** (optionnel)
   - Image: nginx:alpine
   - Port: 80
   - Sert les fichiers statiques HTML/CSS/JS

### Volumes Docker

```bash
# Lister les volumes
docker volume ls

# Inspecter le volume Ollama (modèles téléchargés)
docker volume inspect intelligenttutor_ollama_data
```

## Tester le Modèle Ollama Directement

```bash
# Tester Ollama en mode interactif
docker exec -it moroccan-cs-ollama ollama run mistral

# Poser une question
# > Explique moi les variables en Python

# Quitter: /bye
```

## Configuration Avancée

### Modifier les variables d'environnement

Éditez le fichier `.env`:
```bash
nano .env
```

Puis redémarrez:
```bash
docker compose down
docker compose up -d
```

### Utiliser un autre modèle LLM

```bash
# Télécharger un autre modèle (ex: llama2)
docker exec -it moroccan-cs-ollama ollama pull llama2

# Modifier .env
# OLLAMA_MODEL=llama2

# Redémarrer
docker compose restart backend
```

### Activer le mode GPU (NVIDIA)

Si vous avez une carte NVIDIA, modifiez `docker-compose.yml`:

```yaml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## Résolution de Problèmes

### Le backend ne démarre pas

```bash
# Vérifier les logs
docker compose logs backend

# Vérifier que Ollama est démarré
docker compose ps ollama

# Redémarrer
docker compose restart backend
```

### Ollama ne répond pas

```bash
# Vérifier qu'Ollama fonctionne
docker exec -it moroccan-cs-ollama ollama list

# Redémarrer Ollama
docker compose restart ollama
```

### Port déjà utilisé

Si le port 8000 ou 80 est déjà utilisé, modifiez `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Utiliser le port 8001 au lieu de 8000
```

### Manque d'espace disque

Le modèle Mistral nécessite ~4.4 GB. Vérifiez l'espace disponible:

```bash
df -h
docker system df
```

Nettoyer les anciennes images:
```bash
docker system prune -a
```

## Production

Pour déployer en production:

1. **Utiliser un reverse proxy** (Nginx, Traefik)
2. **Activer HTTPS** avec Let's Encrypt
3. **Configurer les variables d'environnement** de production
4. **Activer l'authentification**
5. **Mettre en place la surveillance** (logs, métriques)
6. **Configurer les sauvegardes** des volumes

### Exemple avec Nginx et SSL

Créer un fichier `nginx.conf`:

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name votre-domaine.com;

    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:80;
    }
}
```

## Support

Pour obtenir de l'aide:
1. Vérifier les logs: `docker compose logs`
2. Vérifier la documentation Docker: https://docs.docker.com/
3. Consulter le README du projet
