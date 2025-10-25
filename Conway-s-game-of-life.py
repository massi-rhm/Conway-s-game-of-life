"""
Jeu de la Vie 
Auteur : Massinissa RAHEM
Description : Simulation du "Jeu de la Vie" de Conway sur une grille 7x7.
"""

import numpy as np
import time

def creer_grille(nb_lignes=7, nb_colonnes=7, cellules_vivantes=None):
    """
    Crée une grille initiale avec des cellules mortes (0) et vivantes (1).(valeur par défaut 7 si on indique rien)
    - nb_lignes, nb_colonnes : dimensions de la grille
    - cellules_vivantes : liste de coordonnées (ligne, colonne) à rendre vivantes par défaut None
    """

    grille = np.zeros((nb_lignes, nb_colonnes), dtype=int) 
    # grille initiale 2D de forme (nb_lignes, nb_colonnes) remplie de zéros 
    #dtype=int signifie que les valeurs sont des entiers (0 ou 1)
    #On stocke ce tableau dans la variable grille

    if cellules_vivantes: #Vérifie si cellules_vivantes a été donnée (et n’est pas None ni une liste vide)
        for (i, j) in cellules_vivantes:
            if 0 <= i < nb_lignes and 0 <= j < nb_colonnes: #Vérifie que les coordonnées sont dans la grille (pas en dehors)
                grille[i, j] = 1 #On place la valeur 1 dans la grille à la position (i, j)
    return grille #La fonction renvoie (retourne) la grille construite

def ajouter_bordure_zero(grille):
    """Ajoute une bordure de zéros autour de la grille pour simplifier les calculs."""
    return np.pad(grille, pad_width=1, mode='constant', constant_values=0)
#np.pad(...) ajoute un rembourrage autour du tableau
#pad_width=1 ajoute 1 ligne/colonne de chaque côté (haut, bas, gauche, droite)
#mode='constant' et constant_values=0 remplissent ce rembourrage avec des zéros

def compter_voisins(grille_paddee, i, j):
    """
    Compte les voisins vivants de la cellule (i,j) dans la grille paddée.
    Une cellule a jusqu’à 8 voisins (haut, bas, gauche, droite, diagonales).
    """
    total = grille_paddee[i-1:i+2, j-1:j+2].sum()
    #Ici on prend une sous-matrice autour de (i, j) :
    #i-1:i+2 signifie lignes i-1, i, i+1 (en Python la fin i+2 est exclue, donc on prend 3 lignes)
    #j-1:j+2 idem pour les colonnes.
    #Cette zone 3×3 contient la cellule elle-même au centre et ses 8 voisins
    #.sum() additionne toutes les valeurs (0 ou 1) dans cette sous-matrice
    #total = nombre de cellules vivantes dans ce carré 3×3 (inclut la cellule centrale si elle est vivante)
    return total - grille_paddee[i, j]  # on retire la cellule elle-même
#rend la grille_paddee (c’est important : on travaille sur la grille après ajout de bordure), et les indices i, j dans la grille paddée
#Remarque : si la grille originale est N×M, la grille paddée est (N+2)×(M+2). Les indices passent donc de 1 à N pour les lignes utiles

def calculer_generation_suivante(grille):
    """
    Calcule la prochaine génération selon les règles du Jeu de la Vie :
      - une cellule vivante survit si elle a 2 ou 3 voisins vivants
      - une cellule morte naît si elle a exactement 3 voisins vivants
    """
    lignes, colonnes = grille.shape
    #grille.shape donne la forme (taille) du tableau : (nb_lignes, nb_colonnes)
    #On assigne ces deux valeurs aux variables lignes et colonnes
    grille_paddee = ajouter_bordure_zero(grille) #On crée la version paddée de la grille (pour éviter les problèmes de bord)
    nouvelle_grille = np.zeros_like(grille) 
    #crée un nouveau tableau de même forme que grille, rempli de zéros
    #nouvelle_grille contiendra la génération suivante (on commence par tout à 0, on mettra des 1 là où il faut)
    for i in range(1, lignes + 1):
        for j in range(1, colonnes + 1):
            voisins = compter_voisins(grille_paddee, i, j)
            cellule = grille_paddee[i, j] #cellule est la même chose que grille[i-1, j-1] mais on l’obtient dans la grille paddée pour symétrie avec l’appel précédent
            
            # Application des règles
            if cellule == 0 and voisins == 3:
                nouvelle_grille[i-1, j-1] = 1
            elif cellule == 1 and (voisins == 2 or voisins == 3):
                nouvelle_grille[i-1, j-1] = 1
            else:
                nouvelle_grille[i-1, j-1] = 0
    return nouvelle_grille

def afficher_grille(grille):
    """Affiche la grille de manière lisible : # = vivant, . = mort."""
    for ligne in grille: #Parcourt chaque ligne (chaque rangée) du tableau grille.ligne est un tableau 1D représentant cette rangée
        print(' '.join('#' if cellule else '.' for cellule in ligne))
    print()

def lancer_simulation(grille_depart, nb_generations=5, delai=0.5):
    """
    Lance la simulation du Jeu de la Vie.
    - grille_depart : état initial
    - nb_generations : nombre de générations à afficher
    - delai : pause (en secondes) entre les générations
    """
    grille = grille_depart.copy() #crée une copie indépendante de la grille initiale
    #sans copy(), grille = grille_depart ferait pointer grille et grille_depart vers le même tableau ; les modifications affecteraient
    print("Génération 0 :")
    afficher_grille(grille)

    for generation in range(1, nb_generations + 1): #de 1 à nb_generations inclus
        grille = calculer_generation_suivante(grille)
        print(f"Génération {generation} :")
        afficher_grille(grille)
        time.sleep(delai) #pause de delai secondes entre chaque génération ,C’est ce qui fait la pause entre générations pour qu’on puisse voir l’évolution

# Exemple : un petit "planeur" (glider)
if __name__ == "__main__":
    motif_planeur = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    grille_initiale = creer_grille(7, 7, cellules_vivantes=motif_planeur)
    lancer_simulation(grille_initiale, nb_generations=5, delai=0.4)

#Chaque tuple (ligne, colonne) représente une cellule initialement vivante.
#Ici on suppose l’indexation commence à 0 (donc (1,2) est la 2e ligne, 3e colonne)
#Le planeur est une configuration bien connue qui se déplace sur la grille à chaque génération
#Appel de creer_grille pour créer une grille 7×7 et activer les cellules listées dans motif_planeur
#Résultat : grille_initiale est un tableau numpy 7x7 avec des 0 et quelques 1 aux positions du planeur