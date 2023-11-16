from dataclasses import dataclass
from typing import Optional, List
from copy import deepcopy
from enum import Enum


class Overwrite(Enum):
    ALWAYS = "always"
    NEVER = "never"

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
    overwrite: Overwrite = Overwrite.NEVER

    # optional
    framework: Optional[str] = None
    language_version: Optional[str] = None
    test_framework: Optional[str] = None
    package_file: Optional[str] = None
    additional_comments: Optional[List[str]] = None


def project_config_factory(input_dict: dict) -> ProjectConfig:
    dict_copy = deepcopy(input_dict)
    dict_copy["files"] = [File(**file) for file in input_dict["files"]]
    if input_dict.get("overwrite"):
        dict_copy["overwrite"] = Overwrite(input_dict["overwrite"])
    return ProjectConfig(**dict_copy)

