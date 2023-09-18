pip install -t ./lib -r requirements.txt 
cd lib
zip ../lambda_function.zip ./*
cd ..
zip lambda_function.zip -u main.py 
zip lambda_function.zip -u __init__.py
zip lambda_function.zip -ur src
zip lambda_function.zip -ur routes
