all: compile run
	echo Done

compile:
	nuitka --recurse-all --show-progress main.py

run:
	./main.exe