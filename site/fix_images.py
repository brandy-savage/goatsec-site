#!/usr/bin/env python3
"""
Fix duplicate/generic images across all 95 service pages.
Each service gets a unique, contextually relevant image. No duplicates.
"""
import os
import re

SITE_DIR = "/Users/cum/Downloads/goatsec_variant8_renderings/site"
SVC_DIR = os.path.join(SITE_DIR, "svc")

# One unique image per service, mapped by slug.
# Rules: NO code-on-screen unless it's literally a code review service.
# Diverse subjects: architecture, infrastructure, industry, abstract, hardware, nature metaphors.
# Every URL is unique across the entire set.

IMAGE_MAP = {
    # ── APPSEC (9) ──
    "asvs-application-security-assessment": "https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?w=600&q=75&fit=crop",  # code on screen (appropriate - it IS code assessment)
    "threat-modeling": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&q=75&fit=crop",  # whiteboard planning
    "secure-sdlc-design-and-implementation": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=600&q=75&fit=crop",  # workflow diagram
    "manual-code-review": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&q=75&fit=crop",  # code closeup (appropriate)
    "api-security-review": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # network connections
    "web-application-penetration-test": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&q=75&fit=crop",  # cyber abstract
    "software-composition-analysis-and-sbom": "https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=600&q=75&fit=crop",  # package boxes / supply
    "security-champion-program": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600&q=75&fit=crop",  # team collaboration
    "smart-contract-security-audit": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=600&q=75&fit=crop",  # blockchain abstract

    # ── CLOUD (6) ──
    "cloud-security-posture-review": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&q=75&fit=crop",  # earth from space
    "iam-governance-and-least-privilege-enforcement": "https://images.unsplash.com/photo-1633265486064-086b219458ec?w=600&q=75&fit=crop",  # padlock
    "kubernetes-security-hardening": "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=600&q=75&fit=crop",  # containers at port
    "infrastructure-as-code-security": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=600&q=75&fit=crop",  # blueprint / architecture
    "serverless-and-function-security-review": "https://images.unsplash.com/photo-1560732488-6b0df240254a?w=600&q=75&fit=crop",  # cloud abstract
    "container-image-security-and-registry-hardening": "https://images.unsplash.com/photo-1494412574643-ff11b0a5eb19?w=600&q=75&fit=crop",  # shipping containers

    # ── MOBILE (5) ──
    "mobile-application-penetration-test-ios-and-android": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600&q=75&fit=crop",  # phone
    "mobile-binary-analysis-and-reverse-engineering": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&q=75&fit=crop",  # circuit board macro
    "mdm-and-enterprise-mobile-security": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=600&q=75&fit=crop",  # office devices
    "mobile-payments-and-nfc-security-review": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&q=75&fit=crop",  # contactless payment
    "ios-secure-enclave-and-keychain-security-review": "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?w=600&q=75&fit=crop",  # iPhone closeup

    # ── RF / WIRELESS (6) ──
    "wireless-network-security-assessment": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # network cables
    "bluetooth-and-ble-security-assessment": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&q=75&fit=crop",  # wireless earbuds
    "iot-wireless-protocol-assessment": "https://images.unsplash.com/photo-1558346490-a72e53ae2d4f?w=600&q=75&fit=crop",  # smart home sensors
    "rfid-and-physical-access-control-security": "https://images.unsplash.com/photo-1585128903994-9788298932a4?w=600&q=75&fit=crop",  # keycard reader
    "software-defined-radio-signal-analysis": "https://images.unsplash.com/photo-1562408590-e32931084e23?w=600&q=75&fit=crop",  # radio antenna
    "automotive-rf-and-keyless-entry-security": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=600&q=75&fit=crop",  # car key fob

    # ── NETWORK (5) ──
    "internal-network-penetration-test": "https://images.unsplash.com/photo-1606765962248-7a0839806e83?w=600&q=75&fit=crop",  # ethernet switch
    "external-attack-surface-assessment": "https://images.unsplash.com/photo-1573164713714-d95e436ab8d6?w=600&q=75&fit=crop",  # server rack
    "firewall-rule-review-and-segmentation-assessment": "https://images.unsplash.com/photo-1558002038-1055907df827?w=600&q=75&fit=crop",  # security fence
    "vpn-and-remote-access-security-review": "https://images.unsplash.com/photo-1563986768609-322da13575f2?w=600&q=75&fit=crop",  # tunnel
    "active-directory-security-assessment": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&q=75&fit=crop",  # dashboard analytics

    # ── HARDWARE / IoT (5) ──
    "hardware-and-embedded-device-security": "https://images.unsplash.com/photo-1516387938699-a93567ec168e?w=600&q=75&fit=crop",  # PCB macro
    "firmware-security-analysis": "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?w=600&q=75&fit=crop",  # chip closeup
    "hardware-supply-chain-risk-assessment": "https://images.unsplash.com/photo-1553413077-190dd305871c?w=600&q=75&fit=crop",  # warehouse logistics
    "iot-product-security-program": "https://images.unsplash.com/photo-1556155092-490a1ba16284?w=600&q=75&fit=crop",  # smart home
    "side-channel-attack-assessment": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&q=75&fit=crop",  # oscilloscope

    # ── OT / ICS (4) ──
    "ot-and-ics-security-assessment": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600&q=75&fit=crop",  # industrial
    "scada-and-hmi-security-review": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?w=600&q=75&fit=crop",  # power plant
    "iec-62443-and-ot-framework-compliance": "https://images.unsplash.com/photo-1565043666747-69f6646db940?w=600&q=75&fit=crop",  # factory floor
    "nerc-cip-compliance-support": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&q=75&fit=crop",  # power lines

    # ── AI (6) ──
    "llm-and-generative-ai-security-assessment": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=600&q=75&fit=crop",  # AI chip
    "ml-model-security-and-adversarial-robustness": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=600&q=75&fit=crop",  # AI brain
    "agentic-ai-and-autonomous-system-security": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=600&q=75&fit=crop",  # robot
    "ai-governance-and-policy-framework": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=600&q=75&fit=crop",  # documents/desk
    "ai-model-supply-chain-security": "https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=600&q=75&fit=crop",  # neural network
    "ai-red-teaming-and-jailbreak-research": "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=600&q=75&fit=crop",  # abstract neural

    # ── RED TEAM (6) ──
    "full-scope-red-team-operation": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?w=600&q=75&fit=crop",  # hacker silhouette
    "social-engineering-and-phishing-simulation": "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=600&q=75&fit=crop",  # email/dark screen
    "physical-security-red-team": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&q=75&fit=crop",  # lock/door
    "purple-team-exercise": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&q=75&fit=crop",  # team collaboration
    "assumed-breach-and-lateral-movement-assessment": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&q=75&fit=crop",  # matrix / data
    "ransomware-resilience-assessment": "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=600&q=75&fit=crop",  # terminal dark

    # ── GRC (7) ──
    "soc-2-readiness-and-preparation": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&q=75&fit=crop",  # charts/analytics
    "iso-27001-isms-implementation": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=75&fit=crop",  # professional office
    "hipaa-security-rule-assessment": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?w=600&q=75&fit=crop",  # hospital
    "pci-dss-scoping-and-readiness": "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?w=600&q=75&fit=crop",  # credit cards
    "fedramp-authorization-support": "https://images.unsplash.com/photo-1501466044931-62695aada8e9?w=600&q=75&fit=crop",  # government building
    "privacy-and-data-protection-assessment": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&q=75&fit=crop",  # privacy / hand on glass
    "third-party-risk-management-program": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=75&fit=crop",  # analytics dashboard

    # ── TRAINING (5) ──
    "security-awareness-training-program": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600&q=75&fit=crop",  # classroom
    "executive-and-board-security-education": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=600&q=75&fit=crop",  # boardroom
    "developer-secure-coding-workshop": "https://images.unsplash.com/photo-1531482615713-2afd69097998?w=600&q=75&fit=crop",  # workshop
    "incident-response-tabletop-exercise": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?w=600&q=75&fit=crop",  # presentation
    "threat-intelligence-analyst-training": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=600&q=75&fit=crop",  # analyst screen
    "security-policy-and-standards-development": "https://images.unsplash.com/photo-1568992687947-868a62a9f521?w=600&q=75&fit=crop",  # documents stacked

    # ── SECOPS (5) ──
    "siem-build-and-detection-engineering": "https://images.unsplash.com/photo-1639322537228-f710d846310a?w=600&q=75&fit=crop",  # server room blue
    "soar-playbook-development": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=600&q=75&fit=crop",  # team at screens
    "threat-hunting-program-and-engagements": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600&q=75&fit=crop",  # cyber grid — wait, already used. need unique
    "incident-response-retainer": "https://images.unsplash.com/photo-1557862921-37829c790f19?w=600&q=75&fit=crop",  # emergency phone
    "vulnerability-management-program-design": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&q=75&fit=crop",  # dashboard — wait, already used
    "digital-forensics-and-incident-investigation": "https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=600&q=75&fit=crop",  # magnifying glass

    # ── IDENTITY (4) ──
    "identity-architecture-review": "https://images.unsplash.com/photo-1548092372-0d1bd40894a3?w=600&q=75&fit=crop",  # fingerprint
    "privileged-access-management-assessment": "https://images.unsplash.com/photo-1555952517-2e8e729e0b44?w=600&q=75&fit=crop",  # vault
    "zero-trust-architecture-assessment": "https://images.unsplash.com/photo-1496368077930-c1e31b4e5b44?w=600&q=75&fit=crop",  # abstract grid
    "joiner-mover-leaver-process-review": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=600&q=75&fit=crop",  # handshake

    # ── DATA (4) ──
    "data-classification-and-protection-assessment": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&q=75&fit=crop",  # filing cabinet
    "database-security-assessment": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop",  # data cables — wait dup
    "secrets-management-and-credential-hygiene": "https://images.unsplash.com/photo-1507209696998-3c532be9b2b5?w=600&q=75&fit=crop",  # combination lock
    "backup-and-recovery-security-review": "https://images.unsplash.com/photo-1506399558188-acca6f8cbf41?w=600&q=75&fit=crop",  # safe deposit boxes

    # ── PHYSICAL (3) ──
    "physical-security-assessment": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&q=75&fit=crop",  # lock — wait dup
    "data-center-and-server-room-security-review": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop",  # datacenter — wait dup
    "insider-threat-program-design": "https://images.unsplash.com/photo-1453738773917-9c3eff1db985?w=600&q=75&fit=crop",  # shadowy figure

    # ── SATELLITE (6) ──
    "satellite-ground-station-security-assessment": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&q=75&fit=crop",  # satellite in space
    "satellite-command-and-control-security": "https://images.unsplash.com/photo-1457364887197-9150188c107b?w=600&q=75&fit=crop",  # dish antenna
    "vsat-and-satellite-internet-security-assessment": "https://images.unsplash.com/photo-1516849841032-87cbac4d88f7?w=600&q=75&fit=crop",  # night sky
    "gps-and-navigation-signal-security-assessment": "https://images.unsplash.com/photo-1476973422084-e0fa66ff9456?w=600&q=75&fit=crop",  # compass/navigation
    "space-system-threat-modeling": "https://images.unsplash.com/photo-1454789548928-9efd52dc4031?w=600&q=75&fit=crop",  # astronaut
    "satellite-rf-downlink-interception-assessment": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=600&q=75&fit=crop",  # satellite dish

    # ── CRYPTO (3) ──
    "cryptographic-implementation-review": "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=600&q=75&fit=crop",  # abstract math
    "pki-design-and-implementation-review": "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=600&q=75&fit=crop",  # abstract geometric
    "post-quantum-cryptography-readiness": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&q=75&fit=crop",  # quantum — wait dup w/ side channel

    # ── AUTOMOTIVE (2) ──
    "automotive-ecu-and-can-bus-security": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&q=75&fit=crop",  # car
    "vehicle-telematics-and-connectivity-security": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&q=75&fit=crop",  # car dashboard

    # ── TELECOM (2) ──
    "ss7-and-telecom-protocol-security-assessment": "https://images.unsplash.com/photo-1423666639041-f56000c27a9a?w=600&q=75&fit=crop",  # cell towers
    "voip-and-sip-infrastructure-security": "https://images.unsplash.com/photo-1596524430615-b46475ddff6e?w=600&q=75&fit=crop",  # phone headset
}

