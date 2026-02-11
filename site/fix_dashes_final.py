#!/usr/bin/env python3
"""
Replace all ' – ' (en dashes used as parenthetical/clause separators) with
real punctuation: colons, commas, periods, semicolons, or sentence restructures.
Keep actual hyphens (e.g. 'real-time', 'board-ready') untouched.
"""
import os
import re
import glob

SITE_DIR = "/Users/cum/Downloads/goatsec_variant8_renderings/site"

def fix_dashes_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # First: remove en dashes from HTML comments (harmless)
    # <!-- WHAT WE DO – blah --> just strip the dash
    content = re.sub(r'(<!--[^>]*?) – ([^>]*?-->)', r'\1: \2', content)
    
    # For prose: ' – ' patterns need contextual replacement.
    # Strategy: most of these are "statement – clarification" which maps to
    # either a colon or a comma depending on what follows.
    
    # Pattern: "X – not Y" → "X, not Y"
    content = re.sub(r' – not ', ', not ', content)
    
    # Pattern: "X – and Y" → "X, and Y"  
    content = re.sub(r' – and ', ', and ', content)
    
    # Pattern: "X – or Y" → "X, or Y"
    content = re.sub(r' – or ', ', or ', content)
    
    # Pattern: "X – so Y" → "X, so Y"
    content = re.sub(r' – so ', ', so ', content)
    
    # Pattern: "X – we Y" → "X. We Y" (new sentence) — but only mid-sentence
    # Actually let's use ". " for these: "we handle X – we do Y" → "we handle X. We do Y"
    # This is tricky, safer to just use a comma or colon
    
    # Pattern: "X – from Y to Z" → "X: from Y to Z"
    content = re.sub(r' – from ', ': from ', content)
    
    # Pattern: "X – including Y" → "X, including Y"
    content = re.sub(r' – including ', ', including ', content)
    
    # Pattern: "X – especially Y" → "X, especially Y"
    content = re.sub(r' – especially ', ', especially ', content)
    
    # Pattern: "X – with Y" → "X, with Y"
    content = re.sub(r' – with ', ', with ', content)
    
    # Pattern: "X – whether Y" → "X, whether Y"
    content = re.sub(r' – whether ', ', whether ', content)
    
    # Pattern: "X – regardless Y" → "X, regardless Y"
    content = re.sub(r' – regardless ', ', regardless ', content)
    
    # Pattern: "X – on Y" → "X, on Y"  
    content = re.sub(r' – on a ', ', on a ', content)
    content = re.sub(r' – on an ', ', on an ', content)
    
    # Pattern: title separators "X – Y" in title tags → "X | Y"
    content = re.sub(r'(<title>[^<]*?) – ([^<]*?</title>)', r'\1 | \2', content)
    
    # Pattern: after a list/description → colon
    # "covers X, Y, and Z – plus A" → "covers X, Y, and Z, plus A"
    content = re.sub(r' – plus ', ', plus ', content)
    
    # Now handle remaining ' – ' occurrences.
    # Most remaining ones are "X – Y" where Y elaborates on X → use a colon
    # But if Y starts with lowercase and reads like a continuation, use comma
    
    # Replace remaining " – " followed by lowercase → comma
    content = re.sub(r' – ([a-z])', r', \1', content)
    
    # Replace remaining " – " followed by uppercase → colon  
    content = re.sub(r' – ([A-Z])', r'. \1', content)
    
    # Replace remaining " – " followed by anything else (numbers, etc) → colon
    content = re.sub(r' – ', ': ', content)
    
    # Also catch any standalone " - " that aren't hyphens (space-dash-space is not a hyphen)
    # But be careful: "1 - 2" ranges, "Phase 1 - Planning" etc are fine as-is
    # Leave these alone for now, they're less visually offensive than en dashes
    
    # Clean up double spaces
    content = re.sub(r'  +', ' ', content)
    
    # Fix any ". we" → ". We" capitalization
    content = re.sub(r'\. ([a-z])', lambda m: '. ' + m.group(1).upper(), content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        count = original.count(' – ')
        return count
    return 0

# Process all HTML files
all_html = glob.glob(os.path.join(SITE_DIR, '*.html')) + glob.glob(os.path.join(SITE_DIR, 'svc', '*.html'))

print(f"Processing {len(all_html)} files...\n")

total = 0
for filepath in sorted(all_html):
    fname = os.path.relpath(filepath, SITE_DIR)
    count = fix_dashes_in_file(filepath)
    if count:
        total += count
        print(f"  {fname}: fixed {count}")

print(f"\nTotal en dashes replaced: {total}")

# Verify none remain
remaining = 0
for filepath in all_html:
    with open(filepath, 'r') as f:
        c = f.read()
    remaining += c.count(' – ')

print(f"Remaining ' – ' in all files: {remaining}")
