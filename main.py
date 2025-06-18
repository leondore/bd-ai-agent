import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import MODEL, FEEDBACK_LIMIT
from prompts import system_prompt
from tools import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    config = types.GenerateContentConfig(
        system_instruction=system_prompt, tools=[available_functions]
    )

    final_response = ""
    feedback_loop = 0
    while feedback_loop < FEEDBACK_LIMIT:
        response = client.models.generate_content(
            model=MODEL, contents=messages, config=config
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls:
            final_response = response.text
            break

        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response.response
            ):
                raise Exception("empty function call result")

            messages.append(function_call_result)

    print("Final response:")
    print(final_response)


if __name__ == "__main__":
    main()
