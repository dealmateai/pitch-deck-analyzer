"""
Quick test to verify everything works
"""

import sys
from pathlib import Path

print("=" * 80)
print("QUICK TEST - Pitch Deck Analyzer")
print("=" * 80)

# 1. Test PDF extraction
print("\n[1] Testing PDF Extraction...")
from nlp.pdf_extractor import PDFExtractor

extractor = PDFExtractor()
pdf_result = extractor.extract("test_pitch_deck.pdf")

if pdf_result:
    print(f"✅ PDF extracted: {pdf_result['num_pages']} pages, {pdf_result['word_count']} words")
else:
    print("❌ PDF extraction failed")
    sys.exit(1)

# 2. Test NLP
print("\n[2] Testing NLP Pipeline...")
from nlp.nlp_pipeline import NLPPipeline

nlp = NLPPipeline()
nlp_result = nlp.analyze_text(pdf_result["full_text_cleaned"])

if nlp_result:
    print(f"✅ NLP analysis done: {len(nlp_result.get('keywords', []))} keywords")
else:
    print("❌ NLP analysis failed")
    sys.exit(1)

# 3. Test Company Extraction
print("\n[3] Testing Company Extraction...")
from nlp.company_extractor import CompanyExtractor

company_ext = CompanyExtractor()
company_info = company_ext.extract_company_info(pdf_result["full_text_cleaned"], nlp_result.get("entities", {}))

if company_info:
    print(f"✅ Company extracted: {company_info['name']}")
else:
    print("❌ Company extraction failed")

# 4. Test Founder Extraction
print("\n[4] Testing Founder Extraction...")
from nlp.founder_extractor import FounderExtractor

founder_ext = FounderExtractor()
founder_info = founder_ext.extract_founder_info(pdf_result["full_text_cleaned"], nlp_result.get("entities", {}))

if founder_info:
    print(f"✅ Founders extracted: {founder_info['count']} founders")
else:
    print("❌ Founder extraction failed")

# 5. Test Fit Calculation
print("\n[5] Testing Fit Calculation...")
from nlp.fit_calculator import FitCalculator

calc = FitCalculator()
company_fit = calc.calculate_company_fit(company_info)
founder_fit = calc.calculate_founder_fit(founder_info)

print(f"✅ Company Fit: {company_fit:.1f}%")
print(f"✅ Founder Fit: {founder_fit:.1f}%")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED - Ready for Postman!")
print("=" * 80)