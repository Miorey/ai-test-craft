
import os
import openai
import click
import json
from pathlib import Path
import pytest

from aitestgen import generate_test, execute_test_cover


@pytest.fixture
def setup_file(tmp_path):
    # Create a temporary JSON setup file
    setup_data = {
        "language": "python",
        "files": [
            {
                "code": str(tmp_path / "test_code.py"),
                "test": str(tmp_path / "test_code_test.py")
            }
        ]
    }

    with open(tmp_path / "setup.json", 'w') as f:
        json.dump(setup_data, f)

    yield str(tmp_path / "setup.json")


def test_generate_test(setup_file, monkeypatch):
    # Mock the environment variable used in the code
    monkeypatch.setenv("OPENAI_API_KEY", "test_api_key")

    # Generate the test file
    generate_test(setup_file)

    # Check that the test file was created
    assert Path(setup_file).parent.joinpath("test_code_test.py").is_file()


def test_execute_test_cover(tmp_path, monkeypatch):
    # Mock the chat completion API call
    def mock_chat_completion_create(*args, **kwargs):
        return {
            "choices": [
                {
                    "message": {
                        "content": """
                            import os
                            import openai
                            import click
                            import json
                            from pathlib import Path

                            def test_code():
                                assert True
                        """
                    }
                }
            ]
        }

    monkeypatch.setattr(openai.ChatCompletion, "create", mock_chat_completion_create)

    # Create the test setup data
    setup_data = {
        "language": "python",
        "files": [
            {
                "code": str(tmp_path / "test_code.py"),
                "test": str(tmp_path / "test_code_test.py")
            }
        ]
    }

    # Create the code file
    code_content = """
        import os
        import openai
        import click
        import json
        from pathlib import Path
    """
    with open(tmp_path / "test_code.py", 'w') as f:
        f.write(code_content)

    # Execute the test cover
    execute_test_cover(setup_data)

    # Check that the test file was created and has the expected content
    test_file = tmp_path.joinpath("test_code_test.py")
    assert test_file.is_file()
    with open(test_file, 'r') as f:
        test_content = f.read()
        assert "def test_code():" in test_content
        assert "assert True" in test_content


