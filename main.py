import os, sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("Usage: python main.py <prompt>")
    sys.exit(1)

verbose = False
prompt = sys.argv[1]
if len(sys.argv) > 2:
    verbose = sys.argv[2] == "--verbose"

client = genai.Client(api_key=api_key)

messages = [genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

print(response.text)

if verbose:
    print("User prompt:", prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
