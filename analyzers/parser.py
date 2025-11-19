"""
Module for parsing extracted text into structured resume sections.
Now uses pyresparser (NLP-based) for AI-powered extraction.
Fallback to regex if pyresparser fails.
"""

import re
from typing import Dict, List, Any
from utils.helpers import EMAIL_REGEX, PHONE_REGEX

try:
    from pyresparser import ResumeParser  # AI/ML: NLP-based parser
    PYPARSER_AVAILABLE = True
except ImportError:
    PYPARSER_AVAILABLE = False
    print("Warning: pyresparser not installed. Falling back to regex parsing.")


def parse_resume(text: str) -> Dict[str, Any]:
    """
    Parse the extracted text into a dictionary of resume sections using AI (pyresparser).
    
    Args:
        text (str): Raw text from the resume.
    
    Returns:
        Dict[str, Any]: Parsed data with sections and lists where applicable.
    """
    if not text:
        return {"error": "No text to parse"}
    
    parsed = {
        "name": "",
        "email": [],
        "phone": [],
        "skills": [],
        "education": [],
        "experience": []
    }
    
    if PYPARSER_AVAILABLE:
        try:
            # AI/ML: Use pyresparser for intelligent extraction
            data = ResumeParser(text).get_extracted_data()
            parsed["name"] = data.get("name", "")
            parsed["email"] = data.get("email", [])
            parsed["phone"] = data.get("mobile_number", [])  # pyresparser uses this key
            parsed["skills"] = data.get("skills", [])
            parsed["education"] = data.get("degree", []) or data.get("college_name", [])  # Combine
            parsed["experience"] = data.get("experience", [])
            print("AI parsing successful with pyresparser.")
            return parsed
        except Exception as e:
            print(f"AI parsing failed ({e}), falling back to regex.")
    
    # Fallback: Original regex-based parsing (unchanged for robustness)
    lines = text.split('\n')
    # Extract name: Assume first non-empty line
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(EMAIL_REGEX + '|' + PHONE_REGEX, stripped):
            parsed["name"] = stripped
            break
    
    # Extract emails and phones
    emails = re.findall(EMAIL_REGEX, text)
    phones = re.findall(PHONE_REGEX, text)
    parsed["email"] = list(set(emails))
    parsed["phone"] = list(set(phones))
    
    # Parse sections (simplified)
    current_section = None
    for line in lines:
        stripped = line.strip().lower()
        if stripped.startswith("education:") or stripped.startswith("education "):
            current_section = "education"
        elif stripped.startswith("experience:") or stripped.startswith("experience "):
            current_section = "experience"
        elif stripped.startswith("skills:") or stripped.startswith("skills "):
            current_section = "skills"
        elif current_section and stripped:
            if current_section == "skills":
                skill_list = re.split(r'[,\n•*-]', stripped)
                parsed["skills"].extend([s.strip() for s in skill_list if s.strip()])
            else:
                parsed[current_section].append(stripped)
    
    parsed["skills"] = list(set([s for s in parsed["skills"] if s]))
    
    return parsed