from openai import OpenAI
from conf_representation import ProjectConfig
from halo import Halo
import os

open_ai_client = OpenAI()


def setup_open_ai_client(open_ai_env_var: str | None):
    open_ai_client.api_key = os.getenv(open_ai_env_var or "OPENAI_API_KEY")


def execute_test_cover(gen_setup: ProjectConfig):
    language = gen_setup.language
    conversation_history: list[dict[str, str]] = [{"role": "system", "content": f"You are a f{language} developer"}]

    spinner = Halo(text="Yolo", spinner='dots')
    for to_cover in gen_setup.files:
        spinner.start(to_cover.code)
        # AI-TEST: Mock the open usage to avoid FileNotFound exception
        with open(to_cover.code, 'r') as file:
            content = file.read()
        additional_comments: list[str] = gen_setup.additional_comments

        conversation_history.append(
            {
                "role": "user",
                "content": f"""
                            Write the unit test of the following code. 
                            The test should follow those rules:
                             - THE TEST SHOULD COVER 100% of the code.
                             - In the imports take in account that the test is in {to_cover.code} and the test in {to_cover.test}.
                             - The comments starting with `AI-TEST:` take them in consideration. 
                             - {', '.join(additional_comments)}
                             - BE SURE YOU USE ONLY THAT YOU WELL `import` the requirements.
                             - The test should be simple and with a cyclomatic complexity as lower as possible.

                            Your answer should contain:
                             - NO SYNTAX HIGHLIGHTING.
                             - no introduction or explanation.
                             - ALL the test should be in the same snippet.
                            ```
                                {content}
                            ```
                            """
            }
        )

        # AI-TEST: mock the following openai call
        completion = open_ai_client.chat.completions.create(
            model=gen_setup.model,
            messages=conversation_history
        )
        ai_answer = completion.choices[0].message.content
        conversation_history.append({'role': 'assistant', 'content': ai_answer})
        only_code = ai_answer.replace("```", "")
        with open(to_cover.test, 'w') as f:
            f.write(only_code)
        spinner.succeed()