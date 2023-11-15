import os
import click
import json
from pathlib import Path
from validators import validate_inputs
from ai_generator import execute_test_cover, setup_open_ai_client
from conf_representation import project_config_factory


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--open-ai-env-var', required=False)
def generate_test(filepath: str, open_ai_env_var: str | None):
    # AI-TEST: don't test this function
    validate_inputs(filepath, open_ai_env_var)
    setup_open_ai_client(open_ai_env_var)
    file_path = Path(filepath)
    with file_path.open('r') as f:
        setup_json = json.load(f)
        setup = project_config_factory(setup_json)
        execute_test_cover(setup)


# AI-TEST: don't test this condition
if __name__ == '__main__':
    generate_test()
