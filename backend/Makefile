.PHONY: test lint format coverage install

# Install dependencies
install:
	pip install -r requirements.txt
	pip install pytest pytest-django coverage flake8 black isort

# Run tests
test:
	pytest

# Run tests with coverage
coverage:
	coverage run -m pytest
	coverage report
	coverage html

# Check code style
lint:
	flake8 .
	black . --check
	isort . --check-only

# Format code
format:
	black .
	isort .

# Run all quality checks
quality: lint test coverage

# Clean up python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# Run development server
run:
	python manage.py runserver

# Make migrations
migrations:
	python manage.py makemigrations

# Apply migrations
migrate:
	python manage.py migrate