import unittest
from unittest.mock import MagicMock, patch
from aitestgen.conf_representation import ProjectConfig, Overwrite, File
from aitestgen.ai_generator import setup_open_ai_client, execute_test_cover
import os


class TestAIGenerator(unittest.TestCase):

    def test_setup_open_ai_client(self):
        # Test case 1: OPENAI_API_KEY environment variable set
        open_ai_env_var = "OPENAI_API_KEY"
        setup_open_ai_client(open_ai_env_var)
        self.assertEqual(open_ai_client.api_key, os.getenv(open_ai_env_var))

        # Test case 2: OPENAI_API_KEY environment variable not set, using default
        open_ai_env_var = None
        default_api_key = "DEFAULT_API_KEY"
        os.environ["OPENAI_API_KEY"] = default_api_key
        setup_open_ai_client(open_ai_env_var)
        self.assertEqual(open_ai_client.api_key, default_api_key)

    @patch('openai.OpenAI')
    def test_execute_test_cover_existing_test_file(self, mock_open_ai_client):
        # Test case 3: Test file exists and overwrite mode is NEVER
        gen_setup = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[File(code="code1.py", test="test1.py")],
            overwrite=Overwrite.NEVER
        )
        gen_setup.additional_comments = []
        execute_test_cover(gen_setup)
        self.assertFalse(mock_open_ai_client.chat.completions.create.called)

    @patch('openai.OpenAI')
    @patch('builtins.open')
    def test_execute_test_cover_nonexistent_test_file(self, mock_open, mock_open_ai_client):
        # Test case 4: Test file does not exist and overwrite mode is NEVER
        gen_setup = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[File(code="code1.py", test="test1.py")],
            overwrite=Overwrite.NEVER
        )
        gen_setup.additional_comments = []
        mock_exists = MagicMock(return_value=False)
        with patch('pathlib.Path.exists', mock_exists):
            execute_test_cover(gen_setup)
        self.assertFalse(mock_open_ai_client.chat.completions.create.called)

    @patch('openai.OpenAI')
    @patch('builtins.open')
    def test_execute_test_cover_overwrite_always(self, mock_open, mock_open_ai_client):
        # Test case 5: Test file exists and overwrite mode is ALWAYS
        gen_setup = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[File(code="code1.py", test="test1.py")],
            overwrite=Overwrite.ALWAYS
        )
        gen_setup.additional_comments = []
        mock_exists = MagicMock(return_value=True)
        with patch('pathlib.Path.exists', mock_exists):
            execute_test_cover(gen_setup)
        self.assertTrue(mock_open_ai_client.chat.completions.create.called)

    @patch('openai.OpenAI')
    @patch('builtins.open')
    def test_execute_test_cover_with_additional_comments(self, mock_open, mock_open_ai_client):
        # Test case 6: Test file exists and has additional comments
        gen_setup = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[File(code="code1.py", test="test1.py")],
            overwrite=Overwrite.ALWAYS
        )
        gen_setup.additional_comments = ["additional comment 1", "additional comment 2"]
        execute_test_cover(gen_setup)
        self.assertTrue(mock_open_ai_client.chat.completions.create.called)


if __name__ == '__main__':
    unittest.main()
