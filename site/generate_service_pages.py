#!/usr/bin/env python3
"""
GoatSec services.html → individual service pages generator.
Parses the monolithic services.html, assigns real images, and creates per-service HTML files.
"""

import re
import os
from html.parser import HTMLParser

SITE_DIR = "/Users/cum/Downloads/goatsec_variant8_renderings/site"
SVC_DIR = os.path.join(SITE_DIR, "svc")

# Unsplash images by category - curated for cybersecurity context, no faces
IMAGES = {
    "appsec": [
        "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=75&fit=crop",  # code on screen
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&q=75&fit=crop",  # code closeup
        "https://images.unsplash.com/photo-1516259762381-22954d7d3ad2?w=600&q=75&fit=crop",  # terminal code
        "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=600&q=75&fit=crop",  # code dark
        "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?w=600&q=75&fit=crop",  # code green
        "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600&q=75&fit=crop",  # matrix style
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=75&fit=crop",  # binary
        "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&q=75&fit=crop",  # github dark
        "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=600&q=75&fit=crop",  # code review
    ],
    "cloud": [
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=75&fit=crop",  # earth from space / network
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # network cables
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # server rack
        "https://images.unsplash.com/photo-1560732488-6b0df240254a?w=600&q=75&fit=crop",  # cloud/sky abstract
        "https://images.unsplash.com/photo-1639322537228-f710d846310a?w=600&q=75&fit=crop",  # server room blue
        "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?w=600&q=75&fit=crop",  # cloud computing
    ],
    "mobile": [
        "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600&q=75&fit=crop",  # phone in hand
        "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600&q=75&fit=crop",  # phone closeup
        "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=600&q=75&fit=crop",  # phones row
        "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=600&q=75&fit=crop",  # phone code
        "https://images.unsplash.com/photo-1585399000684-d2f72660f092?w=600&q=75&fit=crop",  # phone dark
    ],
    "rf": [
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # network
        "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=75&fit=crop",  # antenna
        "https://images.unsplash.com/photo-1516387938699-a93567ec168e?w=600&q=75&fit=crop",  # circuit
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=75&fit=crop",  # circuit board
        "https://images.unsplash.com/photo-1562408590-e32931084e23?w=600&q=75&fit=crop",  # radio tower
    ],
    "network": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # server rack
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # cables
        "https://images.unsplash.com/photo-1606765962248-7a0839806e83?w=600&q=75&fit=crop",  # network equipment
        "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=600&q=75&fit=crop",  # server
        "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=600&q=75&fit=crop",  # lan cables
    ],
    "hardware": [
        "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=75&fit=crop",  # circuit board
        "https://images.unsplash.com/photo-1516387938699-a93567ec168e?w=600&q=75&fit=crop",  # pcb
        "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=600&q=75&fit=crop",  # hardware
        "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?w=600&q=75&fit=crop",  # tech
        "https://images.unsplash.com/photo-1562408590-e32931084e23?w=600&q=75&fit=crop",  # electronics
    ],
    "ot": [
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600&q=75&fit=crop",  # industrial
        "https://images.unsplash.com/photo-1565043666747-69f6646db940?w=600&q=75&fit=crop",  # factory
        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600&q=75&fit=crop",  # power grid
        "https://images.unsplash.com/photo-1588508065123-287b28e013da?w=600&q=75&fit=crop",  # electronics
    ],
    "ai": [
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=75&fit=crop",  # AI chip
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=600&q=75&fit=crop",  # AI brain
        "https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=600&q=75&fit=crop",  # neural
        "https://images.unsplash.com/photo-1680474569854-81216b34417a?w=600&q=75&fit=crop",  # AI abstract
        "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=600&q=75&fit=crop",  # neural network
        "https://images.unsplash.com/photo-1694891788199-7b55accc68c7?w=600&q=75&fit=crop",  # AI
    ],
    "redteam": [
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&q=75&fit=crop",  # cyber
        "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?w=600&q=75&fit=crop",  # hacker hoodie
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=75&fit=crop",  # matrix
        "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=600&q=75&fit=crop",  # dark tech
        "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=600&q=75&fit=crop",  # terminal
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # server
    ],
    "grc": [
        "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75&fit=crop",  # paperwork
        "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&q=75&fit=crop",  # charts
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=75&fit=crop",  # office
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&q=75&fit=crop",  # business
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=75&fit=crop",  # dashboard
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=75&fit=crop",  # analytics
    ],
    "training": [
        "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&q=75&fit=crop",  # classroom
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&q=75&fit=crop",  # workshop
        "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=75&fit=crop",  # training
        "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&q=75&fit=crop",  # presentation
        "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=600&q=75&fit=crop",  # conference
    ],
    "ops": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # monitoring
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=75&fit=crop",  # dashboard
        "https://images.unsplash.com/photo-1639322537228-f710d846310a?w=600&q=75&fit=crop",  # server room
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=75&fit=crop",  # analytics
        "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=600&q=75&fit=crop",  # code screen
    ],
    "identity": [
        "https://images.unsplash.com/photo-1633265486064-086b219458ec?w=600&q=75&fit=crop",  # lock
        "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=75&fit=crop",  # access
        "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=600&q=75&fit=crop",  # auth
        "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=600&q=75&fit=crop",  # identity
    ],
    "data": [
        "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # data center
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=75&fit=crop",  # data viz
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # storage
        "https://images.unsplash.com/photo-1639322537228-f710d846310a?w=600&q=75&fit=crop",  # server
    ],
    "physical": [
        "https://images.unsplash.com/photo-1558002038-1055907df827?w=600&q=75&fit=crop",  # security camera
        "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&q=75&fit=crop",  # lock
        "https://images.unsplash.com/photo-1585399000684-d2f72660f092?w=600&q=75&fit=crop",  # building
        "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=600&q=75&fit=crop",  # facility
    ],
    "satellite": [
        "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=75&fit=crop",  # satellite
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=75&fit=crop",  # earth
        "https://images.unsplash.com/photo-1457364887197-9150188c107b?w=600&q=75&fit=crop",  # antenna dish
        "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=600&q=75&fit=crop",  # space
        "https://images.unsplash.com/photo-1454789548928-9efd52dc4031?w=600&q=75&fit=crop",  # astronaut
        "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=600&q=75&fit=crop",  # satellite 2
    ],
    "crypto": [
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=75&fit=crop",  # matrix
        "https://images.unsplash.com/photo-1633265486064-086b219458ec?w=600&q=75&fit=crop",  # lock
        "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=75&fit=crop",  # crypto
    ],
    "automotive": [
        "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=75&fit=crop",  # car
        "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=600&q=75&fit=crop",  # car tech
    ],
    "telecom": [
        "https://images.unsplash.com/photo-1562408590-e32931084e23?w=600&q=75&fit=crop",  # telecom tower
        "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=75&fit=crop",  # antenna
    ],
}

