import xml.etree.ElementTree as ET
import json
import os

def parse_notam_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    notams = []
    for notam in root.findall('.//NOTAM'):
        notam_data = {
            'id': notam.find('NOTAMNumber').text if notam.find('NOTAMNumber') is not None else '',
            'type': notam.find('NOTAMType').text if notam.find('NOTAMType') is not None else '',
            'category': 'TRA' if 'TEMPORARY RESTRICTED AREA' in notam.find('ItemE').text else 'NORMAL',
            'text': notam.find('ItemE').text if notam.find('ItemE') is not None else '',
            'start_time': notam.find('ItemB').text if notam.find('ItemB') is not None else '',
            'end_time': notam.find('ItemC').text if notam.find('ItemC') is not None else ''
        }
        notams.append(notam_data)
    
    return notams

def categorize_notams(notams):
    categories = {
        'TRA': [],
        'DANGER': [],
        'RESTRICTED': [],
        'OTHER': []
    }
    
    for notam in notams:
        if 'TEMPORARY RESTRICTED AREA' in notam['text'].upper():
            categories['TRA'].append(notam)
        elif 'DANGER AREA' in notam['text'].upper():
            categories['DANGER'].append(notam)
        elif 'RESTRICTED' in notam['text'].upper():
            categories['RESTRICTED'].append(notam)
        else:
            categories['OTHER'].append(notam)
    
    return categories

def save_categorized_notams(categories, output_dir):
    for category, notams in categories.items():
        output_file = os.path.join(output_dir, f'{category.lower()}_notams.json')
        with open(output_file, 'w') as f:
            json.dump(notams, f, indent=2)
