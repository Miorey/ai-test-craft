import os
import openai
import click
import json
from pathlib import Path

# AI-TEST: import the necessary modules for testing
import pytest
from unittest.mock import patch, mock_open

# AI-TEST: import the function to be tested
from aitestgen import validate_inputs, execute_test_cover


# AI-TEST: define the test cases
def test_validate_inputs_valid_file():
    filepath = './tests/valid_file.json'
    openai_env_var = None

    result = validate_inputs(filepath, openai_env_var)

    assert isinstance(result, dict)


def test_validate_inputs_invalid_file():
    filepath = './tests/non_existent_file.json'
    openai_env_var = None

    with pytest.raises(click.ClickException):
        validate_inputs(filepath, openai_env_var)


def test_validate_inputs_non_json_file():
    filepath = './tests/non_json_file.txt'
    openai_env_var = None

    with pytest.raises(click.ClickException):
        validate_inputs(filepath, openai_env_var)


# AI-TEST: mock the openai.api_key assignment and file read operation
def test_execute_test_cover():
    gen_setup = {
        "language": "python",
        "files": [{
            "code": "./tests/test_code.py",
            "test": "./tests/test_aitestgen.py"
        }],
        "additional-comments": ["This is an additional comment."]
    }

    with patch('openai.api_key', 'mock_key'), \
            patch('builtins.open', mock_open(read_data='mock file content')) as m_open:
        execute_test_cover(gen_setup)

        m_open.assert_called_with("./tests/test_code.py", 'r')