import pdfplumber
import pandas as pd
import re

def parse_pdf(pdf_path):
    errors = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # Use regex to find error codes and their details
            matches = re.findall(
                r'(ORA-\d{5}): (.+?)\nCause: (.+?)\nAction: (.+?)(?=\nORA-|\Z)',
                text,
                re.DOTALL
            )
            for match in matches:
                errors.append({
                    'code': match[0],
                    'description': match[1].strip(),
                    'cause': match[2].strip(),
                    'solution': match[3].strip()
                })
    return pd.DataFrame(errors)

# Example usage:
df = parse_pdf('/home/orasniper/oracle-chatbot/data/error-messages.pdf')
df.to_csv('/home/orasniper/oracle-chatbot/data/oracle_errors.csv', index=False)

