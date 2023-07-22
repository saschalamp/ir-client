POETRY := poetry run

init:
	poetry install --no-interaction

release:
	poetry version $(tag)
	git add .
	git commit -m "Prepare release version $(tag)"
	git push origin main
	poetry publish
	poetry version patch
	git add .
	git commit -m "Prepare for next iteration"
	git push origin main

test:
	$(POETRY) pytest tests --junitxml=.build/reports/test-report.xml

it:
	$(POETRY) pytest integration --junitxml=.build/reports/it-report.xml
