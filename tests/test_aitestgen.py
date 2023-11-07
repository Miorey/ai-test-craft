import click
from unittest.mock import mock_open, patch, MagicMock
import pytest

import aitestgen


def test_validate_inputs_existing_file():
    with patch('builtins.open', mock_open()):
        setup = aitestgen.validate_inputs('./tests/valid_file.json', None)
    assert setup["model"] == "fake-ai"


# AI-TEST: define the test cases
def test_validate_inputs_valid_file():
    filepath = './tests/valid_file.json'
    openai_env_var = None

    result = aitestgen.validate_inputs(filepath, openai_env_var)

    assert isinstance(result, dict)


def test_validate_inputs_invalid_file():
    filepath = './tests/non_existent_file.json'
    openai_env_var = None

    with pytest.raises(click.ClickException):
        aitestgen.validate_inputs(filepath, openai_env_var)


def test_validate_inputs_non_json_file():
    filepath = './tests/non_json_file.txt'
    openai_env_var = None

    with pytest.raises(click.ClickException):
        aitestgen.validate_inputs(filepath, openai_env_var)


def test_execute_test_cover():
    gen_setup = {
        "language": "python",
        "files": [{
            "code": "./tests/test_code.py",
            "test": "./tests/test_aitestgen.py"
        }],
        "additional-comments": ["This is an additional comment."],
        "model": "ai-fake-model"
    }

    message_magic = MagicMock()
    message_magic.choices[0].message.content = "``` my code ```"

    with patch(
            'openai.api_key', 'mock_key'
    ), patch(
        'aitestgen.client.chat.completions.create', return_value=message_magic
    ), patch(
        'builtins.open', mock_open(read_data='mock file content')
    ) as m_open:
        aitestgen.execute_test_cover(gen_setup)
        m_open.assert_called_with("./tests/test_aitestgen.py", 'w')