# Track image usage per category to avoid repeats
image_counters = {}

def get_image(cat):
    """Get next image for a category, cycling through available images."""
    if cat not in image_counters:
        image_counters[cat] = 0
    imgs = IMAGES.get(cat, IMAGES["appsec"])
    idx = image_counters[cat] % len(imgs)
    image_counters[cat] += 1
    return imgs[idx]

def slugify(title):
    """Convert service title to URL-friendly slug."""
    s = title.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def extract_cards(html_path):
    """Extract all service cards from services.html."""
    with open(html_path, 'r') as f:
        content = f.read()
    
    cards = []
    # Find each svc-card div
    pattern = r'<div class="svc-card"[^>]*data-cat="([^"]*)"[^>]*data-keywords="([^"]*)"[^>]*>'
    
    # Split by svc-card opening tags
    parts = re.split(r'(<div class="svc-card")', content)
    
    for i in range(1, len(parts), 2):
        if i+1 >= len(parts):
            break
        card_html = parts[i] + parts[i+1]
        # Extract up to the closing of the card (find the next svc-card or end of catalog)
        # Get just up to the next card boundary
        end_idx = card_html.find('\n    <div class="svc-card"')
        if end_idx == -1:
            end_idx = card_html.find('\n  </div>\n</div>')
        if end_idx > 0:
            card_html = card_html[:end_idx]
        
        # Extract metadata
        cat_match = re.search(r'data-cat="([^"]*)"', card_html)
        kw_match = re.search(r'data-keywords="([^"]*)"', card_html)
        title_match = re.search(r'<div class="svc-title">([^<]*)</div>', card_html)
        desc_match = re.search(r'<p class="svc-desc">([^<]*)</p>', card_html)
        
        if title_match:
            cat = cat_match.group(1) if cat_match else "appsec"
            title = title_match.group(1).strip()
            desc = desc_match.group(1).strip() if desc_match else ""
            keywords = kw_match.group(1) if kw_match else ""
            
            # Check if has real image or emoji placeholder
            has_real_image = 'svc-img" src=' in card_html
            existing_img_match = re.search(r'<img class="svc-img" src="([^"]*)"', card_html)
            existing_img = existing_img_match.group(1) if existing_img_match else None
            
            # Extract detail sections
            best_for_match = re.search(r'Best for</div>\s*<p[^>]*>(.*?)</p>', card_html, re.DOTALL)
            deliver_match = re.search(r'What we deliver</div>\s*<ul class="detail-list">(.*?)</ul>', card_html, re.DOTALL)
            how_match = re.search(r'How we work</div>\s*<ul class="detail-list">(.*?)</ul>', card_html, re.DOTALL)
            tools_match = re.search(r'Tools and frameworks</div>\s*<div class="detail-tags">(.*?)</div>', card_html, re.DOTALL)
            timeline_match = re.search(r'timeline-pill">⏱\s*(.*?)</span>', card_html)
            svc_param_match = re.search(r'contact\.html\?svc=([^"]*)', card_html)
            
            cards.append({
                'cat': cat,
                'title': title,
                'desc': desc,
                'keywords': keywords,
                'has_real_image': has_real_image,
                'existing_img': existing_img,
                'best_for': best_for_match.group(1).strip() if best_for_match else "",
                'deliver': deliver_match.group(1).strip() if deliver_match else "",
                'how': how_match.group(1).strip() if how_match else "",
                'tools': tools_match.group(1).strip() if tools_match else "",
                'timeline': timeline_match.group(1).strip() if timeline_match else "",
                'svc_param': svc_param_match.group(1) if svc_param_match else slugify(title),
                'slug': slugify(title),
                'raw_html': card_html,
            })
    
    return cards

