# Utilizamos Python, versão 3.8.10 e 3.10.4
# Também precisa do pip
setup: requirements.txt
	pip install -r requirements.txt

run:
	python3 src/main.py $(FILE)

clean:
	rm -rf __pycache__
