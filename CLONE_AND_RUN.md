# 🚀 Cloner et Exécuter en 3 Étapes

## Méthode Ultra-Rapide

### Linux/Mac (1 minute)

```bash
# 1. Cloner
git clone <URL_DU_REPO>
cd IntelligentTutorMultiAgent

# 2. Installer Ollama (LLM local gratuit)
curl https://ollama.ai/install.sh | sh
ollama pull mistral

# 3. Lancer !
./start.sh
```

Puis ouvrez `frontend/index.html` dans votre navigateur 🎉

---

### Windows (1 minute)

```bash
# 1. Cloner
git clone <URL_DU_REPO>
cd IntelligentTutorMultiAgent

# 2. Installer Ollama
# Télécharger depuis: https://ollama.ai/download
# Puis dans PowerShell:
ollama pull mistral

# 3. Lancer !
start.bat
```

Puis ouvrez `frontend/index.html` dans votre navigateur 🎉

---

## Méthode Docker (Production)

```bash
# 1. Cloner
git clone <URL_DU_REPO>
cd IntelligentTutorMultiAgent

# 2. Lancer tout avec Docker
docker-compose up -d

# 3. Télécharger le modèle
docker exec -it moroccan-cs-ollama ollama pull mistral

# Accéder à l'interface
# Frontend: http://localhost:8080
# API: http://localhost:8000
```

---

## Vérification Rapide

### Test 1: API
```bash
curl http://localhost:8000/
```

Devrait retourner:
```json
{
  "status": "running",
  "system": "Moroccan CS Education Multi-Agent",
  "version": "1.0.0"
}
```

### Test 2: Interface Web
1. Ouvrez `frontend/index.html`
2. Sélectionnez la langue (FR/AR/EN)
3. Tapez: "Explique-moi les variables en Python"
4. Attendez la réponse 🎓

---

## Résolution Rapide

### "Ollama not found"
```bash
# Installer Ollama
curl https://ollama.ai/install.sh | sh  # Linux/Mac
# ou télécharger: https://ollama.ai/download  # Windows

# Télécharger un modèle
ollama pull mistral
```

### "Port 8000 already in use"
```bash
# Trouver et tuer le processus
lsof -i :8000  # Linux/Mac
# puis
kill -9 <PID>
```

### "Module not found"
```bash
# Réinstaller les dépendances
pip install -r backend/requirements.txt
```

---

## Ce Qui Est Inclus

✅ **Backend Multi-Agent**
- Coordinateur central intelligent
- 5 agents spécialisés (Tuteur, Évaluateur, Générateur, RAG, Audio)
- Support LLM local (Ollama) et cloud (OpenAI/Claude)

✅ **Frontend**
- Interface web moderne
- Chat en temps réel
- Support FR/AR/EN
- Design responsive

✅ **Contenu Éducatif**
- Cours Python en français et arabe
- 6 exercices progressifs
- Solutions et indices

✅ **Outils de Déploiement**
- Scripts de démarrage automatique
- Docker Compose
- Guide d'installation complet

---

## Fichiers Importants

- **README.md**: Documentation complète
- **INSTALL.md**: Installation détaillée
- **QUICKSTART.md**: Guide de démarrage rapide
- **start.sh / start.bat**: Scripts de lancement
- **docker-compose.yml**: Stack Docker
- **.env.example**: Configuration

---

## Support et Documentation

📚 **Documentation Complète**
- [README.md](README.md) - Vue d'ensemble
- [INSTALL.md](INSTALL.md) - Installation détaillée
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture technique

🌐 **API Documentation**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

💡 **Exemples de Questions**
- "Explique-moi les boucles en Python"
- "Donne-moi des exercices sur les variables"
- "Corrige mon code: [votre code]"
- "Qu'est-ce qu'une fonction?"

🗣️ **Langues Supportées**
- 🇫🇷 Français
- 🇲🇦 العربية (Arabe)
- 🇬🇧 English

---

## Caractéristiques Uniques

🎯 **Adapté au Maroc**
- Curriculum officiel marocain
- Exemples culturellement pertinents
- Niveaux: Tronc Commun, 1ère Bac, 2ème Bac

🤖 **Multi-Agent Intelligent**
- Coordinateur central qui orchestre
- Agents spécialisés pour chaque tâche
- Routage intelligent des requêtes

🧠 **LLM Flexible**
- Local (Ollama) - Gratuit, offline, privé
- Cloud (OpenAI/Claude) - Qualité supérieure

📚 **RAG Intégré**
- Base de connaissances éducative
- Recherche sémantique
- Contexte enrichi

🎤 **Audio (Prêt)**
- Speech-to-Text (Whisper)
- Text-to-Speech (gTTS)
- Support français et arabe

---

## Prochaines Étapes Après Installation

1. **Essayer l'interface web** - Posez vos premières questions
2. **Explorer l'API** - http://localhost:8000/docs
3. **Tester les langues** - Essayez FR, AR, EN
4. **Générer des exercices** - Demandez des exercices
5. **Évaluer du code** - Soumettez des solutions

---

## Questions Fréquentes

**Q: Faut-il une clé API?**
R: Non! Avec Ollama (local), c'est 100% gratuit et privé.

**Q: Ça fonctionne hors ligne?**
R: Oui, avec Ollama téléchargé localement.

**Q: C'est en quelle langue?**
R: Français, Arabe et Anglais supportés.

**Q: C'est pour quel niveau?**
R: Tronc Commun, 1ère Bac, 2ème Bac (système marocain).

**Q: Les données sont privées?**
R: Avec LLM local, tout reste sur votre machine.

---

## Performance

**Temps de réponse typiques (avec Ollama):**
- Question simple: 2-5 secondes
- Génération d'exercices: 5-10 secondes
- Évaluation de code: 3-7 secondes

**Avec OpenAI/Claude (cloud):**
- Question simple: 1-3 secondes
- Génération d'exercices: 3-5 secondes
- Évaluation de code: 2-4 secondes

---

## Vous Êtes Prêt! 🚀

Le système est maintenant **prêt pour le clonage et l'utilisation locale**.

Pour toute question:
- GitHub Issues
- Documentation dans `/docs`
- Email: support@example.com

**Bon apprentissage! 🎓**
