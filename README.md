# AI Test Generator

AI Test Generator is a command-line tool written in Python that utilizes OpenAI's models to automatically generate unit tests for your code.

## Usage

To generate tests, provide the tool with a JSON configuration file as follows:

```bash
python aitestgen.py ./to-test.json
```

An OpenAI API key is required for authentication, which should be set as an environment variable named `OPENAI_API_KEY`. If you need to use a different environment variable name, pass it to the command with the `--open-ai-env-var` option:

```bash
python aitestgen.py --open-ai-env-var MY_ENV_VAR_NAME ./to-test.json
```

## Configuration File

The `to-test.json` file should be structured as shown below:

```json
{
  "language": "python10",
  "framework": null,
  "model": "gpt-3.5-turbo",
  "test-framework": null,
  "package-file": null,
  "additional-comments": [
    "Use functions for each testcase"
  ],
  "files": [
    {
      "code": "aitestgen.py",
      "test": "tests/test_aitestgen.py"
    }
  ]
}
```

Currently, only the `language`, `model`, `additional-comments`, and `files` keys are functional. The `files` array should contain objects with the paths of the code to test and the test file.

## Important Notes

- **Iterative Generation**: The generation process might need to be run multiple times to achieve satisfactory results. In tests conducted, a maximum of 70% code coverage has been achieved.
- **AI Guidance**: To direct the AI's attention to specific behaviors in your code, use the `AI-TEST` marker. For example, to mock an OpenAI call:

```python
# AI-TEST: mock the following openai call
```

Include this comment directly above the code segment that requires special attention.

## Limitations

Please note that the current version of AI Test Generator may not achieve full code coverage and could require multiple iterations to generate effective tests. Adjustments and manual reviews might be necessary to tailor the tests to your codebase.

## Feedback

Your feedback is invaluable in improving AI Test Generator. Should you encounter any issues or have suggestions, please file them on the project's issue tracker.
