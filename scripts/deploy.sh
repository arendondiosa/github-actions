#!/bin/bash
cd github-actions
git config --global user.email "alejandro@rendon.co"
git config --global user.name "Test Commit"
git add .
git commit -m 'Update pylint score' --allow-empty
git push origin master