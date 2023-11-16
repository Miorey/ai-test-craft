import unittest
from unittest.mock import MagicMock
from typing import List, Dict

# Import the code to be tested
from aitestgen.conf_representation import File, ProjectConfig, Overwrite, project_config_factory


class TestConfRepresentation(unittest.TestCase):

    def test_project_config_factory(self):
        # Test case 1: Input dictionary contains all mandatory fields
        input_dict1 = {
            "language": "Python",
            "model": "Test Model",
            "files": [
                {"code": "code1", "test": "test1"},
                {"code": "code2", "test": "test2"}
            ]
        }
        expected_output1 = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[
                File(code="code1", test="test1"),
                File(code="code2", test="test2")
            ],
            overwrite=Overwrite.NEVER
        )
        self.assertEqual(project_config_factory(input_dict1), expected_output1)

        # Test case 2: Input dictionary contains optional fields
        input_dict2 = {
            "language": "Python",
            "model": "Test Model",
            "files": [
                {"code": "code1", "test": "test1"},
                {"code": "code2", "test": "test2"}
            ],
            "framework": "Test Framework",
            "language_version": "3.7",
            "test_framework": "Test Test Framework",
            "package_file": "Test Package File",
            "additional_comments": ["Comment 1", "Comment 2"]
        }
        expected_output2 = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[
                File(code="code1", test="test1"),
                File(code="code2", test="test2")
            ],
            overwrite=Overwrite.NEVER,
            framework="Test Framework",
            language_version="3.7",
            test_framework="Test Test Framework",
            package_file="Test Package File",
            additional_comments=["Comment 1", "Comment 2"]
        )
        self.assertEqual(project_config_factory(input_dict2), expected_output2)

        # Test case 3: Input dictionary with overwrite="always"
        input_dict3 = {
            "language": "Python",
            "model": "Test Model",
            "files": [
                {"code": "code1", "test": "test1"},
                {"code": "code2", "test": "test2"}
            ],
            "overwrite": "always"
        }
        expected_output3 = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[
                File(code="code1", test="test1"),
                File(code="code2", test="test2")
            ],
            overwrite=Overwrite.ALWAYS
        )
        self.assertEqual(project_config_factory(input_dict3), expected_output3)

    def test_project_config_files(self):
        # Test case 1: ProjectConfig object with empty files list
        project_config = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[],
            overwrite=Overwrite.ALWAYS
        )
        self.assertListEqual(project_config.files, [])

        # Test case 2: ProjectConfig object with files list containing File objects
        file1 = File(code="code1", test="test1")
        file2 = File(code="code2", test="test2")
        project_config = ProjectConfig(
            language="Python",
            model="Test Model",
            files=[file1, file2],
            overwrite=Overwrite.ALWAYS
        )
        self.assertListEqual(project_config.files, [file1, file2])
