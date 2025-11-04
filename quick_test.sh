#!/bin/bash

# Script de test rapide pour Linux/Mac
# Usage: ./quick_test.sh

echo "======================================"
echo "Test Rapide - IntelligentTutorMultiAgent"
echo "======================================"
echo ""

# Vérifier Python
echo "1. Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python n'est pas installé!"
    exit 1
fi

echo "   Python trouvé: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Vérifier pip
echo "2. Vérification de pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
else
    echo "❌ pip n'est pas installé!"
    exit 1
fi
echo "   pip trouvé: $PIP_CMD"
echo ""

# Option: créer environnement virtuel
read -p "Créer un environnement virtuel? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "3. Création de l'environnement virtuel..."
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    echo "   ✓ Environnement virtuel activé"
else
    echo "3. Utilisation de l'environnement Python global"
fi
echo ""

# Installer les dépendances
read -p "Installer les dépendances? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "4. Installation des dépendances..."
    $PIP_CMD install -r requirements.txt
    echo "   ✓ Dépendances installées"
else
    echo "4. Installation des dépendances ignorée"
fi
echo ""

# Vérifier la clé API
echo "5. Vérification de la clé API..."
if [ -f ".env" ]; then
    echo "   ✓ Fichier .env trouvé"
else
    echo "   ⚠ Fichier .env non trouvé"
    read -p "Créer .env depuis l'exemple? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        cp config/.env.example .env
        echo "   ✓ .env créé - N'oubliez pas d'ajouter votre clé API!"
        echo "   Éditez .env et ajoutez: OPENAI_API_KEY=sk-xxxxx"
    fi
fi
echo ""

# Test d'installation
echo "6. Test d'installation..."
$PYTHON_CMD test_installation.py
echo ""

# Test simple
echo "7. Test simple (sans LLM)..."
$PYTHON_CMD examples/simple_test.py
echo ""

# Proposer le test complet
if [ -f ".env" ]; then
    read -p "Exécuter le test avec LLM? (nécessite clé API) (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]]; then
        echo "8. Test complet avec LLM..."
        $PYTHON_CMD examples/basic_usage.py
    fi
fi

echo ""
echo "======================================"
echo "✅ Tests terminés!"
echo "======================================"
echo ""
echo "Prochaines étapes:"
echo "  - Voir docs/TESTING_LOCAL.md pour plus d'informations"
echo "  - Lancer l'API: python examples/rest_api.py"
echo "  - Consulter README.md pour l'utilisation"
