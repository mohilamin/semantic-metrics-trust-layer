install:
	pip install -r requirements.txt

generate-data:
	python -m src.data_generation.generate_enterprise_data

run-pipeline:
	python -m src.pipeline.run_all

calculate-metrics:
	python -m src.metrics_engine.calculator

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --reload

docker-up:
	docker compose up --build

docker-down:
	docker compose down
