#!/bin/bash

# Package dependencies
pip install -r requirements.txt -t ./src/
# Zip code
cd src
zip -r ../lambda_package.zip .
cd ..
# Deploy to AWS Lambda
aws lambda update-function-code --function-name my-ai-assistant \
    --zip-file file://lambda_package.zip