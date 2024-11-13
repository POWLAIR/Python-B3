import random
import os
import time

def generer_niveau():
    niveau = [[random.randint(0, 1) for _ in range(10)] for _ in range(5)]
    niveau[random.randint(0, 4)][random.randint(0, 9)] = 2  
    return niveau

def nettoyer_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_carte(niveau, position):
    print("\n" + "="*40)
    for y, ligne in enumerate(niveau):
        for x, salle in enumerate(ligne):
            if (y, x) == position:
                print("🚶", end=" ")  
            elif salle == 2:
                print("🏆", end=" ")  
            elif salle == 1:
                print("👹", end=" ")  
            else:
                print("⬜", end=" ")  
        print()
    print("="*40)

def traverse_donjons(niveau, vie):
    position = (0, 0)

    while True:
        nettoyer_console()
        afficher_carte(niveau, position)
        y, x = position
        print(f"\nVie restante: {vie}❤️")
        print("Utilisez 'z' pour haut, 's' pour bas, 'q' pour gauche, 'd' pour droite. Appuyez sur 'a' pour quitter.")

        # Gérer la rencontre avec un ennemi
        if niveau[y][x] == 1:
            print("\n👹 Un ennemi est dans cette salle!")
            dice = random.randint(1, 6)
            if dice == 1:
                print(f"   🎲 Résultat dé: {dice} - Tu as battu l'ennemi!")
            else:
                vie -= 1
                print(f"   🎲 Résultat dé: {dice} - L'ennemi t'a battu! (-1❤️)")
            niveau[y][x] = 0  
            time.sleep(1)

        if vie <= 0:
            print("\n❌ Game Over! Tu n'as plus de vie.")
            time.sleep(2)
            return False

        if niveau[y][x] == 2:
            print("\n🏆 Félicitations! Tu as trouvé le trophée et terminé le donjon!")
            time.sleep(2)
            return True

        choix = input("Direction : ").lower()
        if choix == 'q' and x > 0:
            position = (y, x - 1)
        elif choix == 'd' and x < 9:
            position = (y, x + 1)
        elif choix == 'z' and y > 0:
            position = (y - 1, x)
        elif choix == 's' and y < 4:
            position = (y + 1, x)
        elif choix == 'a':  
            print("\nVous avez quitté le jeu.")
            time.sleep(1)
            return False
        else:
            print("Direction invalide. Essayez encore.")
            time.sleep(1)

def main():
    
    nbr_victoire = 0
    nbr_victoire_max = 2
    vie = 10
    tentatives = 0
    
    while nbr_victoire < nbr_victoire_max:
        for i in range(nbr_victoire_max):
            victoire = False
            while not victoire:
                nettoyer_console()
                print(f"\n{'='*20} Tentative {tentatives} {'='*20}")
                niveau = generer_niveau()
                victoire = traverse_donjons(niveau, vie)
                if not victoire:
                    tentatives += 1
            nbr_victoire += 1
        

    print(f"\nTu as réussi après {tentatives} tentative{'s' if tentatives > 1 else ''}!")

if __name__ == "__main__":
    main()
