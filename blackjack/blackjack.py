import random

#APUESTA
wallet = int(500)

#MAZO DE CARTAS
A, J, Q, K = 1, 10, 10, 10
card_numbers = ["A"] + list(range(2,11)) + ["J", "Q", "K"]
card_suits = ["Picas", "Corazones", "Diamantes", "Treboles"]
deck_of_cards = [(card_number, card_suit) for card_number in card_numbers for card_suit in card_suits]

def apostar():
    global wallet
    apuesta = int(input("Realiza una apuesta: \n"))
    while True: 
        if apuesta > wallet:
            print("No tienes el saldo suficiente")
        else:
            print("Apuesta realizada")
            wallet -= apuesta
            break

def repartir_carta():
    random_card = random.choice(deck_of_cards)
    print(random_card)
    deck_of_cards.remove(random_card)
    return random_card

def calcular_puntos(hand):
    points = 0
    aces = 0

    for card_number, card_suit in hand:
        if card_number == "A":
            points += 1
            aces += 1
        elif card_number in ["J", "Q", "K"]:
            points += 10
        else:
            points += card_number

    while aces > 0 and points + 10 <= 21:
        points += 10
        aces -= 1

    return points
    

def bjgame():
    dealer_points = 0
    user_points = 0
    print("Wallet: ", wallet)

    apostar()

    #INICIO DEL JUEGO
    dealer_hand = []
    user_hand = []
    print("Repartiendo... ")

    #REPARTIR LAS CARTAS ENTRE EL DEALER Y EL JUGADOR
    dealer_hand.append(repartir_carta())
    user_hand.append(repartir_carta())
    dealer_hand.append(repartir_carta())
    user_hand.append(repartir_carta())

    dealer_points = calcular_puntos(dealer_hand)
    user_points = calcular_puntos(user_hand)

    #NOMBRAR LAS CARTAS DE CADA UNO
    print("Your hand: ", user_hand, user_points)
    
    print("Dealer's hand: ", dealer_hand, dealer_points)

# Permite importar este módulo desde la interfaz gráfica sin iniciar
# el menú de consola automáticamente.
if __name__ == '__main__':
    print("1. Iniciar Juego")
    print("2. Cerrar")
    while True:
        user_choice = int(input("¿? "))
        if user_choice == 1:
            bjgame()
        elif user_choice == 2:
            break

