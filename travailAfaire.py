import numpy as np
import random

# --- SECTION 1 : MODÉLISATION DE L'ENVIRONNEMENT  ---
LIGNES = 4
COLONNES = 5
# Définition du dictionnaire d'actions autorisées 
MOUVEMENTS = ["Haut", "Bas", "Gauche", "Droite", "Récupérer", "Déposer"]
NB_ACTIONS = len(MOUVEMENTS)

# Coordonnées basées sur la figure (conversion index 0 pour Python) [cite: 4, 8, 9]
POSITION_DEPART = (0, 0)      # Point D (Ligne 4, Col 1 dans l'énoncé) 
ZONE_LIVRAISON = (3, 4)       # Point S (Ligne 1, Col 5) 
EMPLACEMENT_OBJETS = [(3, 0), (0, 3)] # Points O (1,1) et (4,4) 
CELLULES_BLOQUEES = [(0, 1), (3, 2)]  # Obstacles (cases noires du schéma)

# --- SECTION 2 : LOGIQUE DE L'AGENT ---

def calculer_identifiant_etat(lig, col, possede_item):
    """ 
    Génère un index numérique pour chaque situation possible.
    Calcul : (Position dans la grille) + (Décalage si un objet est porté)
    Nombre total d'états : 4x5 x 2 = 40 états.
    """
    return (lig * COLONNES + col) + (20 if possede_item else 0)

def verifier_collision(lig, col, n_lig, n_col):
    """ Vérifie si le déplacement vers la case cible est autorisé  """
    # Sortie de grille
    if not (0 <= n_lig < LIGNES and 0 <= n_col < COLONNES):
        return False
    # Collision avec une case noire
    if (n_lig, n_col) in CELLULES_BLOQUEES:
        return False
    # Mur vertical spécifique entre les colonnes 3 et 4 sur le haut de la grille
    if lig in [0, 1] and n_lig in [0, 1]:
        if (col == 2 and n_col == 3) or (col == 3 and n_col == 2):
            return False
    return True

# --- SECTION 3 : APPRENTISSAGE (Q-LEARNING)  ---

# Initialisation de la Q-Table avec des zéros
table_q = np.zeros((40, NB_ACTIONS))

# Paramètres de l'algorithme
taux_apprentissage = 0.1   # Alpha
facteur_remise = 0.9      # Gamma
taux_exploration = 0.2    # Epsilon
nb_cycles = 5000

print("Initialisation du Q-Learning : Entraînement de l'agent en cours...")

for ep in range(nb_cycles):
    lig, col = POSITION_DEPART
    sac_plein = False
    fini = False
    
    while not fini:
        etat_actuel = calculer_identifiant_etat(lig, col, sac_plein)
        
        # Sélection de l'action : Exploration ou Exploitation
        if random.uniform(0, 1) < taux_exploration:
            action_choisie = random.randint(0, NB_ACTIONS - 1)
        else:
            action_choisie = np.argmax(table_q[etat_actuel])
            
        n_lig, n_col = lig, col
        gain = -1 # Coût systématique d'un mouvement 
        
        # Traitement des actions de déplacement
        if action_choisie == 0: # Monter
            if verifier_collision(lig, col, lig-1, col): n_lig = lig - 1
        elif action_choisie == 1: # Descendre
            if verifier_collision(lig, col, lig+1, col): n_lig = lig + 1
        elif action_choisie == 2: # Gauche
            if verifier_collision(lig, col, lig, col-1): n_col = col - 1
        elif action_choisie == 3: # Droite
            if verifier_collision(lig, col, lig, col+1): n_col = col + 1
            
        # Traitement des actions spéciales 
        elif action_choisie == 4: # Récupérer
            if (lig, col) in EMPLACEMENT_OBJETS and not sac_plein:
                sac_plein = True
                gain = 5 # Bonus intermédiaire
            else:
                gain = -10 # Pénalité : mauvais endroit 
                
        elif action_choisie == 5: # Déposer
            if (lig, col) == ZONE_LIVRAISON and sac_plein:
                gain = 20 # Succès de la mission [cite: 16]
                fini = True 
            else:
                gain = -10 # Pénalité : mauvais endroit ou vide 

        # Mise à jour de la connaissance (Équation de Bellman)
        etat_suivant = calculer_identifiant_etat(n_lig, n_col, sac_plein)
        meilleure_q_suivante = np.max(table_q[etat_suivant])
        
        # Formule du Q-Learning
        table_q[etat_actuel, action_choisie] += taux_apprentissage * \
            (gain + facteur_remise * meilleure_q_suivante - table_q[etat_actuel, action_choisie])
        
        lig, col = n_lig, n_col

print("Apprentissage terminé. Le robot est prêt pour le test.\n")

# --- SECTION 4 : DÉMONSTRATION DU CHEMIN OPTIMAL ---

def executer_test():
    print("--- PARCOURS DU ROBOT APRÈS APPRENTISSAGE ---")
    lig, col = POSITION_DEPART
    sac_plein = False
    limite_mouvements = 25
    
    for etape in range(limite_mouvements):
        id_etat = calculer_identifiant_etat(lig, col, sac_plein)
        action = np.argmax(table_q[id_etat])
        
        # Affichage lisible pour l'utilisateur
        statut_objet = "OUI" if sac_plein else "NON"
        print(f"Étape {etape+1} | Case: ({4-lig},{col+1}) | Action: {MOUVEMENTS[action]} | Objet porté: {statut_objet}")
        
        if action == 0: lig -= 1
        elif action == 1: lig += 1
        elif action == 2: col -= 1
        elif action == 3: col += 1
        elif action == 4: sac_plein = True
        elif action == 5 and (lig, col) == ZONE_LIVRAISON:
            print("\nRESULTAT : L'agent a déposé l'objet avec succès au point S.")
            break

executer_test()