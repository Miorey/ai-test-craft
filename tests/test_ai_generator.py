import unittest
from unittest.mock import patch, MagicMock, mock_open
from aitestcraft.conf_representation import File, Overwrite

# Import the code to be tested
from aitestcraft.ai_generator import execute_test_cover


class TestAiGenerator(unittest.TestCase):

    def test_execute_test_cover_existing_test(self):
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
                execute_test_cover(gen_setup, MagicMock())
        
        m_open.assert_called_with("test_code_test.py", 'w')

    def test_execute_test_cover_new_test(self):
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
                execute_test_cover(gen_setup, MagicMock())

        m_open.assert_called_with("test_code_test.py", 'w')

    def test_execute_test_cover_new_test_overwrite_always(self):
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
                execute_test_cover(gen_setup, MagicMock())
        m_open.assert_called_with("test_code_test.py", 'w')

    def test_execute_test_cover_additional_comments(self):
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
                execute_test_cover(gen_setup, MagicMock())
        
        m_open.assert_called_with("test_code_test.py", 'w')