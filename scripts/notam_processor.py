import xml.etree.ElementTree as ET
import json
from datetime import datetime
import os

class UKNotamProcessor:
    def __init__(self):
        self.categories = {
            'TRA': [],
            'DANGER': [],
            'RESTRICTED': [],
            'FIR': [],
            'AERODROMES': {},
            'META': {}
        }
    
    def extract_pib_metadata(self, root):
        meta = root.find('AreaPIBHeader')
        if meta is not None:
            self.categories['META'] = {
                'issued': meta.find('Issued').text if meta.find('Issued') is not None else '',
                'valid_from': meta.find('.//ValidFrom').text if meta.find('.//ValidFrom') is not None else '',
                'valid_to': meta.find('.//ValidTo').text if meta.find('.//ValidTo') is not None else '',
                'pib_id': root.get('PIBId', '')
            }
    
    def extract_aerodromes(self, root):
        for aerodrome in root.findall('.//Aerodrome'):
            code = aerodrome.find('Code').text
            self.categories['AERODROMES'][code] = {
                'name': aerodrome.find('Name').text,
                'city': aerodrome.find('CityName').text,
                'iata': aerodrome.find('IATA').text if aerodrome.find('IATA') is not None else None,
                'fir': aerodrome.find('.//FIR/ICAO').text if aerodrome.find('.//FIR/ICAO') is not None else None
            }
    
    def process_notams(self, root):
        for notam in root.findall('.//NOTAM'):
            notam_data = self._extract_notam_data(notam)
            self._categorize_notam(notam_data)
    
    def _extract_notam_data(self, notam):
        return {
            'id': notam.find('NOTAMNumber').text if notam.find('NOTAMNumber') is not None else '',
            'type': notam.find('NOTAMType').text if notam.find('NOTAMType') is not None else '',
            'fir': notam.find('.//FIR/ICAO').text if notam.find('.//FIR/ICAO') is not None else '',
            'location': notam.find('ItemA').text if notam.find('ItemA') is not None else '',
            'start_time': notam.find('ItemB').text if notam.find('ItemB') is not None else '',
            'end_time': notam.find('ItemC').text if notam.find('ItemC') is not None else '',
            'schedule': notam.find('ItemD').text if notam.find('ItemD') is not None else '',
            'text': notam.find('ItemE').text if notam.find('ItemE') is not None else '',
            'lower_limit': notam.find('ItemF').text if notam.find('ItemF') is not None else '',
            'upper_limit': notam.find('ItemG').text if notam.find('ItemG') is not None else ''
        }
    
    def _categorize_notam(self, notam):
        text = notam['text'].upper()
        if 'TEMPORARY RESTRICTED AREA' in text or 'TRA' in text:
            self.categories['TRA'].append(notam)
        elif 'DANGER AREA' in text or 'EGD' in text:
            self.categories['DANGER'].append(notam)
        elif 'RESTRICTED' in text:
            self.categories['RESTRICTED'].append(notam)
        
        # Also add to FIR category if it affects whole FIR
        if notam['location'] in ['EGTT', 'EGPX']:
            self.categories['FIR'].append(notam)
    
    def save_processed_data(self, output_dir):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        # Save each category to separate file
        for category, data in self.categories.items():
            filename = f'{category.lower()}_{timestamp}.json'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
