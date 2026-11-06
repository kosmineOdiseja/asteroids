import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(
    client: OpenAI,
    messages: list,
    verbose: bool,
) -> None:
    max_iterations = 20

    for iteration in range(max_iterations):
        if verbose:
            print(f"\nIteration: {iteration + 1}/{max_iterations}")

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message

        # Pirmiausia į istoriją įrašome modelio atsakymą.
        messages.append(message)

        if verbose and response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Jei funkcijų nebeprašo, užduotis baigta.
        if not message.tool_calls:
            print("Final response:")
            print(message.content)
            return

        # Vykdome visas šiame atsakyme prašomas funkcijas.
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)

            if not result_message.get("content"):
                raise RuntimeError(
                    "Function call returned empty content"
                )

            # Pridedame rezultatą, kad kitame cikle modelis jį matytų.
            messages.append(result_message)

            if verbose:
                print(f"-> {result_message['content']}")

    print(
        "Error: Agent reached the limit of 20 iterations "
        "without producing a final response."
    )
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="Prompt to send to the LLM"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    load_dotenv()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    generate_content(client, messages, args.verbose)

if __name__ == "__main__":
    main()