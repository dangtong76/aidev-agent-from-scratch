import openai
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = openai.OpenAI()
    message_list = []
    
    while True:
        user_input = input("Chat> ").strip()
        if user_input.lower() in ["exit","e"]:
            break
        if not user_input:
            continue

        message_list.append(
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_input
                    }
                ]
            }
        )
        response_msg = llm_request(client, message_list)
        print("after llm-request")

        if response_msg:
            print(f"AI > {response_msg}")
            print(message_list)
        else:
            break

def llm_request(client, message_list):
    try:
        print("start request to llm")
        response = client.responses.create(
            model="gpt-4o-mini",
            input=message_list,
            # temperature=0.5,
            # max_tokens=1000
        )
        print("end request to llm")
        if response.output_text:
            response_msg = response.output_text
            # message_list += response.output
            message_list.append(
                {
                        "type": "message",
                        "role": "assistant", 
                        "content": [
                            {
                                "type": "output_text",
                                "text": response_msg
                            }
                        ]
                }
            )
            return response_msg
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    main()