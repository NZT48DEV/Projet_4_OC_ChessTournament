# Chess Tournament Manager

Un outil en ligne de commande pour créer et gérer facilement des tournois d’échecs, enregistrer les joueurs, dérouler les rondes, saisir les résultats et générer des rapports.

---

## 🗂️ Structure du projet

```
ChessTournament/
├── __init__.py
├── config.py                 # Configuration globale (fichiers, constantes)
├── main.py                   # Point d’entrée de l’application
├── requirements.txt                   
├── README.md
├── setup.cfg                
├── controllers/              # Logique métier (CRUD, appariements, gestion de tournois)
│   ├── __init__.py
│   ├── player_controller.py
│   ├── tournament_controller.py
│   ├── round_controller.py
│   └── match_controller.py
├── models/                   # Définition des objets métier
│   ├── __init__.py
│   ├── player_model.py
│   ├── tournament_model.py
│   ├── round_model.py
│   └── match_model.py
├── storage/                  # Lecture/écriture des données persistées
│   ├── __init__.py
│   ├── player_data.py
│   └── tournament_data.py
├── utils/                    # Helpers et messages (I/O, validation, formattage, rangs…)
│   ├── __init__.py
│   ├── console.py
│   ├── date_helpers.py
│   ├── input_manager.py
│   ├── input_formatters.py
│   ├── input_validators.py
│   ├── update_ranks.py
│   ├── error_messages.py
│   └── info_messages.py
├── views/                    # Affichage et menus CLI
│   ├── __init__.py
│   ├── main_menu.py
│   ├── player_view.py
│   ├── tournament_view.py
│   ├── round_view.py
│   ├── match_view.py
│   └── reports_view.py
├── flake8_rapport/ 
│   ├── back.svg
│   ├── file.svg
│   ├── index.html
│   └── style.css  
└── data/                     # Dossiers de stockage JSON/CSV
    ├── players/              # Fichiers individuels de joueurs
    └── tournaments/          # Fichiers individuels de tournois
                       
```

---

## 🚀 Installation

1. **Clonez le dépôt**

   ```bash
   git clone https://github.com/NZT48DEV/Projet_4_OC_ChessTournament.git
   cd ChessTournament
   ```

2. **Créez un environnement virtuel**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .venv\Scripts\activate       # Windows
   ```

3. **Installez les dépendances**
   Si vous ajoutez des bibliothèques externes, listez-les dans `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

* **`config.py`** contient les chemins vers vos dossiers de données, le format de date, etc.
* Vous pouvez personnaliser le nombre de rondes par défaut, le nombre de points assignés par victoire/défaite/nul, etc.

---

## 🔧 Formatage et Nettoyage de Code

Pour garantir la conformité aux directives PEP 8 et un code propre :

1. **Installez flake8 et flake8-html :**

```bash
pip install flake8 flake8-html
```

2. **Vérifiez votre code avec flake8 (longueur max : 119) :**

```bash
flake8 --max-line-length=119 .
```

3. **Générez un rapport HTML dans un dossier flake8_rapport/ :**

```bash
flake8 --max-line-length=119 --format=html --htmldir=flake8_rapport .
```

Le rapport flake8_rapport/index.html doit s’ouvrir sans aucune erreur pour valider la conformité PEP 8.

---

## ▶️ Utilisation

Lancez l’application depuis le terminal :

```bash
python main.py
```

Vous verrez le **menu principal** :

1. 🧑 Créer un joueur
2. 🏆 Créer un tournoi
3. 📂 Charger un tournoi
4. 📊 Afficher des rapports
0. ❌ Quitter

---

**Les flux** :

1. 🧑 **Créer** quelques joueurs via le menu (nom, prénom, date de naissance, classement).
2. 🏆 **Créer un tournoi** 
    - saisissez nom, lieu, date de début, date de fin et nombre de rounds
    - sélectionnez/ajoutez les joueurs 
    - démarrez ou non le tournoi.
3. 📂 **Charger un tournoi** reprenez un tournoi existant (en cours ou non) pour poursuivre sa gestion.
4. 📊 **Afficher les rapports** .

    **[1]** Liste des joueurs (ordre alphabétique)

    **[2]** Liste des tournois enregistrés

    **[3]** Infos d’un tournoi (nom, dates)

    **[4]** Liste des joueurs d’un tournoi (ordre alphabétique)

    **[5]** Liste des rounds et matches d’un tournoi

    **[0]** Retour au menu principal

0. ❌ **Quitter**, fermeture du programme.

---

## 🔑 Fonctionnalités principales

Le programme gère :

- **Appariements selon la méthode suisse** : tri des joueurs par score, mélange aléatoire des ex-æquo, appariements sans rematch, et recours aux rematch en dernier recours.

- **Gestion des joueurs impairs (bye)** : détection automatique d’un nombre impair de joueurs, attribution d’un tour de repos (« bye ») au joueur admissible (score le plus faible n’ayant pas déjà bénéficié d’un bye), mise à jour du classement dense et snapshot du match de repos.

- **Suivi des horaires des rondes** : enregistrement automatique de l’heure de début et de fin de chaque round.

- **Rapport de ronde formaté** : génération d’un rapport console clair, avec les byes listés en premier, présentation alignée des noms, identifiants, couleurs et scores.

- **Sérialisation JSON** : conversion des rounds et matchs en dictionnaires prêts à être persistés avec dates et scores formatés.

- **Enregistrement et persistance en temps réel** : Les données associées au tournoi (match_score/tournament_score/rank/etc.) sont mis à jour et sauvegardés après chaque action utilisateur, et peuvent être rechargés à tout moment via l’option Charger un tournoi.

---

## 📦 Détails techniques

* **Controllers** : orchestrent la création et la mise à jour des modèles.
* **Models** : classes `Player`, `Tournament`, `Round`, `Match` et méthodes de sérialisation JSON.
* **Storage** : lecture/écriture dans `data/players/*.json` et `data/tournaments/*.json`.
* **Views** : menus et affichages en mode console (utilisation de `console.py`).
* **Utils** : gestion des dates, validation d’entrée, formatage, calcul et mise à jour des classements (`update_ranks.py`).

---

## 🤝 Contribuer

1. Forkez ce dépôt
2. Créez une branche feature/xxx
3. Codez votre fonctionnalité ou correctif
4. Ouvrez une Pull Request
5. Attendez la revue et fusion
