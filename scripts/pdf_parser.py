import pdfplumber
import pandas as pd
import re
import spacy

# Load spaCy for NLP
nlp = spacy.load("en_core_web_sm")

def parse_pdf(pdf_path):
    errors = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Try table extraction first
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    header = table[0]
                    if "Error Code" in header:
                        for row in table[1:]:
                            if len(row) >= 4 and re.match(r'ORA-\d{5}', row[0]):
                                errors.append({
                                    'code': row[0],
                                    'description': row[1],
                                    'cause': row[2],
                                    'solution': row[3]
                                })
                        continue
            
            # Fallback to text parsing
            text = page.extract_text(layout=True)
            current_error = None
            for line in text.split('\n'):
                if re.match(r'ORA-\d{5}', line):
                    if current_error:
                        errors.append(current_error)
                    current_error = {'code': line.split()[0]}
                elif current_error:
                    if 'Description:' in line:
                        current_error['description'] = line.split(':', 1)[1].strip()
                    elif 'Cause:' in line:
                        current_error['cause'] = line.split(':', 1)[1].strip()
                    elif 'Solution:' in line:
                        current_error['solution'] = line.split(':', 1)[1].strip()
            
            if current_error:
                errors.append(current_error)
    
    return pd.DataFrame(errors)
