# 📚 Base de Données Éducative

Ce dossier contient les ressources pédagogiques pour le système RAG.

## Structure

```
data/
├── courses/              # Cours et leçons
│   ├── python_basics_fr.md
│   ├── python_basics_ar.md
│   ├── algorithms_fr.md
│   └── ...
├── exercises/            # Exercices et problèmes
│   ├── python_variables.json
│   ├── loops_exercises.json
│   └── ...
├── knowledge_base/       # Base de connaissances générale
│   ├── glossary_fr.md
│   ├── glossary_ar.md
│   └── ...
└── chroma_db/           # Base de données vectorielle (générée)
```

## Cours Disponibles

### Tronc Commun
- ✅ Introduction à Python (FR/AR)
- ✅ Variables et types de données
- 🔄 Structures conditionnelles (à venir)
- 🔄 Boucles (à venir)

### 1ère Année Bac
- 🔄 Programmation orientée objet
- 🔄 Structures de données
- 🔄 Algorithmes de recherche

### 2ème Année Bac
- 🔄 Algorithmes avancés
- 🔄 Bases de données
- 🔄 Développement web

## Format des Cours

Les cours sont en Markdown avec des blocs de code:

```markdown
# Titre du Cours

## Section

Explication...

### Exemple:
\`\`\`python
# Code exemple
x = 5
\`\`\`

### Exercice:
Description de l'exercice...
```

## Format des Exercices

Les exercices sont en JSON:

```json
{
  "title": "Titre de l'exercice",
  "level": "tronc_commun|premiere_bac|deuxieme_bac",
  "language": "fr|ar",
  "exercises": [
    {
      "id": "ex1",
      "title": "...",
      "difficulty": "facile|moyen|difficile",
      "description": "...",
      "solution": "...",
      "hints": ["...", "..."]
    }
  ]
}
```

## Ajouter du Contenu

### Nouveau Cours

1. Créer `courses/votre_cours_fr.md`
2. Optionnel: Version arabe `votre_cours_ar.md`
3. Suivre la structure Markdown standard

### Nouveaux Exercices

1. Créer `exercises/votre_exercice.json`
2. Suivre le format JSON ci-dessus
3. Ajouter des hints progressifs

### Base de Connaissances

1. Ajouter des fichiers dans `knowledge_base/`
2. Utiliser Markdown pour le formatage
3. Inclure des métadonnées (niveau, sujet, langue)

## Langues Supportées

- 🇫🇷 Français (fr)
- 🇲🇦 العربية (ar)
- 🇬🇧 English (en)

## Contribution

Pour contribuer du contenu:

1. Respecter le format existant
2. Inclure des exemples concrets
3. Adapter au contexte marocain
4. Fournir des versions multilingues si possible
5. Tester les exercices

## Qualité du Contenu

✅ Explications claires et progressives
✅ Exemples pertinents au Maroc
✅ Exercices de difficulté croissante
✅ Solutions détaillées
✅ Hints pédagogiques

## Indexation RAG

Les contenus sont automatiquement indexés par le système RAG pour:
- Recherche sémantique
- Récupération de contexte
- Réponses personnalisées

Pour réindexer:
```bash
python -m backend.rag.index_documents
```

## Statistiques Actuelles

- **Cours**: 2 (Python basics FR/AR)
- **Exercices**: 6 (Variables Python)
- **Langues**: Français, Arabe
- **Niveaux**: Tronc Commun

## Roadmap du Contenu

### Phase 1 (Actuelle)
- ✅ Python basics
- ✅ Variables et types

### Phase 2
- [ ] Conditions et boucles
- [ ] Fonctions
- [ ] Listes et dictionnaires

### Phase 3
- [ ] POO (Classes et objets)
- [ ] Fichiers et exceptions
- [ ] Modules et packages

### Phase 4
- [ ] Algorithmes de tri
- [ ] Structures de données avancées
- [ ] Projets pratiques

## Contact

Pour suggérer du contenu ou signaler des erreurs:
- Ouvrir une issue GitHub
- Contact: education@example.com