# Fix duplicates I spotted above
IMAGE_MAP["threat-hunting-program-and-engagements"] = "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=600&q=75&fit=crop"  # analyst screen — wait, also dup w/ training
# Need truly unique ones for these:
IMAGE_MAP["threat-hunting-program-and-engagements"] = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&q=75&fit=crop"  # retro tech / hunt vibe
IMAGE_MAP["vulnerability-management-program-design"] = "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&q=75&fit=crop"  # monitoring screens
IMAGE_MAP["database-security-assessment"] = "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&q=75&fit=crop"
# ^^^ that's still dup with wireless. Fix:
IMAGE_MAP["database-security-assessment"] = "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&q=75&fit=crop"  # terminal dark mode
IMAGE_MAP["physical-security-assessment"] = "https://images.unsplash.com/photo-1585128903994-9788298932a4?w=600&q=75&fit=crop"
# ^^^ dup with rfid. Fix:
IMAGE_MAP["physical-security-assessment"] = "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&q=75&fit=crop"  # modern office
IMAGE_MAP["data-center-and-server-room-security-review"] = "https://images.unsplash.com/photo-1606765962248-7a0839806e83?w=600&q=75&fit=crop"
# ^^^ dup with network. Fix:
IMAGE_MAP["data-center-and-server-room-security-review"] = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600&q=75&fit=crop"
# ^^^ dup with api. Fix:
IMAGE_MAP["data-center-and-server-room-security-review"] = "https://images.unsplash.com/photo-1600267185393-e158a98703de?w=600&q=75&fit=crop"  # server room corridor
IMAGE_MAP["post-quantum-cryptography-readiness"] = "https://images.unsplash.com/photo-1534723452862-4c874018d66d?w=600&q=75&fit=crop"  # abstract light / quantum
IMAGE_MAP["physical-security-red-team"] = "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600&q=75&fit=crop"
# ^^^ Still keeping but check for dup. Let me assign a different one:
IMAGE_MAP["physical-security-red-team"] = "https://images.unsplash.com/photo-1459767129954-1b1c1f9b9ace?w=600&q=75&fit=crop"  # building exterior

