
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from weather_tool import get_weather


# STEP 1: Load environment variables
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


# STEP 2: Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


# STEP 3: Define the weather tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather information for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


# STEP 4: Initialize conversation history
messages = [
    {
        "role": "system",
        "content": (
            "You are a reliable AI weather assistant.\n"
            "1. Use get_weather for requests about current weather.\n"
            "2. Never invent temperatures, weather conditions, or observations.\n"
            "3. Use actual weather tool results when answering.\n"
            "4. If the tool returns an error, explain it clearly.\n"
            "5. Understand English, Hindi, and Hinglish queries.\n"
            "6. Respond in the same language as the user.\n"
            "7. Keep responses concise, friendly, and factual.\n"
            "8. Use previous conversation messages to understand follow-up questions.\n"
            "9. If the user asks something unrelated to weather, politely explain your purpose."
        )
    }
]


# STEP 5: Process user queries
def run_agent(user_query):

    # Add user question to conversation history
    messages.append({
        "role": "user",
        "content": user_query
    })

    # First API call: Ask AI whether to use a tool
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    first_usage = response.usage
    assistant_message = response.choices[0].message

    # Check whether AI wants to call a tool
    if assistant_message.tool_calls:

        # Store AI tool-call decision
        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Execute the weather tool
            if tool_name == "get_weather":

                print("\nFetching weather data...")

                weather_result = get_weather(
                    arguments["city"]
                )

                # Check whether the weather tool returned an error
                if "error" in weather_result:
                    print(
                        f"\nWeather Error: {weather_result['error']}"
                    )

                # Send tool result back to AI
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(weather_result)
                })

        # Second API call: Generate final response
        final_response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )

        second_usage = final_response.usage

        # Store final AI response in conversation history
        final_message = final_response.choices[0].message
        messages.append(final_message)

        # Calculate combined token usage
        total_prompt = (
            first_usage.prompt_tokens +
            second_usage.prompt_tokens
        )

        total_completion = (
            first_usage.completion_tokens +
            second_usage.completion_tokens
        )

        total_tokens = (
            first_usage.total_tokens +
            second_usage.total_tokens
        )

        # Display API usage
        print("\n========== API USAGE ==========")

        print("\nFirst API Call (Tool Selection)")
        print(f"Model: {response.model}")
        print(f"Prompt tokens: {first_usage.prompt_tokens}")
        print(f"Completion tokens: {first_usage.completion_tokens}")
        print(f"Total tokens: {first_usage.total_tokens}")

        print("\nSecond API Call (Final Response)")
        print(f"Model: {final_response.model}")
        print(f"Prompt tokens: {second_usage.prompt_tokens}")
        print(f"Completion tokens: {second_usage.completion_tokens}")
        print(f"Total tokens: {second_usage.total_tokens}")

        print("\nCombined Usage")
        print(f"Total prompt tokens: {total_prompt}")
        print(f"Total completion tokens: {total_completion}")
        print(f"Total tokens consumed: {total_tokens}")

        print("===============================")

        return final_message.content

    # If AI doesn't call a tool, return its direct response
    messages.append(assistant_message)

    print("\n========== API USAGE ==========")
    print(f"Model: {response.model}")
    print(f"Prompt tokens: {first_usage.prompt_tokens}")
    print(f"Completion tokens: {first_usage.completion_tokens}")
    print(f"Total tokens: {first_usage.total_tokens}")
    print("===============================")

    return assistant_message.content


# STEP 6: Start continuous conversation
if __name__ == "__main__":

    print("\nAI Weather Agent")
    print("------------------------------")
    print("Ask me about the weather.")
    print("Type 'exit' to stop.\n")

    while True:

        query = input("You: ")

        if query.lower().strip() == "exit":
            print("\nWeather Agent: Goodbye!")
            break

        if not query.strip():
            continue

        try:
            answer = run_agent(query)

            print("\nWeather Assistant:")
            print(answer)

        except Exception as error:
            print(f"\nSomething went wrong: {error}")

        print("\n------------------------------")
