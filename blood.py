import re
import os
import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        text = "".join(doc.page_content for doc in docs)
        return text
    except Exception as e:
        logging.error(f"Failed to extract text from PDF: {e}")
        return ""

def parse_blood_test_results(text):
    """Parse blood test values from extracted text using regex patterns."""
    # Enhanced patterns with variations in formatting
    patterns = {
        "Patient Name": r"(?:Patient\s*Name|Name\s*of\s*Patient|Patient|Mr\.|Mrs\.|Ms\.|Patient Details)\s*[:\n]*\s*([A-Za-z\.\s]+)",
        "Age": r"(?:Age|Patient\s*Age|Age&Gender)\s*[:;]\s*(\d+)(?:\s*Years)?",
        "Gender": r"(?:Gender|Sex|Age&Gender.*?)(Male|Female|M|F)",
        "Referred Doctor": r"(?:Referred\s*By|Referring\s*Doctor|Dr\.|Doctor|Physician|Reference Details)\s*[:;]\s*([^\n]+)",
        "Bill Number": r"(?:Invoice\s*No|Bill\s*No|Bill\s*Number|No|KDL-|Bill No\s*)\s*[:;]?\s*(\w+[-]?\d+)",
        "Haemoglobin": r"(?:Haemoglobin|Hb)\s*[:;]\s*(\d+\.?\d*)\s*(?:gms%|g%|g/dL)",
        "Total Count": r"(?:Total\s*Count|WBC)\s*[:;]\s*([0-9,]+)\s*(?:cells/cumm|/cumm)",
        "Neutrophils": r"(?:NEUTROPHILS|Neutrophils)\s*[:;]\s*(\d+)\s*%",
        "Lymphocytes": r"(?:LYMPHOCYTES|Lymphocytes)\s*[:;]\s*(\d+)\s*%",
        "Eosinophils": r"(?:EOSINOPHILS|Eosinophils)\s*[:;]\s*(\d+)\s*%",
        "Platelet Count": r"(?:Platelet\s*Count|Platelets)\s*[:;]\s*([0-9\.]+)\s*(?:lakhs|lakh|lac)?\s*(?:cells/cumm|/cumm)?",
        "RBC Count": r"(?:RBC\s*Count|RBC)\s*[:;]\s*(\d+\.?\d*)\s*(?:millions/cumm|mill/cumm|M/cumm)",
        "ESR": r"(?:ESR)\s*[:;]\s*(\d+)\s*(?:mm/1hour|mm/hr|mm/h)",
        "PCV": r"(?:PCV)(?:\s*-\s*\(\s*Hematocrit\s*\))?\s*[:;]\s*(\d+\.?\d*)\s*%",
        "MCV": r"(?:MCV)\s*[:;]\s*(\d+\.?\d*)\s*(?:FL|fl)",
        "MCH": r"(?:MCH)\s*[:;]\s*(\d+\.?\d*)\s*(?:pg)",
        "MCHC": r"(?:MCHC)\s*[:;]\s*(\d+\.?\d*)\s*(?:g/L)"
    }
    
    compiled_patterns = {key: re.compile(pattern, re.IGNORECASE) for key, pattern in patterns.items()}
    results = {}
    
    for key, pattern in compiled_patterns.items():
        match = pattern.search(text)
        if match:
            value = match.group(1).strip()
            
            # Clean up the value
            if key in ["Total Count", "Platelet Count"]:
                value = value.replace(',', '')  # Remove commas in numbers
            
            # Convert numeric values to float if applicable
            if key not in ["Patient Name", "Referred Doctor", "Bill Number", "Gender"]:
                try:
                    value = float(value)
                except ValueError:
                    logging.warning(f"Could not convert {key} value '{value}' to float")
            
            results[key] = value
    
    # Standardize gender format
    if "Gender" in results:
        if results["Gender"] in ["M", "m"]:
            results["Gender"] = "Male"
        elif results["Gender"] in ["F", "f"]:
            results["Gender"] = "Female"
    
    return results

def get_reference_ranges(age, gender):
    """Get appropriate reference ranges based on age and gender."""
    reference_ranges = {
        "Male": {
            "Haemoglobin": (13.5, 18.0), 
            "Total Count": (4500, 11000), 
            "Neutrophils": (40, 70), 
            "Lymphocytes": (20, 40), 
            "Eosinophils": (1, 6),
            "Platelet Count": (1.5, 4.5),  # In lakhs cells/cumm
            "RBC Count": (4.0, 6.0), 
            "ESR": (0, 10),
            "PCV": (40, 52),
            "MCV": (76, 96),
            "MCH": (27, 32),
            "MCHC": (32, 36)
        },
        "Female": {
            "Haemoglobin": (12.0, 16.0), 
            "Total Count": (4500, 11000), 
            "Neutrophils": (40, 70), 
            "Lymphocytes": (20, 40), 
            "Eosinophils": (1, 6),
            "Platelet Count": (1.5, 4.5),  # In lakhs cells/cumm
            "RBC Count": (3.5, 5.5), 
            "ESR": (0, 20),
            "PCV": (36, 48),
            "MCV": (76, 96),
            "MCH": (27, 32),
            "MCHC": (32, 36)
        }
    }
    
    try:
        age_value = int(float(age)) if age is not None else 30  # Default to 30 if age not provided
        
        if age_value < 18:
            # Default ranges for children
            return reference_ranges.get(gender, reference_ranges["Male"])
        elif age_value > 60:
            # Slightly modified ranges for elderly
            return reference_ranges.get(gender, reference_ranges["Male"])
        else:
            return reference_ranges.get(gender, reference_ranges["Male"])
    except (ValueError, TypeError):
        logging.warning(f"Invalid age or gender: Age={age}, Gender={gender}. Using adult male ranges as default.")
        return reference_ranges["Male"]