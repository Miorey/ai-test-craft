import unittest
import click
from unittest.mock import patch

# Import the code to be tested
from aitestcraft.validators import validate_inputs


class TestValidators(unittest.TestCase):

    @patch('os.getenv', return_value="FAKE_KEY")
    def test_validate_inputs_valid_file(self, mock_getenv):
        # Test case 1: Valid file path provided
        file_path = "./tests/valid_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        result = validate_inputs(file_path, open_ai_env_var)
        self.assertIsNotNone(result)

    @patch('os.getenv', return_value="FAKE_KEY")
    def test_validate_inputs_invalid_file(self, mock_getenv):
        # Test case 2: Invalid file path provided
        file_path = "./tests/nonexistent_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), f"File {file_path} not exists")

    @patch('os.getenv', return_value="FAKE_KEY")
    def test_validate_inputs_invalid_extension(self, mock_getenv):
        # Test case 3: File with invalid extension provided
        file_path = "./tests/invalid_file.txt"
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), "File does not have a .json extension.")

    @patch('os.getenv', return_value=None)
    def test_validate_inputs_missing_api_key_var(self, mock_getenv):
        # Test case 4: Missing OPENAI_API_KEY environment variable
        file_path = "./tests/valid_file.json"
        open_ai_env_var = None
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), "Api key env var is not set")

    @patch('os.getenv', return_value="FAKE_KEY")
    def test_validate_inputs_missing_file(self, mock_getenv):
        # Test case 5: Missing file path
        file_path = ""
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), "File is not set")

    @patch('os.getenv', return_value="FAKE_KEY")
    def test_validate_inputs_invalid_json(self, mock_getenv):
        # Test case 6: Invalid JSON file
        file_path = "./tests/invalid_json_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), f"Unable to read json file {file_path}")
