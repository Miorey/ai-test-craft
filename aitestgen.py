import os
import openai
import click
import json
from pathlib import Path


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--open-ai-env-var', required=False)
def generate_test(filepath: str, open_ai_env_var: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not filepath:
        raise click.ClickException('File is not set')
    file_path = Path(filepath)

    if not file_path.exists():
        raise click.ClickException(f'File is not {filepath} not exists')

    if file_path.suffix != ".json":
        raise click.ClickException("File does not have a .json extension.")

    try:
        with file_path.open('r') as f:
            setup = json.load(f)
        print(setup)
    except (IOError, json.JSONDecodeError) as e:
        raise click.ClickException(f"Unable to read json file {filepath}")

    execute_test_cover(setup)


def execute_test_cover(gen_setup: dict[str, str|list[dict[str, str]]]):
    language = gen_setup["language"]
    for to_cover in gen_setup["files"]:
        with open(to_cover["code"], 'r') as file:
            content = file.read()

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a f{language} developer"},
                {
                    "role": "user", "content": f"""
                    Write the unit test of the following code. 
                    The test should follow those rules:
                     - THE TEST SHOULD COVER 100% of the code
                     - In the imports take in account that the test is in {to_cover["code"]} and the test in {to_cover["test"]}
                     
                    Your answear sshould contain:
                     - no syntax highlighting
                     - no introduction or explanation
                     - ALL the test should be in the same snippet
                    ```
                        {content}
                    ```
                    """
                 }
            ]
        )

        print(completion)

        s = completion["choices"][0]["message"]["content"]
        s = s.replace("```", "")

        with open(to_cover["test"], 'w') as f:
            f.write(s)




if __name__ == '__main__':
    generate_test()

# openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.api_key)


