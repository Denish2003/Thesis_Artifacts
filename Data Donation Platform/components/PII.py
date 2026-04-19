# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine
# import warnings

# warnings.filterwarnings("ignore")

# def pii(text):
#     analyzer = AnalyzerEngine()
#     results = analyzer.analyze(
#         text=text,
#         entities=[],  # all default entities
#         language="en"
#     )

#     pii_data = []
#     for r in results:
#         pii_data.append({
#             "Entity Type": r.entity_type,
#             "Text": text[r.start:r.end],
#             "Confidence": round(r.score, 2)
#         })

#     return pii_data

# anonymized = anonymizer.anonymize(
    #     text=text,
    #     analyzer_results=results
    # )

    # print("\nAnonymized text:\n", anonymized.text)

import re

# Structured PII patterns
PII_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"\+?\d[\d\s().-]{7,}\d",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}

# Contextual name detection
def detect_names(text):
    pattern = r"(?:My name is|I am|I'm)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)"
    return [{"Text": m, "Entity": "NAME"} for m in re.findall(pattern, text)]

# Main PII function
def pii(text):
    results = []

    # Detect structured PII
    for entity, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            results.append({"Text": match.group(), "Entity": entity})

    # Detect names using context
    results.extend(detect_names(text))

    # Deduplicate
    seen = set()
    unique_results = []
    for r in results:
        if r["Text"] not in seen:
            unique_results.append(r)
            seen.add(r["Text"])

    return unique_results
