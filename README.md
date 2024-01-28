# Cow says moo?

Maybe not... A game created during CCJ 2024!

## Adding more animals

TODO: add docs (animals.json + assets)

## Installing

TODO: from release page to running it

## Install from scratch

Pre conditions:
* repository is cloned
* a python environment configured with the requirements.txt

### Linux
```
pyinstaller --onefile main.py
cp -R assets/ dist/assets/
tar -zcvf cowsays.tar.gz dist/
```
### Windows
```
pyinstaller --noconsole --onefile main.py
# copy assets over to dist/assets/
# zip it
```

