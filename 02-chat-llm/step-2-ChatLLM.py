import openai
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = openai.OpenAI()
    
    while True:
        user_input = input("Chat> ").strip()
        if user_input.lower() in ["exit","e"]:
            break
        if not user_input:
            continue
        response = client.responses.create(
            model="gpt-4o-mini",
            input=user_input
        )
        ai_message = response.output_text
        print(f"AI > {ai_message}")

if __name__ == "__main__":
    main()