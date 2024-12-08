# UK NOTAMs Repository

This repository is used to track and store UK NOTAM information, particularly focusing on Temporary Restricted Areas.

## Structure

- `/notams`: Directory containing NOTAM XML files
- `/scripts`: Helper scripts for processing NOTAMs
- `/tra`: Extracted information about Temporary Restricted Areas

## How to Update NOTAMs

1. Download the latest PIB.xml from https://pibs.nats.co.uk
2. Save it in the `/notams` directory with the date (e.g., `notams/2024-12-08.xml`)
3. Update the TRA information in the `/tra` directory

## Latest Update

Last updated: 2024-12-08