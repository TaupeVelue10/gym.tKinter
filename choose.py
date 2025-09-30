def main():
    """Interface simple pour choisir le nombre de jours d'entrainement"""
    while True:
        try:
            nb_jours = int(input("Entrez le nombre de jours d'entrainement (2-6): "))
            if 2 <= nb_jours <= 6:
                return nb_jours
            else:
                print("Veuillez entrer un nombre entre 2 et 6.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    days = main()
    print(f"Nombre de jours selectionne: {days}")
