/* GoatSec shared nav + footer injector */
(function(){

const NAV = `
<nav class="nav">
  <div class="nav-top">
    <a class="nav-logo" href="home.html">
      <img src="https://goatinfosec.files.wordpress.com/2024/02/goatsec-logo-type-horizontal.png?w=1024" alt="GoatSec" />
    </a>
    <div style="display:flex;align-items:center;gap:10px">
      <a class="nav-cta" href="contact.html">Book a Scope Call</a>
      <button class="nav-hamburger" id="nav-hamburger" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="nav-bottom">
    <div class="nav-links">
      <a href="why.html">Why GoatSec</a>
      <div class="drop">
        <a href="packages.html">Packages &#9662;</a>
        <div class="dropmenu"><div class="dropmenu-inner">
          <a href="packages.html#retainer">Executive Retainer</a>
          <a href="packages.html#assessment">Assessment Sprint</a>
          <a href="packages.html#integration">Integration Sprint</a>
          <a href="packages.html#readiness">Incident Readiness</a>
          <a href="packages.html#ai">AI Governance Jumpstart</a>
        </div></div>
      </div>
      <div class="drop">
        <a href="offerings.html">Offerings &#9662;</a>
        <div class="dropmenu"><div class="dropmenu-inner">
          <a href="appsec.html">Application Security</a>
          <a href="cloud.html">Cloud &amp; Platform</a>
          <a href="ai.html">AI Security</a>
          <a href="vuln.html">Vulnerability Management</a>
          <a href="secops.html">Security Operations</a>
          <a href="grc.html">GRC &amp; Audit Readiness</a>
          <a href="strategy.html">Strategy &amp; Governance</a>
          <a href="training.html">Security Training</a>
          <a href="staff.html">Staff Augmentation</a>
        </div></div>
      </div>
      <a href="vendor.html">Vendor Enablement</a>
      <a href="smb.html">Small Business</a>
      <a href="integrations.html">Integrations</a>
      <a href="services.html">All Services</a>
      <a href="proof.html">Proof</a>
      <div class="drop">
        <a href="resources.html">Resources &#9662;</a>
        <div class="dropmenu"><div class="dropmenu-inner">
          <a href="resources.html#playbooks">Playbooks</a>
          <a href="resources.html#reporting">Reporting standards</a>
          <a href="resources.html#faq">FAQ</a>
        </div></div>
      </div>
    </div>
  </div>
</nav>

<div class="nav-drawer" id="nav-drawer">
  <div class="nav-drawer-overlay" id="nav-drawer-overlay"></div>
  <div class="nav-drawer-panel">
    <div class="nav-drawer-header">
      <img src="https://goatinfosec.files.wordpress.com/2024/02/goatsec-logo-type-horizontal.png?w=1024" alt="GoatSec" style="height:22px;opacity:.85" />
      <button class="nav-drawer-close" id="nav-drawer-close">&#x2715;</button>
    </div>
    <div class="nav-drawer-links">
      <a href="home.html">Home</a>
      <a href="why.html">Why GoatSec</a>
      <div class="nav-drawer-section">Packages</div>
      <div class="nav-drawer-sub">
        <a href="packages.html">All Packages</a>
        <a href="packages.html#retainer">Executive Retainer</a>
        <a href="packages.html#assessment">Assessment Sprint</a>
        <a href="packages.html#integration">Integration Sprint</a>
        <a href="packages.html#readiness">Incident Readiness</a>
        <a href="packages.html#ai">AI Governance Jumpstart</a>
      </div>
      <div class="nav-drawer-section">Offerings</div>
      <div class="nav-drawer-sub">
        <a href="offerings.html">All Offerings</a>
        <a href="appsec.html">Application Security</a>
        <a href="cloud.html">Cloud &amp; Platform</a>
        <a href="ai.html">AI Security</a>
        <a href="vuln.html">Vulnerability Management</a>
        <a href="secops.html">Security Operations</a>
        <a href="grc.html">GRC &amp; Audit Readiness</a>
        <a href="strategy.html">Strategy &amp; Governance</a>
        <a href="training.html">Security Training</a>
        <a href="staff.html">Staff Augmentation</a>
      </div>
      <a href="vendor.html">Vendor Enablement</a>
      <a href="smb.html">Small Business</a>
      <a href="integrations.html">Integrations</a>
      <a href="services.html">All Services</a>
      <a href="proof.html">Proof</a>
      <div class="nav-drawer-section">Resources</div>
      <div class="nav-drawer-sub">
        <a href="resources.html">Resources</a>
        <a href="resources.html#playbooks">Playbooks</a>
        <a href="resources.html#reporting">Reporting standards</a>
        <a href="resources.html#faq">FAQ</a>
      </div>
    </div>
    <div class="nav-drawer-cta">
      <a href="contact.html">Book a Scope Call</a>
    </div>
  </div>
</div>`;

const FOOTER = `
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="https://goatinfosec.files.wordpress.com/2024/02/goatsec-logo-type-horizontal.png?w=1024" alt="GoatSec" />
        <p class="footer-tagline">White-glove security execution for security leaders who want outcomes, not overhead.</p>
        <div style="margin-top:16px;display:flex;gap:10px">
          <a href="mailto:goat@goatinfosec.com" class="btn btn-sm btn-outline">goat@goatinfosec.com</a>
          <a href="tel:+15055467310" class="btn btn-sm btn-outline">505-546-7310</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="packages.html">Packages</a>
        <a href="offerings.html">Offerings</a>
        <a href="vendor.html">Vendor Enablement</a>
        <a href="integrations.html">Integrations</a>
        <a href="resources.html">Resources</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="why.html">Why GoatSec</a>
        <a href="proof.html">Proof</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h4>Get Started</h4>
        <a href="contact.html">Book a Scope Call</a>
        <a href="mailto:goat@goatinfosec.com">Email Us</a>
        <a href="tel:+15055467310">Call or Text</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&#169; 2025 GoatSec. All rights reserved.</span>
      <span>Security Outcomes Desk</span>
    </div>
  </div>
</footer>`;

document.addEventListener('DOMContentLoaded', function(){
  const n = document.getElementById('nav-slot');
  if(n) n.outerHTML = NAV;
  const f = document.getElementById('footer-slot');
  if(f) f.outerHTML = FOOTER;

  // Fix relative paths when loaded from a subdirectory (e.g. svc/)
  const depth = (location.pathname.replace(/\/[^\/]*$/, '').match(/\/[^\/]+/g) || []).length;
  const scriptDir = document.querySelector('script[src$="nav.js"]');
  const isSubdir = scriptDir && scriptDir.src.includes('../nav.js');
  if(isSubdir){
    document.querySelectorAll('nav a, .nav-drawer a, footer a').forEach(a => {
      const href = a.getAttribute('href');
      if(href && !href.startsWith('http') && !href.startsWith('mailto:') && !href.startsWith('tel:') && !href.startsWith('#') && !href.startsWith('../')){
        a.setAttribute('href', '../' + href);
      }
    });
    // Fix logo images too
    document.querySelectorAll('nav img, footer img').forEach(img => {
      // Logo is absolute URL, no fix needed
    });
  }

  // Mark active link
  const here = location.pathname.split('/').pop() || 'home.html';
  document.querySelectorAll('.nav-links a, .nav-drawer-links a').forEach(a => {
    const href = (a.getAttribute('href') || '').split('#')[0];
    if(href === here) { a.classList.add('active'); a.style.fontWeight = '650'; }
  });

  // Hamburger / drawer
  const hamburger = document.getElementById('nav-hamburger');
  const drawer    = document.getElementById('nav-drawer');
  const overlay   = document.getElementById('nav-drawer-overlay');
  const closeBtn  = document.getElementById('nav-drawer-close');

  function openDrawer(){
    drawer.classList.add('open');
    hamburger.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeDrawer(){
    drawer.classList.remove('open');
    hamburger.classList.remove('open');
    document.body.style.overflow = '';
  }

  if(hamburger) hamburger.addEventListener('click', openDrawer);
  if(overlay)   overlay.addEventListener('click', closeDrawer);
  if(closeBtn)  closeBtn.addEventListener('click', closeDrawer);

  // Close drawer on link tap
  document.querySelectorAll('.nav-drawer-links a, .nav-drawer-cta a').forEach(a => {
    a.addEventListener('click', closeDrawer);
  });

  // Close on Escape
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape') closeDrawer();
  });
});
})();
