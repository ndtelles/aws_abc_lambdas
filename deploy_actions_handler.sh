#!/bin/sh
deployment_package=actions_handler_package.zip

rm -f $deployment_package
cd ./actions_handler
zip ../$deployment_package *.py
cd ..
echo "Deploying to AWS..."
aws lambda update-function-code --function-name abc_actions_handler --region us-west-2 --zip-file fileb://$deployment_package
rm $deployment_package