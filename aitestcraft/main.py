import os
import click
import json
from pathlib import Path
from .validators import validate_inputs
from .ai_generator import execute_test_cover
from .conf_representation import project_config_factory
from openai import OpenAI


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--open-ai-env-var', required=False)
def generate_test(filepath: str, open_ai_env_var: str | None):
    # AI-TEST: don't test this function
    validate_inputs(filepath, open_ai_env_var)
    open_ai_api_key = os.getenv(open_ai_env_var or "OPENAI_API_KEY")
    file_path = Path(filepath)

    with file_path.open('r') as f:
        setup_json = json.load(f)
        setup = project_config_factory(setup_json)
        execute_test_cover(setup, OpenAI(api_key=open_ai_api_key))


# AI-TEST: don't test this condition
if __name__ == '__main__':
    generate_test()
