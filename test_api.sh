#!/bin/bash

# Script de test de l'API Multi-Agent
# Usage: ./test_api.sh

BASE_URL="http://localhost:8000"

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Test de l'API Multi-Agent${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Test du status
echo -e "\n${YELLOW}1. Test du status du système...${NC}"
STATUS_RESPONSE=$(curl -s $BASE_URL/api/status)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ API accessible${NC}"
    echo "$STATUS_RESPONSE" | jq .
else
    echo -e "${RED}✗ Erreur: Impossible d'accéder à l'API${NC}"
    echo -e "${RED}  Assurez-vous que le serveur est démarré sur $BASE_URL${NC}"
    exit 1
fi

# 2. Créer une session
echo -e "\n${YELLOW}2. Création d'une session d'apprentissage...${NC}"
SESSION_RESPONSE=$(curl -s -X POST $BASE_URL/api/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "ahmed_001",
    "name": "Ahmed",
    "curriculum_level": "tronc_commun",
    "language": "fr"
  }')

if [ $? -eq 0 ]; then
    SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
    echo -e "${GREEN}✓ Session créée${NC}"
    echo -e "${GREEN}  Session ID: $SESSION_ID${NC}"
    echo "$SESSION_RESPONSE" | jq .
else
    echo -e "${RED}✗ Erreur lors de la création de la session${NC}"
    exit 1
fi

# 3. Test question simple
echo -e "\n${YELLOW}3. Test d'une question simple...${NC}"
echo -e "   Question: 'Qu'est-ce qu'une variable en Python?'"
CHAT_RESPONSE=$(curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Qu'est-ce qu'une variable en Python? Explique avec un exemple simple.\",
    \"language\": \"fr\"
  }")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Réponse reçue${NC}"
    RESPONSE_TEXT=$(echo $CHAT_RESPONSE | jq -r '.response')
    AGENT_USED=$(echo $CHAT_RESPONSE | jq -r '.agent_used')
    echo -e "${GREEN}  Agent utilisé: $AGENT_USED${NC}"
    echo -e "\n${BLUE}Réponse:${NC}"
    echo "$RESPONSE_TEXT" | fold -w 80 -s
else
    echo -e "${RED}✗ Erreur lors de l'envoi du message${NC}"
fi

# 4. Test demande exercice
echo -e "\n${YELLOW}4. Test de demande d'exercice...${NC}"
echo -e "   Demande: 'Donne-moi un exercice sur les variables'"
EXERCISE_RESPONSE=$(curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Donne-moi un exercice facile sur les variables Python\",
    \"language\": \"fr\"
  }")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Exercice reçu${NC}"
    EXERCISE_TEXT=$(echo $EXERCISE_RESPONSE | jq -r '.response')
    AGENT_USED=$(echo $EXERCISE_RESPONSE | jq -r '.agent_used')
    echo -e "${GREEN}  Agent utilisé: $AGENT_USED${NC}"
    echo -e "\n${BLUE}Exercice:${NC}"
    echo "$EXERCISE_TEXT" | fold -w 80 -s
else
    echo -e "${RED}✗ Erreur lors de la demande d'exercice${NC}"
fi

# 5. Test soumission de solution
echo -e "\n${YELLOW}5. Test de soumission de solution...${NC}"
SOLUTION_CODE="nom = 'Ahmed'\nage = 17\nprint('Je m\\'appelle', nom, 'et j\\'ai', age, 'ans')"
echo -e "   Solution soumise:"
echo -e "   ${BLUE}$SOLUTION_CODE${NC}"

EVAL_RESPONSE=$(curl -s -X POST $BASE_URL/api/chat \
  -H "Content-Type: application/json" \
  -d "{
    \"session_id\": \"$SESSION_ID\",
    \"message\": \"Voici ma solution:\n\n$SOLUTION_CODE\",
    \"language\": \"fr\"
  }")

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Évaluation reçue${NC}"
    EVAL_TEXT=$(echo $EVAL_RESPONSE | jq -r '.response')
    AGENT_USED=$(echo $EVAL_RESPONSE | jq -r '.agent_used')
    echo -e "${GREEN}  Agent utilisé: $AGENT_USED${NC}"
    echo -e "\n${BLUE}Évaluation:${NC}"
    echo "$EVAL_TEXT" | fold -w 80 -s
else
    echo -e "${RED}✗ Erreur lors de l'évaluation${NC}"
fi

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${GREEN}✓ Tests terminés avec succès!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo -e "\nPour plus d'informations:"
echo -e "  - Documentation API: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  - Guide API REST: ${BLUE}GUIDE_API_REST.md${NC}"
echo -e "  - Guide Docker: ${BLUE}GUIDE_DOCKER.md${NC}"
