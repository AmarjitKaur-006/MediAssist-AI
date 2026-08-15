import re       # re -> Python's regular expression module.

def correct_numeric_ocr_errors(text: str) -> str:
    """
    Correct high-confidence OCR mistakes involving '@'
    inside numeric-looking values.

    Examples:
        12.@ -> 12.0
        3@   -> 30
        10@  -> 100

    Text such as:
        Patient Name: A@ron

    remains unchanged.
    """

    # Correct decimal values such as 12.@
    text = re.sub(
        r"(\d+)\.@(?=\s|[-–—]|$)",
        r"\g<1>.0",
        text
    )

    # Correct integer values such as 3@ and 10@
    text = re.sub(
        r"(\d+)@(?=\s|[-–—]|$)",
        r"\g<1>0",
        text
    )

    return text



def clean_medical_text(text: str) -> str:
    """
    Clean and normalize raw medical report text.

    This function performs safe formatting normalization.
    It does NOT attempt to diagnose the patient or change
    medical values.
    """

    # 1. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    ## Different operating systems can represent a new line differently.
    ## For example:
    ## Windows → \r\n, Linux   → \n, Older Mac → \r
    ## We standardize everything to: \n
    ## This prevents weird formatting later. /*

    # 2. Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split("\n")]
    #Suppose OCR gives: Hemoglobin: 11.2 g/dL
    #strip() removes unnecessary whitespace around the line: Hemoglobin: 11.2 g/dL

    # 3. Remove completely empty lines
    lines = [line for line in lines if line]
    #So: Hemoglobin: 11.2 g/dL   \n\n\n       Reference Range: 12.0 - 16.0 g/dL becomes:
    #Hemoglobin: 11.2 g/dL /n Reference Range: 12.0 - 16.0 g/dL

    # 4. Normalize multiple spaces/tabs to a single space
    lines = [re.sub(r"[ \t]+", " ", line) for line in lines]


    # 5. Correct high-confidence numeric OCR errors
    text = "\n".join(lines)
    text = correct_numeric_ocr_errors(text)


    # 6. Normalize a few common medical units
    cleaned_lines = []

    for line in text.split("\n"):
        line = re.sub(r"\bg/dl\b", "g/dL", line, flags=re.IGNORECASE)
        line = re.sub(r"\bng/ml\b", "ng/mL", line, flags=re.IGNORECASE)
        line = re.sub(r"/ul\b", "/uL", line, flags=re.IGNORECASE)

        cleaned_lines.append(line)

    # 6. Join everything back together
    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text