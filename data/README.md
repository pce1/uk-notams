# NOTAM Data Structure

This directory contains processed NOTAM data in the following structure:

## Categories

- `tra_notams.json`: Temporary Restricted Areas
- `danger_notams.json`: Danger Areas
- `restricted_notams.json`: Other Restricted Areas
- `other_notams.json`: Other NOTAMs

## File Format

Each JSON file contains an array of NOTAM objects with the following structure:

```json
{
  "id": "NOTAM ID",
  "type": "NOTAM Type",
  "category": "Category (TRA/DANGER/etc)",
  "text": "Full NOTAM text",
  "start_time": "Start time in format YYMMDDHHMM",
  "end_time": "End time in format YYMMDDHHMM"
}
```

## Usage

1. Place new XML files in the `raw` directory
2. Run the parsing script
3. Check the processed files in this directory