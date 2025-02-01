import pdfplumber
import pandas as pd

def extract_errors(pdf_path):
    errors = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                if "ORA-" in line:
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        error_code = parts[0].strip()
                        description = parts[1].strip()
                        errors.append({"error_code": error_code, "description": description})
    return pd.DataFrame(errors)

df = extract_errors("data/error-messages.pdf")
df.to_csv("data/errors.csv", index=False)
