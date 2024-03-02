import random

def coin_flip_illusion():
    print("Let's flip a coin! Heads or tails?")
    user_choice = input("Enter your choice (heads/tails): ").lower()

    # Regardless of input, the outcome is predetermined (Illusion of Choice)
    result = random.choice(["heads", "tails"])

    print("The coin flips...")
    print(f"It's {result}!")

    if user_choice == result:
        print("You guessed correctly!")
    else:
        print("Better luck next time!")

coin_flip_illusion()