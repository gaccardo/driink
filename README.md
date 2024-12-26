# Driink

UNDER DEVELOPMENT - DO NOT USE

## Build

rm -rf build dist ; poetry build
pip install dist/*.whl

python3 -m twine upload dist/*

## OS Dependencies
Before installing this project, ensure the following packages are installed:
- `libnotify-bin` (for notifications)
- `libappindicator3-dev` (for AppIndicator)
- `python-gi-dev`
- `ligghc-cairo-dev`
- `gobject-introspection`
- `libgirepository-2.0-dev`
- `libgirepository-1.0-dev`
- `gir1.2-appindicator3-0.1`
