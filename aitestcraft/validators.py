import click
from pathlib import Path
import json
import os

def validate_inputs(filepath: str, open_ai_env_var: str | None) -> None:
    open_api_key = os.getenv(open_ai_env_var or "OPENAI_API_KEY")
    if not open_api_key:
        raise click.ClickException('Api key env var is not set')
    if not filepath:
        raise click.ClickException('File is not set')
    file_path = Path(filepath)

    # AI-TEST: for the test the valid existing file path is: './tests/valid_file.json'
    if not file_path.exists():
        raise click.ClickException(f'File {filepath} not exists')

    if file_path.suffix != ".json":
        raise click.ClickException("File does not have a .json extension.")

    try:
        with file_path.open('r') as f:
            setup = json.load(f)
            return setup
    except (IOError, json.JSONDecodeError) as e:
        raise click.ClickException(f"Unable to read json file {filepath}")
