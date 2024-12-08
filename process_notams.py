from scripts.notam_processor import UKNotamProcessor
import xml.etree.ElementTree as ET
import os

def main():
    # Initialize processor
    processor = UKNotamProcessor()
    
    # Process the latest XML file
    xml_file = "raw/NOTAM_20241208.xml"
    
    try:
        # Parse XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Extract metadata
        processor.extract_pib_metadata(root)
        
        # Extract aerodrome information
        processor.extract_aerodromes(root)
        
        # Process NOTAMs
        processor.process_notams(root)
        
        # Save processed data
        processor.save_processed_data('processed')
        
        print("NOTAM processing completed successfully!")
        
    except Exception as e:
        print(f"Error processing NOTAMs: {str(e)}")

if __name__ == "__main__":
    main()