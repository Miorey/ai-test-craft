
import os
import openai
import click
import json
from pathlib import Path
import pytest
from unittest import mock
from aitestgen import (
     generate_test,
     validate_inputs,
     execute_test_cover,
)


@pytest.fixture
def setup():
    return {
        'language': 'python',
        'files': [
            {
                'code': 'tests/test_code.py',
                'test': 'tests/test_code_test.py'
            }
        ],
        'additional-comments': []
    }


def test_validate_inputs_with_valid_file(setup):
    filepath = 'valid_file.json'
    open_ai_env_var = 'OPENAI_API_KEY'

    result = validate_inputs(filepath, open_ai_env_var)

    assert result == setup


def test_validate_inputs_with_missing_file(setup):
    filepath = 'missing_file.json'
    open_ai_env_var = 'OPENAI_API_KEY'

    with pytest.raises(click.ClickException) as excinfo:
        validate_inputs(filepath, open_ai_env_var)

    assert str(excinfo.value) == f'File {filepath} not exists'


def test_validate_inputs_with_invalid_file_extension(setup):
    filepath = 'invalid_file.txt'
    open_ai_env_var = 'OPENAI_API_KEY'

    with pytest.raises(click.ClickException) as excinfo:
        validate_inputs(filepath, open_ai_env_var)

    assert str(excinfo.value) == 'File does not have a .json extension.'


def test_execute_test_cover(mock_open, setup):
    setup_data = {
        'language': 'python',
        'files': [
            {
                'code': 'tests/test_code.py',
                'test': 'tests/test_code_test.py'
            }
        ],
        'additional-comments': []
    }
    gen_setup = setup_data

    expected_message = """
    import os
    import openai
    import click
    import json
    from pathlib import Path

    @click.command()
    @click.argument('filepath', type=click.Path(exists=True))
    @click.option('--open-ai-env-var', required=False)
    def generate_test(filepath: str, open_ai_env_var: str | None):
        ...

    def validate_inputs(filepath: str, open_ai_env_var: str | None) -> dict:
        ...

    def execute_test_cover(gen_setup: dict[str, str | list[dict[str, str]]]):
        ...

    if __name__ == '__main__':
        generate_test()
    """

    completion = {
        "choices": [{
            "message": {
                "content": expected_message
            }
        }]
    }

    openai_mock = mock.Mock()
    openai_mock.ChatCompletion.create.return_value = completion

    open_mock = mock.mock_open()

    with mock.patch.object(openai, "api_key", "KEY"), \
            mock.patch.object(openai, "ChatCompletion", openai_mock), \
            mock.patch('builtins.open', open_mock), \
            mock.patch('openai.api_key', 'KEY'):

        execute_test_cover(gen_setup)

    open_mock.assert_called_with('tests/test_code_test.py', 'w')
    handle = open_mock()
    handle.write.assert_called_with(expected_message)


def test_generate_test_no_exception(setup):
    filepath = 'valid_file.json'
    open_ai_env_var = 'OPENAI_API_KEY'

    with mock.patch.object(click, 'command', create=True), \
            mock.patch.object(click, 'argument', create=True), \
            mock.patch.object(click, 'option', create=True), \
            mock.patch('openai.api_key', 'KEY'), \
            mock.patch('builtins.open'), \
            mock.patch.object(openai, 'api_key', 'KEY'), \
            mock.patch.object(validate_inputs, 'return_value', setup):

        generate_test(filepath, open_ai_env_var)


def test_generate_test_missing_api_key(setup):
    filepath = 'valid_file.json'
    open_ai_env_var = 'OPENAI_API_KEY'

    with mock.patch.object(click, 'command', create=True), \
            mock.patch.object(click, 'argument', create=True), \
            mock.patch.object(click, 'option', create=True), \
            mock.patch('openai.api_key', ''), \
            mock.patch('builtins.open'), \
            mock.patch.object(openai, 'api_key', 'KEY'), \
            mock.patch.object(validate_inputs, 'return_value', setup):

        with pytest.raises(click.ClickException) as excinfo:
            generate_test(filepath, open_ai_env_var)

        assert str(excinfo.value) == 'Api key env var is not set'


def test_generate_test_missing_file(setup):
    filepath = ''
    open_ai_env_var = 'OPENAI_API_KEY'

    with mock.patch.object(click, 'command', create=True), \
            mock.patch.object(click, 'argument', create=True), \
            mock.patch.object(click, 'option', create=True), \
            mock.patch('openai.api_key', 'KEY'), \
            mock.patch('builtins.open'), \
            mock.patch.object(openai, 'api_key', 'KEY'), \
            mock.patch.object(validate_inputs, 'return_value', setup):

        with pytest.raises(click.ClickException) as excinfo:
            generate_test(filepath, open_ai_env_var)

        assert str(excinfo.value) == 'File is not set'


def test_generate_test_execute_test_cover(setup):
    filepath = 'valid_file.json'
    open_ai_env_var = 'OPENAI_API_KEY'

    with mock.patch.object(click, 'command', create=True), \
            mock.patch.object(click, 'argument', create=True), \
            mock.patch.object(click, 'option', create=True), \
            mock.patch('openai.api_key', 'KEY'), \
            mock.patch('builtins.open'), \
            mock.patch.object(openai, 'api_key', 'KEY'), \
            mock.patch.object(execute_test_cover, 'return_value', None):

        generate_test(filepath, open_ai_env_var)


