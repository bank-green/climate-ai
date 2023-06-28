init-frontend:
	npm install -C frontend

init-backend:
	virtualenv backend/venv
	. backend/venv/bin/activate
	pip install -r backend/requirements.txt

init:
	make init-backend & make init-frontend

run-frontend:
	npx nuxi dev frontend

run-backend:
	. backend/venv/bin/activate
	python backend/api.py

run:
	make run-backend & make run-frontend