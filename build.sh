#!/bin/bash
cd "$(dirname "$0")"
rm -f "Akamai-Account-Search.alfredworkflow"
cd "Akamai Account Search.alfredworkflow"
zip -r "../Akamai-Account-Search.alfredworkflow" . -x "*.DS_Store" -x "__pycache__/*"
echo "Built: Akamai-Account-Search.alfredworkflow"