def test_execute_test_coverage_no_additional_comments(mock_open, setup):
    setup_data = {
        'language': 'python',
        'files': [
            {
                'code': 'tests/test_code.py',
                'test': 'tests/test_code_test.py'
            }
        ],
        'additional-comments': []
    }
    gen_setup = setup_data

    expected_message = """
    import os
    import openai
    import click
    import json
    from pathlib import Path

    @click.command()
    @click.argument('filepath', type=click.Path(exists=True))
    @click.option('--open-ai-env-var', required=False)
    def generate_test(filepath: str, open_ai_env_var: str | None):
        ...

    def validate_inputs(filepath: str, open_ai_env_var: str | None) -> dict:
        ...

    def execute_test_cover(gen_setup: dict[str, str | list[dict[str, str]]]):
        ...

    if __name__ == '__main__':
        generate_test()
    """

    completion = {
        "choices": [{
            "message": {
                "content": expected_message
            }
        }]
    }

    openai_mock = mock.Mock()
    openai_mock.ChatCompletion.create.return_value = completion

    open_mock = mock.mock_open()

    with mock.patch.object(openai, "api_key", "KEY"), \
            mock.patch.object(openai, "ChatCompletion", openai_mock), \
            mock.patch('builtins.open', open_mock), \
            mock.patch('openai.api_key', 'KEY'):

        execute_test_cover(gen_setup)

    open_mock.assert_called_with('tests/test_code_test.py', 'w')
    handle = open_mock()
    handle.write.assert_called_with(expected_message)
    openai_mock.ChatCompletion.create.assert_called_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fpython developer"},
            {
                "role": "user", "content": """
                Write the unit test of the following code. 
                The test should follow those rules:
                 - THE TEST SHOULD COVER 100% of the code.
                 - In the imports take in account that the test is in tests/test_code.py and the test in tests/test_code_test.py.
                 - The comments starting with `AI-TEST:` take them in consideration. 
                 
                Your answer should contain:
                 - NO SYNTAX HIGHLIGHTING.
                 - no introduction or explanation.
                 - ALL the test should be in the same snippet.
                
                    import os
                    import openai
                    import click
                    import json
                    from pathlib import Path

                    @click.command()
                    @click.argument('filepath', type=click.Path(exists=True))
                    @click.option('--open-ai-env-var', required=False)
                    def generate_test(filepath: str, open_ai_env_var: str | None):
                        ...

                    def validate_inputs(filepath: str, open_ai_env_var: str | None) -> dict:
                        ...

                    def execute_test_cover(gen_setup: dict[str, str | list[dict[str, str]]]):
                        ...

                    if __name__ == '__main__':
                        generate_test()
                
                """
            }
        ]
    )


def test_execute_test_coverage_with_additional_comments(mock_open, setup):
    setup_data = {
        'language': 'python',
        'files': [
            {
                'code': 'tests/test_code.py',
                'test': 'tests/test_code_test.py'
            }
        ],
        'additional-comments': ['Add some assertions', 'Check for edge cases']
    }
    gen_setup = setup_data

    expected_message = """
    import os
    import openai
    import click
    import json
    from pathlib import Path

    @click.command()
    @click.argument('filepath', type=click.Path(exists=True))
    @click.option('--open-ai-env-var', required=False)
    def generate_test(filepath: str, open_ai_env_var: str | None):
        ...

    def validate_inputs(filepath: str, open_ai_env_var: str | None) -> dict:
        ...

    def execute_test_cover(gen_setup: dict[str, str | list[dict[str, str]]]):
        ...

    if __name__ == '__main__':
        generate_test()
    """

    completion = {
        "choices": [{
            "message": {
                "content": expected_message
            }
        }]
    }

    openai_mock = mock.Mock()
    openai_mock.ChatCompletion.create.return_value = completion

    open_mock = mock.mock_open()

    with mock.patch.object(openai, "api_key", "KEY"), \
            mock.patch.object(openai, "ChatCompletion", openai_mock), \
            mock.patch('builtins.open', open_mock), \
            mock.patch('openai.api_key', 'KEY'):

        execute_test_cover(gen_setup)

    open_mock.assert_called_with('tests/test_code_test.py', 'w')
    handle = open_mock()
    handle.write.assert_called_with(expected_message)
    openai_mock.ChatCompletion.create.assert_called_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fpython developer"},
            {
                "role": "user", "content": """
                Write the unit test of the following code. 
                The test should follow those rules:
                 - THE TEST SHOULD COVER 100% of the code.
                 - In the imports take in account that the test is in tests/test_code.py and the test in tests/test_code_test.py.
                 - The comments starting with `AI-TEST:` take them in consideration. 
                 - Add some assertions
                 - Check for edge cases
                 
                Your answer should contain:
                 - NO SYNTAX HIGHLIGHTING.
                 - no introduction or explanation.
                 - ALL the test should be in the same snippet.
                
                    import os
                    import openai
                    import click
                    import json
                    from pathlib import Path

                    @click.command()
                    @click.argument('filepath', type=click.Path(exists=True))
                    @click.option('--open-ai-env-var', required=False)
                    def generate_test(filepath: str, open_ai_env_var: str | None):
                        ...

                    def validate_inputs(filepath: str, open_ai_env_var: str | None) -> dict:
                        ...

                    def execute_test_cover(gen_setup: dict[str, str | list[dict[str, str]]]):
                        ...

                    if __name__ == '__main__':
                        generate_test()
                
                """
            }
        ]
    )

