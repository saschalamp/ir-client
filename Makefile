POETRY := poetry run

init:
	poetry install

test:
	$(POETRY) pytest tests --junitxml=.build/reports/test-report.xml

it:
	$(POETRY) pytest integrationtests --junitxml=.build/reports/it-report.xml
