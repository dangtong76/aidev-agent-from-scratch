import openai
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = openai.OpenAI()
    response = client.responses.create(
        model = "gpt-4o",
        input = "안녕? 만나서 반가워!",
        temperature=0.5,
        max_output_tokens=100
    )
    print(response.output_text)
if __name__ == "__main__":
    main()