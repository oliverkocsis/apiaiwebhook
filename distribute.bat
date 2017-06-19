rmdir dist /s /q
python setup.py sdist
pip install wheel
python setup.py bdist_wheel
pip install twine
twine upload dist/*
