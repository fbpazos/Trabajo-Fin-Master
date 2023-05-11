#!/bin/bash

# Get the current date in the desired format
date=$(date +%d-%m-%Y)

# Create the name of the zip file
zip_name="End of Master's Thesis($date).zip"

# Compress all files except backup.sh into the zip
zip -r "$zip_name" ./ -x "*.zip" -x "backup.sh" -x "/Backups/*"

# Move the zip file to the Backups directory
mkdir -p Backups
mv "$zip_name" Backups/
