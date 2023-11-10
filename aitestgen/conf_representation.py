from dataclasses import dataclass
from typing import Optional, List


# Define a dataclass for the nested 'files' array objects
@dataclass
class File:
    code: str
    test: str


# Define a dataclass for the main JSON object
@dataclass
class ProjectConfig:
    # mandatory
    language: str
    model: str
    files: List[File]

    # optional
    framework: Optional[str] = None
    test_framework: Optional[str] = None
    package_file: Optional[str] = None
    additional_comments: Optional[List[str]] = None
