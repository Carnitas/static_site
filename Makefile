.PHONY: all
all: test quality

.PHONY: test
test:
	poetry run coverage run --module pytest --random-order
	poetry run coverage report

.PHONY: test-ordered
test-ordered:
	poetry run coverage run --module pytest
	poetry run coverage report

.PHONY: quality
quality:
	poetry run pre-commit run --all-files
