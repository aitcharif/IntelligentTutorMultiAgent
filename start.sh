#!/bin/bash

# Script de démarrage automatique pour le système multi-agent

echo "╔═══════════════════════════════════════════════════╗"
echo "║   Plateforme Multi-Agent - Éducation Marocaine   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Python
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python trouvé: $(python3 --version)${NC}"
echo ""

# Vérifier si Ollama est installé
echo "🔍 Vérification d'Ollama (LLM local)..."
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ollama n'est pas installé${NC}"
    echo ""
    echo "Pour installer Ollama (LLM local gratuit):"
    echo "  curl https://ollama.ai/install.sh | sh"
    echo ""
    echo "Puis télécharger un modèle:"
    echo "  ollama pull mistral"
    echo ""
    read -p "Voulez-vous continuer sans Ollama? (vous devrez utiliser une API cloud) [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ Ollama installé${NC}"

    # Vérifier si Ollama tourne
    if ! pgrep -x "ollama" > /dev/null; then
        echo "🚀 Démarrage d'Ollama..."
        ollama serve &> /dev/null &
        sleep 3
    fi

    # Vérifier les modèles disponibles
    echo "📚 Modèles disponibles:"
    ollama list
fi
echo ""

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Environnement virtuel créé${NC}"
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -q -r backend/requirements.txt
echo -e "${GREEN}✓ Dépendances installées${NC}"
echo ""

# Vérifier la configuration
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Fichier .env non trouvé${NC}"
    echo "📝 Création du fichier .env depuis l'exemple..."
    cp config/.env.example .env
    echo -e "${GREEN}✓ Fichier .env créé${NC}"
    echo ""
    echo -e "${YELLOW}Note: Éditez .env si vous voulez utiliser un LLM cloud (OpenAI/Claude)${NC}"
fi
echo ""

# Créer le dossier de logs
mkdir -p logs

# Démarrer le backend
echo "🚀 Démarrage du serveur backend..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd backend
python3 -m api.main

# Note: Le script s'arrête ici car le serveur tourne en avant-plan
# Pour arrêter: Ctrl+C
