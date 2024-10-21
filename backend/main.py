from chain import get_food_recommendation_with_db


def main():
    # Use a fixed session_id for now, in real use this could be a unique user ID or token
    session_id = "session_1"

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Call the function with the session_id
        response = get_food_recommendation_with_db(user_input, session_id)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
