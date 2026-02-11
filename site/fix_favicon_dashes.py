#!/usr/bin/env python3
"""
1. Add favicon to all HTML files
2. Replace em dashes (—) with contextually appropriate punctuation
"""
import os
import re
import glob

SITE_DIR = "/Users/cum/Downloads/goatsec_variant8_renderings/site"

FAVICON_HTML = '  <link rel="icon" sizes="32x32" href="{prefix}favicon-32.png" />\n  <link rel="icon" sizes="192x192" href="{prefix}favicon-192.png" />\n  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png" />'

def add_favicon(filepath):
    """Add favicon links after the last <meta> or <link> in <head>."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'favicon' in content:
        return False  # Already has favicon
    
    # Determine prefix based on directory depth
    if '/svc/' in filepath:
        prefix = '../'
    else:
        prefix = ''
    
    fav = FAVICON_HTML.format(prefix=prefix)
    
    # Insert before </head>
    content = content.replace('</head>', fav + '\n</head>')
    
    with open(filepath, 'w') as f:
        f.write(content)
    return True

def fix_em_dashes(filepath):
    """Replace — with contextually appropriate punctuation."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Common patterns and replacements:
    # "X — Y" in titles/headings → "X: Y" or "X. Y" or " - "
    # "word — word" in prose → ": " or " - " depending on context
    
    # Pattern: em dash between clauses in prose → colon or dash
    # We'll use " – " (en dash with spaces) as the general replacement
    # since it's the typographically correct alternative for parenthetical asides
    # But for title patterns like "Title — Subtitle" use ": "
    
    # In <title> tags: use " | "
    content = re.sub(r'(<title>[^<]*?)—([^<]*?</title>)', r'\1|\2', content)
    
    # In headings (h1-h4): use ": "
    content = re.sub(r'(<h[1-4][^>]*>[^<]*?)—([^<]*?</h[1-4]>)', r'\1:\2', content)
    
    # "Best for:" sections and similar label contexts: use ". "  
    # But most prose em dashes are parenthetical asides → use " – " (en dash)
    
    # General: replace all remaining — with " – " (en dash), 
    # but clean up double spaces
    content = content.replace(' — ', ' – ')
    content = content.replace('— ', ' – ')
    content = content.replace(' —', ' –')
    content = content.replace('—', ' – ')
    
    # Clean up any resulting double spaces
    content = re.sub(r'  +', ' ', content)
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        count = original.count('—')
        return count
    return 0

# Process all HTML files
all_html = glob.glob(os.path.join(SITE_DIR, '*.html')) + glob.glob(os.path.join(SITE_DIR, 'svc', '*.html'))

print(f"Processing {len(all_html)} HTML files...\n")

favicon_count = 0
dash_total = 0

for filepath in sorted(all_html):
    fname = os.path.relpath(filepath, SITE_DIR)
    
    added = add_favicon(filepath)
    if added:
        favicon_count += 1
    
    dashes = fix_em_dashes(filepath)
    if dashes:
        dash_total += dashes
        print(f"  {fname}: replaced {dashes} em dashes")

print(f"\nFavicon added to {favicon_count} files")
print(f"Em dashes replaced: {dash_total} total")
