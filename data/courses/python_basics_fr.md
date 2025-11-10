# Introduction à Python - Niveau Tronc Commun

## Les Variables en Python

### Qu'est-ce qu'une variable?

Une variable est un conteneur qui permet de stocker des données en mémoire. En Python, vous n'avez pas besoin de déclarer le type de la variable.

### Exemples:

```python
# Variables numériques
age = 16
note = 15.5

# Variables textuelles
nom = "Ahmed"
ville = "Casablanca"

# Variables booléennes
est_etudiant = True
```

### Règles de nommage:
- Commencer par une lettre ou underscore (_)
- Pas d'espaces (utiliser _)
- Pas de mots réservés Python (if, for, etc.)

### Exemple marocain:
```python
ville_natale = "Rabat"
nombre_de_freres = 3
parle_arabe = True
```

## Les Opérations Mathématiques

Python peut être utilisé comme une calculatrice:

```python
# Addition
somme = 10 + 5  # 15

# Soustraction
difference = 20 - 8  # 12

# Multiplication
produit = 6 * 7  # 42

# Division
quotient = 20 / 4  # 5.0

# Division entière
division_entiere = 20 // 3  # 6

# Modulo (reste)
reste = 20 % 3  # 2

# Puissance
puissance = 2 ** 3  # 8
```

## Les Types de Données

### Types de base:
- **int**: Nombres entiers (ex: 42, -10)
- **float**: Nombres décimaux (ex: 3.14, -2.5)
- **str**: Chaînes de caractères (ex: "Bonjour", "المغرب")
- **bool**: Booléens (True ou False)

### Vérifier le type:
```python
age = 16
print(type(age))  # <class 'int'>

note = 15.5
print(type(note))  # <class 'float'>

nom = "Ahmed"
print(type(nom))  # <class 'str'>
```

## Les Chaînes de Caractères

### Création:
```python
message = "Bonjour le Maroc!"
prenom = 'Fatima'
phrase = """Ceci est une
chaîne sur plusieurs lignes"""
```

### Opérations sur les chaînes:
```python
# Concaténation
salutation = "Bonjour " + "Ahmed"  # "Bonjour Ahmed"

# Répétition
repeat = "Ha" * 3  # "HaHaHa"

# Longueur
longueur = len("Casablanca")  # 10

# Majuscules/Minuscules
ville = "rabat"
print(ville.upper())  # "RABAT"
print(ville.capitalize())  # "Rabat"
```

## Exercices Pratiques

### Exercice 1: Calculer l'âge
```python
# Un élève est né en 2008
# Calculez son âge en 2024

annee_naissance = 2008
annee_actuelle = 2024
age = annee_actuelle - annee_naissance
print(f"L'élève a {age} ans")
```

### Exercice 2: Carte d'identité
```python
# Créez des variables pour votre profil
nom = "Amrani"
prenom = "Youssef"
age = 16
ville = "Marrakech"

# Affichez votre carte d'identité
print("=== Carte d'Identité ===")
print(f"Nom: {nom}")
print(f"Prénom: {prenom}")
print(f"Âge: {age} ans")
print(f"Ville: {ville}")
```

### Exercice 3: Calcul de moyenne
```python
# Calculez la moyenne de trois notes
note1 = 15
note2 = 17
note3 = 14

moyenne = (note1 + note2 + note3) / 3
print(f"Moyenne: {moyenne:.2f}")
```

## Points Clés à Retenir

✅ Les variables stockent des données
✅ Python détermine automatiquement le type
✅ Utilisez des noms de variables descriptifs
✅ Les chaînes peuvent être entre " " ou ' '
✅ Les opérations mathématiques sont intuitives

## Prochaine Leçon

Dans la prochaine leçon, nous allons apprendre:
- Les structures conditionnelles (if/else)
- Les boucles (for/while)
- Les listes et dictionnaires
