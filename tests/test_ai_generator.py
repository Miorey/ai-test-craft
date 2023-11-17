import unittest
from unittest.mock import patch, MagicMock, mock_open
from aitestcraft.ai_generator import open_ai_client
from aitestcraft.conf_representation import ProjectConfig, File, Overwrite
from halo import Halo
from pathlib import Path
import os

# Import the code to be tested
from aitestcraft.ai_generator import setup_open_ai_client, execute_test_cover


class TestAiGenerator(unittest.TestCase):

    @patch('os.getenv', return_value="test_api_key")
    def test_setup_open_ai_client(self, mock_getenv):
        # Test case: API key environment variable set
        open_ai_env_var = "OPENAI_API_KEY"
        setup_open_ai_client(open_ai_env_var)
        self.assertEqual(open_ai_client.api_key, "test_api_key")

    @patch('os.getenv', return_value=None)
    def test_setup_open_ai_client_missing_api_key(self, mock_getenv):
        # Test case: Missing API key environment variable
        open_ai_env_var = "OPENAI_API_KEY"
        setup_open_ai_client(open_ai_env_var)
        self.assertIsNone(open_ai_client.api_key)

    @patch('aitestcraft.ai_generator.open_ai_client.chat.completions.create')
    def test_execute_test_cover_existing_test(self, mock_create):
        # Test case 1: Existing test file and overwrite set to NEVER
        gen_setup = MagicMock()
        gen_setup.files = [
            File(code="test_code.py", test="test_code_test.py")
        ]
        gen_setup.language = "python"
        gen_setup.language_version = None
        gen_setup.additional_comments = None
        gen_setup.overwrite = Overwrite.NEVER

        # Mock the file existence check
        patch('pathlib.Path.is_file', return_value=True)
        
        with patch('builtins.open', mock_open(read_data='mock file content')) as m_open:
            with patch('builtins.openai', create=True):
                execute_test_cover(gen_setup)
        
        m_open.assert_called_with("test_code_test.py", 'w')

    @patch('aitestcraft.ai_generator.open_ai_client.chat.completions.create')
    def test_execute_test_cover_new_test(self, mock_create):
        # Test case 2: New test file and overwrite set to NEVER
        gen_setup = MagicMock()
        gen_setup.files = [
            MagicMock(code="test_code.py", test="test_code_test.py")
        ]
        gen_setup.language = "python"
        gen_setup.language_version = None
        gen_setup.additional_comments = None
        gen_setup.overwrite = MagicMock(return_value="never")

        # Mock the file existence check
        patch('pathlib.Path.is_file', return_value=False)

        with patch('builtins.open', mock_open(read_data='mock file content')) as m_open:
            with patch('builtins.openai', create=True):
                execute_test_cover(gen_setup)

        m_open.assert_called_with("test_code_test.py", 'w')

    @patch('aitestcraft.ai_generator.open_ai_client.chat.completions.create')
    def test_execute_test_cover_new_test_overwrite_always(self, mock_create):
        # Test case 3: New test file and overwrite set to ALWAYS
        gen_setup = MagicMock()
        gen_setup.files = [
            MagicMock(code="test_code.py", test="test_code_test.py")
        ]
        gen_setup.language = "python"
        gen_setup.language_version = None
        gen_setup.additional_comments = None
        gen_setup.overwrite = MagicMock(return_value="always")
        
        with patch('builtins.open', mock_open(read_data='mock file content')) as m_open:
            with patch('builtins.openai', create=True):
                execute_test_cover(gen_setup)
        mock_create.assert_called_once()

    @patch('aitestcraft.ai_generator.open_ai_client.chat.completions.create')
    def test_execute_test_cover_additional_comments(self, mock_create):
        # Test case 4: Additional comments included in chat conversation
        gen_setup = MagicMock()
        gen_setup.files = [
            MagicMock(code="test_code.py", test="test_code_test.py")
        ]
        gen_setup.language = "python"
        gen_setup.language_version = None
        gen_setup.additional_comments = ["Additional Comment 1", "Additional Comment 2"]
        gen_setup.overwrite = MagicMock(return_value="always")

        with patch('builtins.open', mock_open(read_data='mock file content')) as m_open:
            with patch('builtins.openai', create=True):
                execute_test_cover(gen_setup)
        
        mock_create.assert_called_once()