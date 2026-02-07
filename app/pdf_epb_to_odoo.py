import re

# Expanded NOISE_PATTERNS to filter out unwanted text
NOISE_PATTERNS = [
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Email addresses
    r'\(?\+?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # Phone numbers
    r'(?i)\b(?:be\s)?\d{3}[.\s]?\d{3}[.\s]?\d{3}\b',  # VAT numbers
    r'[A-Za-z]\s?[-]?[\d]{1,5}\s?[A-Za-z][ ]+\d{4,}',  # Postal codes and addresses
    r'(?i)\b(?:benso-tec\s?bv|facq\s?diest)\b',  # Company names
    r'(?i)www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Website URLs
    r'(?i)geachte\s?(mevrouw|mijnheer)',  # Customer salutations
    r'(?i)no\s?article\s?quantite\s?libelle\s?prijs',  # Table headers
    r'(?i)(vendeur|verkoper|creatie\s?datum|drukdatum)',  # Document metadata
    r'(?i)(totaal\s?zonder\s?b\.t\.w|b\.t\.w|totaal\s?:)',  # Price/total lines
    r'(?i)(vriendelijke\s?groeten|voor\s?akkoord|handtekening)'  # Greeting/signature text
]

def is_valid_legend_item(item):
    if any(re.search(pattern, item) for pattern in NOISE_PATTERNS):
        return False
    if len(item) < 10 and not any(keyword in item.lower() for keyword in ['pump', 'valve', 'module', 'sensor', 'boiler']):
        return False
    if any(x in item.lower() for x in ['@', 'tel', 'fax']):
        return False
    if item.isupper():  # Filter out ALL CAPS
        return False
    if item.lower().startswith(('betreft:', 'naam:', 'email:', 'tel:')):
        return False
    return True

# Improve fallback extraction logic
# Lines to only extract if strong product indicators are found
def fallback_extraction(lines):
    if legend_section_found:
        return extracted_items  # Only use fallback if legend section is not found
    filtered_lines = []
    for line in lines:
        if len(line) >= 15 and (
            re.match(r'\d{6,}', line) or  # Product codes (6+ digits at start)
            re.match(r'^(vr|vp|vw)\d+', line) or  # Vaillant product codes
            any(keyword in line.lower() for keyword in ['pump', 'valve', 'module', 'sensor', 'boiler'])  # Strong product keywords
        ):
            filtered_lines.append(line)
    return filtered_lines

# Comment explaining the conservative fallback mechanism
# Fallback extraction should be conservative to avoid noise and only catch legitimate items.