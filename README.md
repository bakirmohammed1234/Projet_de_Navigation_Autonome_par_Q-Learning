#  Projet de Navigation Autonome par Q-Learning

Ce projet implémente un agent robotisé capable de naviguer dans un environnement contraint pour accomplir une mission de logistique : récupérer un objet et le livrer à un point précis.

## Présentation du Problème

L'objectif est de piloter un robot sur une grille de **4 lignes par 5 colonnes**. L'agent doit :
1. Partir du point de départ **D** (case (4,1)).
2. Se déplacer vers l'un des points de collecte **O** (cases (1,1) ou (4,4)).
3. Récupérer l'objet et le transporter jusqu'au point de destination **S**.



###  Contraintes de l'Environnement
* **Obstacles fixes** : Certaines cases sont inaccessibles (marquées en noir sur le plan).
* **Murs internes** : Des parois bloquent le passage direct entre certaines colonnes, obligeant l'agent à contourner.

## ⚙️ Modélisation de l'Intelligence Artificielle

### 1. Espace d'États
Le nombre total d'états est de **40**:
* **20 positions** possibles (4x5).
* **2 variables d'état** : Avec objet ou Sans objet.
* *Calcul : 20 positions × 2 états de charge = 40 combinaisons possibles.*

### 2. Système d'Actions
L'agent peut effectuer **6 actions** distinctes:
* Déplacements : `Haut`, `Bas`, `Gauche`, `Droite`.
* Interactions : `Récupérer` (charger l'objet) et `Déposer` (décharger l'objet).

### 3. Politique de Récompenses
Le comportement de l'agent est dicté par les scores suivants :
* **-1** : Pénalité pour chaque mouvement (incite à trouver le chemin le plus court).
* **-10** : Pénalité pour une tentative de récupération ou dépôt hors zone.
* **+20** : Bonus pour une livraison réussie au point S.

## 🧠= Algorithme Utilisé : Q-Learning

Le projet utilise l'algorithme de **Q-Learning** pour remplir une table de décision (Q-Table). La mise à jour de la connaissance se fait via l'équation de Bellman :

<img width="720" height="122" alt="image" src="https://github.com/user-attachments/assets/a4e1211d-dda9-4307-a63a-554480a2739b" />

* **Alpha (0.1)** : Vitesse à laquelle l'agent intègre les nouvelles informations.
* **Gamma (0.9)** : Importance accordée aux récompenses futures.
* **Epsilon (0.2)** : Probabilité de tester des actions aléatoires pour découvrir de nouveaux chemins.

##  Résultats du Test
Une fois l'apprentissage terminé, l'agent trouve le chemin optimal en 11 étapes pour récupérer l'objet en (1,1) et le livrer en (1,5).

<img width="582" height="311" alt="image" src="https://github.com/user-attachments/assets/24d032ad-909a-4fdc-9682-78088167d499" />

> **Note :** Comme illustré ci-dessus, le robot optimise son trajet en évitant les obstacles et en effectuant les actions de chargement/déchargement aux coordonnées précises définies dans l'énoncé.



##  Comment l'utiliser ?

1. Assurez-vous d'avoir **Python 3** et **Numpy** installés.
2. Placez le fichier `travailAFaire.py` dans votre dossier.
3. Lancez l'apprentissage et le test :
   ```bash
   python travailAFaire.py