# Verify no duplicates
vals = list(IMAGE_MAP.values())
dupes = [v for v in vals if vals.count(v) > 1]
if dupes:
    print(f"WARNING: {len(set(dupes))} duplicate URLs found:")
    for d in set(dupes):
        keys = [k for k, v in IMAGE_MAP.items() if v == d]
        print(f"  {d[:60]}... → {keys}")
else:
    print(f"✓ All {len(vals)} images are unique")

print(f"\nTotal services mapped: {len(IMAGE_MAP)}")

# Now apply to all service pages and services.html index
def update_svc_page(filepath, slug):
    """Update the image in an individual service page."""
    if slug not in IMAGE_MAP:
        return False
    with open(filepath, 'r') as f:
        content = f.read()
    new_img = IMAGE_MAP[slug]
    # Replace the hero image src
    content = re.sub(
        r'<img src="[^"]*" alt="',
        f'<img src="{new_img}" alt="',
        content,
        count=1
    )
    with open(filepath, 'w') as f:
        f.write(content)
    return True

def update_index(index_path):
    """Update images in the services.html index."""
    with open(index_path, 'r') as f:
        content = f.read()
    
    for slug, img_url in IMAGE_MAP.items():
        # Find the card link for this slug and update its image
        pattern = rf'(href="svc/{re.escape(slug)}\.html"[^>]*>[\s\S]*?<img class="svc-img" src=")([^"]*)'
        content = re.sub(pattern, rf'\g<1>{img_url}', content)
    
    with open(index_path, 'w') as f:
        f.write(content)


# Run
print("\nUpdating individual service pages...")
updated = 0
for filename in os.listdir(SVC_DIR):
    if not filename.endswith('.html'):
        continue
    slug = filename[:-5]  # remove .html
    filepath = os.path.join(SVC_DIR, filename)
    if update_svc_page(filepath, slug):
        updated += 1

print(f"Updated {updated} service pages")

print("\nUpdating services.html index...")
update_index(os.path.join(SITE_DIR, "services.html"))
print("✓ Index updated")

print("\nDone!")
