#!/bin/sh
deployment_package=discord_interactions_package.zip

rm -f $deployment_package
cd .venv/lib/python3.8/site-packages
zip -r ../../../../$deployment_package .
cd ../../../../discord_interactions
zip -g ../$deployment_package *.py
cd ..
echo "Deploying to AWS..."
aws lambda update-function-code --function-name abc_discord_interactions --region us-west-2 --zip-file fileb://$deployment_package
rm $deployment_package