# main.py
from chain import get_food_recommendation_with_db

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = get_food_recommendation_with_db(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
