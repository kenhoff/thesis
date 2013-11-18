all:
	python create_latex.py 
	python generate_surveytex.py
	pdflatex KenHoffThesis.tex	

final: all
	pdflatex KenHoffThesis.tex

clean:
	rm *.pyc *.aux *.dvi *.pdf *.log *.toc