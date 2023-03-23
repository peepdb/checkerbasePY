rm -rf dist/
python3 -m nuitka geokekker/__main__.py --follow-imports --onefile --output-dir=dist