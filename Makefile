all:
	latexmk -pdf

clean:
	rm *.aux *.log *.out *.synctex.gz *.pdf