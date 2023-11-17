run-test-coverage:
	unset "OPENAI_API_KEY" && coverage run -m pytest
	coverage report --omit="tests/*"