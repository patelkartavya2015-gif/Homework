import random

choices = ["rock", "paper", "scissors"]

def player_choice():
    while True:
        choice = input("Enter your choice (rock, paper, scissors): ").strip().lower()
        if choice in choices:
            return choice
        print("Invalid choice. Please choose rock, paper, or scissors.")

def computer_choice():
    return random.choice(choices)

def determine_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (
        (player == "rock" and computer == "scissors") or 
        (player == "paper" and computer == "rock") or 
        (player == "scissors" and computer == "paper")
    ):
        return "You win!"
    else:
        return "Computer wins!"

def play_game():
    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        player = player_choice()
        computer = computer_choice()
        
        print(f"\nYou chose: {player}")
        print(f"Computer chose: {computer}")
        
        result = determine_winner(player, computer)
        print(f"*** {result} ***\n")
        
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again not in ["y", "yes"]:
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()