SERVICE_PAGE_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>{title} — GoatSec</title>
  <meta name="description" content="{desc}" />
  <link rel="stylesheet" href="../shared.css" />
  <style>
    .svc-hero{{position:relative;overflow:hidden;border-radius:var(--r-xl);margin-bottom:32px}}
    .svc-hero img{{width:100%;height:320px;object-fit:cover;display:block}}
    .svc-hero-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(31,16,9,.7) 0%,transparent 60%);display:flex;align-items:flex-end;padding:32px}}
    .svc-hero-text{{color:#fff}}
    .svc-hero-tag{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);background:rgba(255,255,255,.15);backdrop-filter:blur(8px);padding:4px 12px;border-radius:999px;display:inline-block;margin-bottom:10px}}
    .svc-hero-title{{font-size:clamp(24px,3.5vw,40px);font-weight:800;line-height:1.1;margin-bottom:8px}}
    .svc-hero-desc{{font-size:15px;opacity:.9;max-width:60ch;line-height:1.6}}

    .svc-content{{display:grid;grid-template-columns:1fr 320px;gap:32px;margin-bottom:48px}}
    @media(max-width:800px){{.svc-content{{grid-template-columns:1fr}}}}

    .svc-main{{display:flex;flex-direction:column;gap:28px}}
    .svc-section-label{{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);margin-bottom:10px}}
    .svc-section p,.svc-section li{{font-size:14px;line-height:1.65;color:var(--text-2)}}
    .svc-section ul{{list-style:none;display:flex;flex-direction:column;gap:8px;padding:0}}
    .svc-section li{{padding-left:20px;position:relative}}
    .svc-section li::before{{content:"✦";position:absolute;left:0;color:var(--accent);font-size:10px;top:3px}}

    .svc-sidebar{{display:flex;flex-direction:column;gap:20px}}
    .svc-sidebar-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:20px}}
    .svc-sidebar-card h4{{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:12px}}

    .svc-tags{{display:flex;gap:6px;flex-wrap:wrap}}
    .svc-tag-pill{{font-size:11px;padding:4px 10px;border-radius:999px;background:var(--surface-mid);border:1px solid var(--line);color:var(--text-2)}}

    .svc-cta-box{{background:var(--surface);border:2px solid var(--accent);border-radius:var(--r-xl);padding:32px;text-align:center;margin:32px 0 48px}}
    .svc-cta-box h3{{font-size:22px;font-weight:700;margin-bottom:8px}}
    .svc-cta-box p{{font-size:14px;color:var(--text-muted);margin-bottom:18px;max-width:50ch;margin-left:auto;margin-right:auto}}
    .svc-cta-row{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}

    .svc-back{{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--text-muted);margin-bottom:20px;transition:color .15s}}
    .svc-back:hover{{color:var(--accent)}}
  </style>
