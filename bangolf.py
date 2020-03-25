
result_list = []

def main():
    ''' Huvudfunktion, styr programmet ''' 
    welcome("Klubbmästerskap i BANGOLF! ")
  
    choice = None
    games = get_result()
    
    

    while choice != 4:
        print_menu()
        try:    
            choice = int(input("Val: "))
        except: 
            print("Ditt val måste vara 1, 2 eller 3! ")
            continue
        
        if choice == 1:
            print_score(games)
            
        elif choice == 2:
            add_player_result(games)
        elif choice == 3: 
            delete_score()
        elif choice == 4: 
            save_result_to_file(games)
            break
    welcome("Välkommen åter! ")

def welcome(text):
    ''' Hälsar användaren vid start och avslut av programmet ''' 
    print("*" * 35)
    print(text)
    print("*" * 35)

def print_menu():
    print("\n Meny")
    print("*" * 6 + "\n")
    print("1) Visa resultat ")
    print("2) Registrera resultat ")
    print("3) Radera resultat ")
    print("4) Spara resultat & avsluta ")
  
    
def add_player_result(games):
    ''' funktion som ber anv om input och sparar i ett temporärt lexikon för att sedan till sist läggas till i den globala listan ''' 
    save_temporary = {}

    while True:
        try:
    
            save_temporary["namn"] = input("namn: ")
            save_temporary["Varv1"] = int(input("varv 1: "))
            save_temporary["Varv2"] = int(input("varv 2: "))
            save_temporary["Varv3"] = int(input("varv 3: "))
            break
        except ValueError: 
            print("Dina poäng måste vara i siffror")
            
    
    result_list.append(save_temporary)

def get_result():
    
    ''' Öppnar filen i läsläge och går igenom lexikonen i listan  för att semikolonseparera och göra det enklare att hämta ut olika delar '''
    try:
        result_file = open("result.txt", "r")
        games = result_file.read()

        for game in games.split("\n"):
            if game != "":
                result_info = game.split(";")
                result_list.append({
                    "namn": result_info[0],
                    "Varv1": result_info[1],
                    "Varv2": result_info[2],
                    "Varv3": result_info[3]
                })

    except FileNotFoundError:
        print("Det gick inte att hitta filen")

    return result_list

def save_result_to_file(games):
    ''' Öppnar filen i skrivläge och skriver ut allt i listan, både de "gamla" och nya resultaten. När man trycker avsluta så sparar man alltså ''' 
    result_file = open("result.txt", "w")
    
    for game in games:
        result_file.write("{};{};{};{}\n".format(game["namn"], game["Varv1"], game["Varv2"], game["Varv3"]))

    result_file.close()  

def delete_score():
    ''' Funktion som raderar namn och resultat ''' 
    
    delete_player = input("Namnet på spelaren du vill ta bort: ")
    for obj in result_list:
        if obj["namn"] == delete_player:
            result_list.remove(obj)
            print(delete_player + " har raderats")
            return
    print(delete_player + " hittas ej i resultatlistan")

def get_total_score(Varv1, Varv2, Varv3):
    ''' Hämtar in resultat och sparar de i variabler för att räkna ihop totalen
        och sedan skicka tillbaka till funktionen som printar ''' 
    p1 = int(Varv1)
    p2 = int(Varv2)
    p3 = int(Varv3)

    tot = p1+p2+p3
    tot = str(tot)
    return tot

def get_average(Varv1, Varv2, Varv3):
    ''' Hämtar in resultat och sparar i variabler för att räkna ut snittet och skicka tillbaka ''' 
    a1 = int(Varv1)
    a2 = int(Varv2)
    a3 = int(Varv3)

    average = round((a1 + a2 + a3)/ 3, 1)
    average = str(average)
    return average

def print_score(games):
    ''' Skriver ut namn, resultat, total och snitt ''' 
    print("\n{:>15}".format("Resultat: "))
    print("-"*87)
    print("{} {:>20} {:>15} {:>15} {:>10} {:>10}".format("Deltagare: ", "Runda 1", "Runda 2", "Runda 3", "Totalt", "Snitt"))
    print("-"*87)
    for game in games:
        tot = get_total_score(game["Varv1"], game["Varv2"], game["Varv3"])
        average = get_average(game["Varv1"], game["Varv2"], game["Varv3"])
        print("{:>15} {:>10} slag {:>10} slag {:>10} slag {:>10}p {:>10}".format(game["namn"], game["Varv1"], game["Varv2"], game["Varv3"], tot, average))

main()

def name():
    nameoffile = input("titel: ")
    content = input("Innehåll: ")
    name = nameoffile +'.txt'

    try:
        file = open(name, "w")
        file.write(content)
        file.close()
        return file
    except:
        print("Something went wrong")

name()



 % for title in wiki:
        <a href="wiki/article_name" target="_blank"></a>
        % end