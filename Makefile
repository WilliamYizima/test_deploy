install:
	pip install -r requirements.txt
run:
	uvicorn --proxy-headers  src.main.app:app --host 0.0.0.0 --port 9002
run-dev:
	uvicorn --proxy-headers  src.app:app --host 0.0.0.0 --port 9002 --reload

