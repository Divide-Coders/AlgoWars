FROM texlive/texlive:latest

RUN tlmgr update --self && \
    tlmgr install xcolor setspace titlesec tocloft lipsum microtype hyperref etex listings parskip babel

WORKDIR /docs

COPY . /docs

CMD ["latexmk", "-pdflatex", "-interaction=nonstopmode", "main.tex"]