</head>
<body>
<div id="nav-slot"></div>

<div class="wrap" style="padding-top:32px">
  <a href="../services.html" class="svc-back">← Back to All Services</a>

  <div class="svc-hero">
    <img src="{image_url}" alt="{title}" />
    <div class="svc-hero-overlay">
      <div class="svc-hero-text">
        <span class="svc-hero-tag">{cat_upper}</span>
        <h1 class="svc-hero-title">{title}</h1>
        <p class="svc-hero-desc">{desc}</p>
      </div>
    </div>
  </div>

  <div class="svc-content">
    <div class="svc-main">
      <div class="svc-section">
        <div class="svc-section-label">Best for</div>
        <p>{best_for}</p>
      </div>
      <div class="svc-section">
        <div class="svc-section-label">What we deliver</div>
        <ul>{deliver}</ul>
      </div>
      <div class="svc-section">
        <div class="svc-section-label">How we work</div>
        <ul>{how}</ul>
      </div>
    </div>
    <div class="svc-sidebar">
      <div class="svc-sidebar-card">
        <h4>Timeline</h4>
        <span class="timeline-pill">⏱ {timeline}</span>
      </div>
      <div class="svc-sidebar-card">
        <h4>Tools &amp; Frameworks</h4>
        <div class="svc-tags">{tools}</div>
      </div>
    </div>
  </div>

  <div class="svc-cta-box">
    <h3>Ready to get started?</h3>
    <p>Let's scope this together. No pressure, no jargon — just a conversation about what you need.</p>
    <div class="svc-cta-row">
      <a class="btn btn-accent" href="../contact.html?svc={svc_param}">Book a Scope Call →</a>
      <a class="btn btn-outline" href="../packages.html">See Packages</a>
    </div>
  </div>
</div>

