# Documentation (Sphinx)

# 1. Dependencies

# 1.1. Sphinx Basic HTML / RTD Theme
 
```bash
# install dependencies
apt-get install python3-sphinx python3-sphinx-rtd-theme
```

# 1.2. PDF / Latex

```bash
# install texlive
apt-get install texlive-full
```

# 2. Build

# 2.1. HTML Documentation

```bash
# build html doc
make html
cd ./build/html/
```

# 2.2. PDF / Latex

```bash
# build pdf doc
make latexpdf
cd ./build/latex/
```
