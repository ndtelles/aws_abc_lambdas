#!/bin/sh
deployment_package=discord_bot_package.zip

rm -f $deployment_package
cd ./discord_bot
zip ../$deployment_package *.py
cd ..
echo "Deploying to AWS..."
aws lambda update-function-code --function-name abc_discord_bot --region us-west-2 --zip-file fileb://$deployment_package
rm $deployment_package