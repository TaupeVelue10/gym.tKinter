#!/usr/bin/env python3

"""
Programme Principal - Generateur de Programme d'Entrainement
Flux automatique: muscle.py -> exercise.py -> choose.py -> programme final
"""

def main():
    """
    Fonction principale - lance automatiquement le flux complet
    """
    print("GENERATEUR DE PROGRAMME D'ENTRAINEMENT")
    print("=" * 50)
    
    # Etape 1: Selection des objectifs musculaires
    print("\nEtape 1: Selection des objectifs musculaires")
    try:
        import muscle
        # Utilise l'interface tkinter originale de muscle.py
        muscle.main()  # Appelle la fonction main() de muscle.py
    except Exception as e:
        print(f"Erreur lors de la selection des muscles: {e}")
        return
    
    # Etape 2: Selection des exercices
    print("\nEtape 2: Selection des exercices")
    try:
        import exercise
        # Utilise l'interface tkinter originale d'exercise.py
        exercise.main()  # Appelle la fonction main() d'exercise.py
    except Exception as e:
        print(f"Erreur lors de la selection des exercices: {e}")
        return
    
    # Etape 3: Choix du nombre de jours
    print("\nEtape 3: Choix du nombre de jours d'entrainement")
    try:
        import choose
        # Utilise l'interface tkinter originale de choose.py
        nb_jours = choose.main()  # Appelle la fonction main() de choose.py
        if nb_jours is None:
            print("Aucun nombre de jours selectionne")
            return
        print(f"Nombre de jours selectionne: {nb_jours}")
    except Exception as e:
        print(f"Erreur lors du choix du nombre de jours: {e}")
        return
    
    # Etape 4: Generation du programme final
    print("\nEtape 4: Generation du programme d'entrainement")
    try:
        from prog import create_complete_program
        programme = create_complete_program(nb_jours)
        
        if programme is None:
            print("Erreur: Impossible de generer le programme")
        else:
            print("\nProgramme genere avec succes!")
            
    except Exception as e:
        print(f"Erreur lors de la generation du programme: {e}")
    
    print("\nProcessus termine.")

if __name__ == "__main__":
    main()

