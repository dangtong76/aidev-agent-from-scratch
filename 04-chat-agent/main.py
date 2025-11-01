import openai, json
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = openai.OpenAI()
    message_list = []


    while True:
        user_input = input("Chat> ").strip()
        if user_input in ("exit", "e"):
            break
        if not user_input:
            continue
        message_list.append({
            "role":"user",
            "content": [{"type": "input_text", "text": user_input}]
        })

        response = llm_request(client, message_list)
        if response:
            process_ai_response(client, response, message_list)
        else:
            break


def llm_request(client, message_list):
    try:
        # print("start call llm")
        response = client.responses.create(
            # model="claude-3.7-sonnet-reasoning-gemma3-12b",
            model="gpt-4o-mini",
            input = message_list,
            tools = TOOLS
        )  
        # ai_message = response.output[0].content[0].text
        # print("end call llm and return response")
        return response
        
    except Exception as e:
        print(f"Error {e}")
        return None
    
def process_ai_response(client, response, message_list):
    # print(response)
    message_list += response.output
    pending_calls = []
    for out in response.output:
        if out.type == "function_call":  # response output 중에 function_call 인것만 처리, 나머지는 skip
            pending_calls.append(out)
    if pending_calls:
        for call in pending_calls: 
            function_name = call.name
            args = {}
            try:
                args = json.loads(call.arguments) if call.arguments else {}
            except json.JSONDecodeError:
                pass

            function_to_run = FUNCTION_MAP.get(function_name)

            if not function_to_run:
                continue
            result = function_to_run(**args) # tool 실행

            # 도구 결과를 메시지에 추가 (올바른 형식)
            message_list.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps({
                    "result": result
                })
            })

        # print("도구 실행 완료, 다시 LLM 호출")
        final_response = llm_request(client, message_list)
        if final_response:
            # 최종 응답 출력
            print(f"AI: {final_response.output_text}")
    else:
        print(f"AI(normal): {response.output_text}")



def get_weather(location):
    return f"{location}의 현재 날씨는 맑음, 온도는 25도 입니다."

FUNCTION_MAP = {
    'get_weather': get_weather
}

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current weather of a given locaiton",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The name of the location to get the weather for"
                },
            },
            "required": ["location"]
        }   
    }
]

if __name__ == "__main__":
    main()