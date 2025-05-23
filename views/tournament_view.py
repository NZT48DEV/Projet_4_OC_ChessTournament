class CreateTournamentView:
    def display_create_tournament_menu(self):
        print("\n" + "=" * 40)
        print("🏆    CRÉATION D'UN TOURNOI    🏆")
        print("=" * 40)

        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date = input("Date de début (JJMMAAA) : ")
        end_date = input("Date de fin (JJMMAAAA) : ")
        number_of_rounds = input("Nombre de rounds (par défaut 4): ")
        description = input("Description/Remarques : ")

        return {
            "name": name.strip(),
            "location": location.strip(),
            "start_date": start_date.strip(),
            "end_date": end_date.strip(),
            "number_of_rounds": int(number_of_rounds) if number_of_rounds.strip().isdigit() else 4,
            "description": description.strip()
        }