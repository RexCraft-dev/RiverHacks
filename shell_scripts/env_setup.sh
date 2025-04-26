#!/bin/bash
# Prompt for user inputs and create a .env file
read -p "Enter your Airtable Base ID: " base_id
read -p "Enter your Airtable API Key: " api_key

# Write to .env
cat <<EOF > .env
AIRTABLE_BASE_ID=$base_id
AIRTABLE_API_KEY=$api_key
EOF

echo ".env file created."