<div id="footer-slot"></div>
<script src="../nav.js"></script>
</body>
</html>'''


def generate_pages(cards):
    """Generate individual service HTML pages."""
    os.makedirs(SVC_DIR, exist_ok=True)
    
    generated = []
    for card in cards:
        img = card['existing_img'] if card['has_real_image'] else get_image(card['cat'])
        
        # Clean up deliver/how HTML - ensure list items are preserved
        deliver = card['deliver'] if card['deliver'] else "<li>Detailed findings report</li><li>Executive summary</li><li>Remediation roadmap</li>"
        how = card['how'] if card['how'] else "<li>Scoping and planning</li><li>Assessment execution</li><li>Analysis and reporting</li><li>Debrief and handoff</li>"
        
        # Convert tool tags to pill format if needed
        tools = card['tools']
        if tools:
            tools = re.sub(r'<span class="detail-tag">', '<span class="svc-tag-pill">', tools)
        else:
            tools = '<span class="svc-tag-pill">Custom methodology</span>'
        
        html = SERVICE_PAGE_TEMPLATE.format(
            title=card['title'],
            desc=card['desc'],
            image_url=img,
            cat_upper=card['cat'].upper(),
            best_for=card['best_for'] if card['best_for'] else card['desc'],
            deliver=deliver,
            how=how,
            tools=tools,
            timeline=card['timeline'] if card['timeline'] else "Varies by scope",
            svc_param=card['svc_param'],
        )
        
        filename = card['slug'] + '.html'
        filepath = os.path.join(SVC_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(html)
        
        generated.append({
            'title': card['title'],
            'cat': card['cat'],
            'desc': card['desc'],
            'slug': card['slug'],
            'filename': filename,
            'image_url': img,
            'keywords': card['keywords'],
            'svc_param': card['svc_param'],
        })
        print(f"  ✓ svc/{filename}")
    
    return generated

def generate_index(generated_cards, html_path):
    """Generate new services.html as a lightweight index linking to individual pages."""
    
    # Group by category
    cats_ordered = []
    cats_seen = set()
    for c in generated_cards:
        if c['cat'] not in cats_seen:
            cats_ordered.append(c['cat'])
            cats_seen.add(c['cat'])
    
    cat_labels = {
        'appsec': 'Application Security', 'cloud': 'Cloud & Platform',
        'mobile': 'Mobile Security', 'rf': 'RF & Wireless',
        'network': 'Network Security', 'hardware': 'Hardware & IoT',
        'ot': 'OT / ICS', 'ai': 'AI & Machine Learning',
        'redteam': 'Red Team & Adversary Simulation', 'grc': 'GRC & Compliance',
        'training': 'Security Training', 'ops': 'Security Operations',
        'identity': 'Identity & Access', 'data': 'Data Security',
        'physical': 'Physical Security', 'satellite': 'Space & Satellite',
        'crypto': 'Cryptography & PKI', 'automotive': 'Automotive',
        'telecom': 'Telecom Security',
    }
    
    # Build filter buttons
    filter_btns = ['    <input class="search-bar" type="search" id="search-input" placeholder="Search services…" oninput="filterCards()" />']
    filter_btns.append('    <button class="filter-btn active" onclick="setFilter(\'all\',this)">All</button>')
    for cat in cats_ordered:
        label = cat_labels.get(cat, cat.title())
        filter_btns.append(f'    <button class="filter-btn" onclick="setFilter(\'{cat}\',this)">{label}</button>')
    
    # Build card grid
    card_htmls = []
    for c in generated_cards:
        card_htmls.append(f'''    <a class="svc-card-link" href="svc/{c['filename']}" data-cat="{c['cat']}" data-keywords="{c['keywords']}">
      <div class="svc-card">
        <img class="svc-img" src="{c['image_url']}" alt="{c['title']}" loading="lazy" />
        <div class="svc-body">
          <span class="svc-tag">{c['cat'].upper()}</span>
          <div class="svc-title">{c['title']}</div>
          <p class="svc-desc">{c['desc']}</p>
          <span class="svc-expand-btn">View details →</span>
        </div>
      </div>
    </a>''')
    
    index_html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>All Services — GoatSec</title>
  <meta name="description" content="Every information security service GoatSec can scope and deliver. 80+ services across AppSec, cloud, RF, satellite, hardware, OT/ICS, AI, red team, GRC, and beyond." />
  <link rel="stylesheet" href="shared.css" />
  <style>
    .filter-bar{{display:flex;gap:8px;flex-wrap:wrap;position:sticky;top:92px;z-index:50;background:rgba(201,188,158,.95);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--line);margin:0 -28px;padding:12px 28px}}
    @media(max-width:660px){{.filter-bar{{top:56px;overflow-x:auto;flex-wrap:nowrap;padding:10px 16px;margin:0 -16px}}}}
    .filter-btn{{padding:7px 15px;border-radius:999px;border:1px solid var(--line-med);background:var(--surface-mid);cursor:pointer;font-size:12px;font-weight:500;color:var(--text-2);transition:all .15s;white-space:nowrap;flex-shrink:0}}
    .filter-btn:hover{{background:var(--surface);box-shadow:var(--shadow-sm)}}
    .filter-btn.active{{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 4px 14px rgba(138,94,46,.28)}}
    .search-bar{{min-width:180px;max-width:280px;flex-shrink:0;padding:8px 14px;border-radius:999px;border:1px solid var(--line-med);background:var(--surface);font-size:13px;color:var(--text);outline:none;transition:border-color .2s,box-shadow .2s}}
    .search-bar:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(138,94,46,.12)}}
    .catalog-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;margin-top:24px}}
    @media(max-width:660px){{.catalog-grid{{grid-template-columns:1fr}}}}
    .svc-card-link{{text-decoration:none;color:inherit;display:block}}
    .svc-card{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-xl);overflow:hidden;box-shadow:var(--shadow-sm);transition:box-shadow .2s,transform .2s;display:flex;flex-direction:column;height:100%}}
    .svc-card:hover{{box-shadow:var(--shadow);transform:translateY(-2px)}}
    .svc-card.hidden{{display:none}}
    .svc-img{{width:100%;height:150px;object-fit:cover;display:block;flex-shrink:0}}
    .svc-body{{padding:18px 20px 14px;flex:1;display:flex;flex-direction:column}}
    .svc-tag{{display:inline-flex;align-items:center;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:6px}}
    .svc-title{{font-size:16px;font-weight:700;margin-bottom:6px;line-height:1.25}}
    .svc-desc{{font-size:13px;line-height:1.6;color:var(--text-muted);flex:1;margin-bottom:12px}}
    .svc-expand-btn{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;color:var(--accent);margin-top:auto}}
    .count-label{{font-size:13px;color:var(--text-muted)}}
    #no-results{{display:none;grid-column:1/-1;text-align:center;padding:60px 0;color:var(--text-muted)}}
  </style>
</head>
<body>
<div id="nav-slot"></div>

<div class="wrap">
  <div class="hero-wrap" style="margin-bottom:0">
    <div class="hero-content" style="padding:48px 48px 44px">
      <div class="eyebrow">All Services</div>
      <h1 class="h1">Every security discipline. <span>One accountable partner.</span></h1>
      <p class="lead">From AppSec and cloud hardening to satellite security, RF, mobile, OT/ICS, hardware, and beyond. Click any tile to see full scope, deliverables, and timeline.</p>
    </div>
  </div>
</div>

<div class="wrap">
  <div class="filter-bar" id="filter-bar">
{chr(10).join(filter_btns)}
  </div>
</div>

<div class="wrap">
  <div style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
    <p class="count-label"><span id="visible-count">0</span> services</p>
  </div>
  <div class="catalog-grid" id="catalog">
{chr(10).join(card_htmls)}
    <div id="no-results"><p>No services match your search.</p></div>
  </div>
</div>

<div id="footer-slot"></div>
<script src="nav.js"></script>
<script>
let currentFilter = 'all';
function setFilter(cat, btn) {{
  currentFilter = cat;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if(btn) btn.classList.add('active');
  filterCards();
}}
function filterCards() {{
  const q = (document.getElementById('search-input').value || '').toLowerCase();
  let count = 0;
  document.querySelectorAll('.svc-card-link').forEach(link => {{
    const cat = link.dataset.cat;
    const kw = (link.dataset.keywords || '').toLowerCase();
    const title = (link.querySelector('.svc-title')?.textContent || '').toLowerCase();
    const desc = (link.querySelector('.svc-desc')?.textContent || '').toLowerCase();
    const catMatch = currentFilter === 'all' || cat === currentFilter;
    const textMatch = !q || title.includes(q) || desc.includes(q) || kw.includes(q);
    const show = catMatch && textMatch;
    link.style.display = show ? '' : 'none';
    if(show) count++;
  }});
  document.getElementById('visible-count').textContent = count;
  document.getElementById('no-results').style.display = count === 0 ? '' : 'none';
}}
document.addEventListener('DOMContentLoaded', filterCards);
</script>
</body>
</html>'''
    
    with open(html_path, 'w') as f:
        f.write(index_html)
    print(f"\\n✓ Updated {html_path} (lightweight index with {len(generated_cards)} cards)")


if __name__ == '__main__':
    print("Extracting service cards from services.html...")
    html_path = os.path.join(SITE_DIR, "services.html")
    cards = extract_cards(html_path)
    print(f"Found {len(cards)} service cards\\n")
    
    print("Generating individual service pages...")
    generated = generate_pages(cards)
    print(f"\\nGenerated {len(generated)} service pages in svc/")
    
    print("\\nGenerating new services.html index...")
    generate_index(generated, html_path)
    
    print("\\nDone!")
