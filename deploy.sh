#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Add changes to git.
git add --all

# Commit changes.
msg="rebuilding site `date`"
echo "Enter the commit message"
read msg

git commit -m "$msg"

# Push source and build repos.
git push -u origin master
