POETRY := poetry run

init:
	poetry install

test:
	$(POETRY) pytest tests --junitxml=.build/reports/test-report.xml

it:
	$(POETRY) pytest integration --junitxml=.build/reports/it-report.xml
