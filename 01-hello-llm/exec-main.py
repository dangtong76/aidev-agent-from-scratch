import openai
from dotenv import load_dotenv
import base64

def get_base64_image(file_path):
    with open(file_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return base64_data 

def main():
    load_dotenv()
    client = openai.OpenAI()
    b64_data = get_base64_image("resources/draw.png")
    response = client.responses.create(
        model = "gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "이 이미지 설명해줘"},
                    {
                        "type": "input_image", 
                        "image_url": f"data:image/png;base64,{b64_data}"
                    },
                ],
            }
        ],
        temperature=0.5,
        max_output_tokens=100
    )
    print(response.output_text)
if __name__ == "__main__":
    main()