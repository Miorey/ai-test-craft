# AITestCraft

## AITestCraft - Automated Unit Test Generation for Python

AITestCraft is a Python package that assists developers in generating unit tests for their code. It leverages OpenAI's GPT models to create test cases based on the structure and requirements of your codebase.

### Features:

- Automated generation of unit tests from JSON configuration.
- Support for Python 3.11 and other versions.
- Customizable to prevent overwriting existing test files.
- Allows for additional comments to guide test case creation.
- Sequential file processing for context-aware test generation.

### Prerequisites:

To use AITestCraft, you need an OpenAI API key. To obtain it, follow these steps:

1. Sign up for an account at [OpenAI](https://openai.com).
2. Navigate to the API section and follow the instructions to generate your API key.

### Installation:

Install AITestCraft using pip:

```bash
pip install aitestcraft
```

### Usage:

To generate unit tests, create a JSON configuration file named `to-test.json`:

```json
{
  "language": "python",
  "language_version": "3.11",
  "model": "gpt-3.5-turbo",
  "overwrite": "never",
  "additional_comments": [
    "Use functions for each testcase and not unittest.TestCase"
  ],
  "files": [
    {
      "code": "aitestcraft/conf_representation.py",
      "test": "tests/test_conf_representation.py"
    },
    {
      "code": "aitestcraft/validators.py",
      "test": "tests/test_validators.py"
    },
    {
      "code": "aitestcraft/ai_generator.py",
      "test": "tests/test_ai_generator.py"
    }
  ]
}
```

Then run the package with:

```bash
aitestcraft to-test.json
```

### Configuration Fields:

- `language`: Programming language used.
- `language_version`: Version of the programming language.
- `model`: OpenAI model used for generating tests.
- `overwrite`: If set to "never", existing test files will not be overwritten.
- `additional_comments`: Optional, global comments for test generation.
- `files`: A list of objects representing the source code and the test files.

In the `files`, if a comment starts with `AI-TEST`, it indicates a message for the AI to include specific demands for the next line, like so:

```python
# AI-TEST: don't test this condition
```

### Note:

The generated tests may require minor adjustments to fit the exact needs of your project.

Order the files in `to-test.json` from the most standalone files to those with the most dependencies. This helps to provide context that can improve the quality of the generated tests.

### Disclaimer:

The test generation is not guaranteed to be perfect and might need adjustments to work seamlessly with your codebase.

Happy Testing with AITestCraft!
