all: *.pdf

*.pdf: *.tex
	latexmk -pdf

*.tex:
	python MakeTEX.py

clean:
	rm *.aux *.log *.out *.synctex.gz *.pdf *.tex *.fdb_latexmk