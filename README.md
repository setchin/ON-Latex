# ON-Latex
LaTeX source for Old Norse Grammar

# Compilation
Index and bibliography are included, so it requires multiple compilations.

I strongly recommend using Latexmk, a tool for complex compilations. It should be installed with TeXLive.
```shell
latexmk -xelatex main.tex
```

Otherwise, you will have to manually compile with the following commands:
```shell
xelatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
biber main.tex
texindy -L icelandic -C utf8 main.idx
xelatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
xelatex -synctex=1 -interaction=nonstopmode -file-line-error main.tex
```

# Structure
Three parts are included in the book, grammar (phonology and morphology), syntax and reader.

Source code for each part is separately saved in three folders.

Commands and packages required for this document is in the *include* folder.
