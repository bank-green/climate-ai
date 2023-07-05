SHELL := /bin/bash

init-frontend:
	npm install -C frontend

init-backend:
	python3 -m venv backend/venv
	source backend/venv/bin/activate; \
	pip install -r backend/requirements.txt

init:
	echo "Installing backend requirements…"
	make init-backend
	echo "Installing frontend requirements…"
	make init-frontend
	echo "Done installing!"

run-frontend:
	cd frontend; \
	npx nuxi dev

run-backend:
	source backend/venv/bin/activate; \
	python backend/api.py

run:
	make run-backend & make run-frontend