import unittest
from unittest.mock import MagicMock
from pathlib import Path
import json
import click
import os
from unittest.mock import mock_open, patch, MagicMock

# Import the code to be tested
from aitestgen.validators import validate_inputs


class TestValidators(unittest.TestCase):

    def test_validate_inputs_valid_file(self):
        # Test case 1: Valid file path provided
        file_path = "./tests/valid_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        result = validate_inputs(file_path, open_ai_env_var)
        self.assertIsNotNone(result)

    def test_validate_inputs_invalid_file(self):
        # Test case 2: Invalid file path provided
        file_path = "./tests/nonexistent_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), f"File {file_path} not exists")

    @patch('os.getenv', return_value="yolo")
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

    def test_validate_inputs_missing_file(self):
        # Test case 5: Missing file path
        file_path = ""
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), "File is not set")

    def test_validate_inputs_invalid_json(self):
        # Test case 6: Invalid JSON file
        file_path = "./tests/invalid_json_file.json"
        open_ai_env_var = "OPENAI_API_KEY"
        with self.assertRaises(click.ClickException) as context:
            validate_inputs(file_path, open_ai_env_var)
        self.assertEqual(str(context.exception), f"Unable to read json file {file_path}")
