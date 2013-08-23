all:
	python create_latex.py 
	pdflatex KenHoffThesis.tex	
	pdflatex KenHoffThesis.tex

clean:
	rm *.pyc *.aux *.dvi *.pdf