.PHONY: dbpush run test deps docker

deps:
	pip install -r requirements.txt

run:
	python app.py

dbpush:
	python db_push.py

test:
	pytest -s

docker:
	docker build -t flask-api:1.0.0 .