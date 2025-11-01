import openai
from dotenv import load_dotenv

def main():
    load_dotenv()
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt="Hello, how are you?",
        max_tokens=100,
        temperature=0.5
    )
    print(response.choices[0].text)

if __name__ == "__main__":
    main()