"""
Programme Principal - Generateur de Programme d'Entrainement
Flux automatique: muscle.py -> exercise.py -> choose.py -> programme final
"""

def main():
    """
    Fonction principale - lance automatiquement le flux complet
    """
    # Etape 1: Selection des objectifs musculaires 
    try:
        import muscle
        muscle.main()
    except Exception as e:
        print(f"Erreur lors de la selection des muscles: {e}")
        return
    
    # Etape 2: Selection des exercices 
    try:
        import exercise
        exercise.main()
    except Exception as e:
        print(f"Erreur lors de la selection des exercices: {e}")
        return
    
    # Etape 3: Choix du nombre de jours
    try:
        import choose
        nb_jours = choose.main()
        if nb_jours is None:
            return
    except Exception as e:
        print(f"Erreur lors du choix du nombre de jours: {e}")
        return
    
    # Générer et print le programme
    try:
        from prog import create_complete_program
        programme = create_complete_program(nb_jours)
        
    except Exception as e:
        print(f"Erreur lors de la generation du programme: {e}")

if __name__ == "__main__":
    main()

