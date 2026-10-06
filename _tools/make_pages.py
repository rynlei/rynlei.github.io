"""Build index.html (live) and lab.html (sandbox copy) from the content
source in _src/home.html. Run: python3 _tools/make_pages.py"""
import re, pathlib, html
root = pathlib.Path(__file__).resolve().parents[1]
src = (root/'_src'/'home.html').read_text()

def one(pattern, text, flags=re.S):
    m = re.search(pattern, text, flags); assert m, pattern[:60]; return m
def section(id_):
    return one(r'<section id="%s"[^>]*>(.*?)</section>' % id_, src).group(1)

tagline = one(r'<p class="hero-tagline">(.*?)</p>', src).group(1)
lead = 'What do altered states tell us about how the mind gives rise to consciousness?'  # lab-only hero statement
interests = re.findall(r'<li>(.*?)</li>', one(r'<ul class="interests-list">(.*?)</ul>', src).group(0))
interests = ['Altered states of consciousness' if i.startswith('Altered states of consciousness') else i for i in interests]  # lab: short form; examples live in About
cv = one(r'<a class="btn" href="([^"]+)">Download CV</a>', src).group(1)
about_ps = re.findall(r'<p>(.*?)</p>', section('about'))
highlights = re.findall(r'<div class="highlight-title">(.*?)</div>\s*<div class="highlight-meta">(.*?)</div>', section('highlights'))
news = re.findall(r'<div class="news-date">(.*?)</div>\s*<div class="news-body">(.*?)</div>', section('news'))
skills = re.findall(r'<li>(.*?)</li>', section('skills'))
footer = one(r'<footer id="contact".*?</footer>', src).group(0)

drawer_foot = '    <p class="drawer-foot">&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.<br>Experimental layout &mdash; not the live site.</p>'

def cards(id_):
    out = []
    for art in re.findall(r'<article class="project-card"[^>]*>(.*?)</article>', section(id_), re.S):
        img = one(r'<img([^>]*)>', art).group(1)
        srcm = one(r'src="([^"]+)"', img).group(1); alt = one(r'alt="([^"]*)"', img).group(1)
        photo = 'class="photo"' in img
        kicker = one(r'<p class="project-kicker">(.*?)</p>', art).group(1)
        title = one(r'<h3>(.*?)</h3>', art).group(1)
        meta = one(r'<p class="project-meta">(.*?)</p>', art).group(1)
        desc = re.sub(r'</?strong>', '', re.findall(r'<p>(.*?)</p>', art)[-1])
        cta = re.search(r'<p class="card-cta">(.*?)</p>', art, re.S)
        cta = cta.group(1) if cta else ''
        out.append(dict(src=srcm, alt=alt, photo=photo, kicker=kicker, title=title, meta=meta, desc=desc, cta=cta))
    return out
projects, pubs = cards('projects'), cards('publications')
LAB_IMG = {'assets/img/retrieved-context-thumbnail.jpg': 'assets/img/lab/rns-illustration.jpg',
           'assets/img/sleep-memory-thumbnail.jpg': 'assets/img/lab/sleep-memory-1600.jpg',
           'assets/img/hckh-program-photo.jpg': 'assets/img/lab/hckh-program-towel.webp',
           'assets/img/humour-insight-thumbnail.jpg': 'assets/img/lab/humour-insight-1500.jpg',
           'assets/img/high-mind-thumbnail.jpg': 'assets/img/lab/high-mind-900.jpg'}
for c in projects + pubs:
    if c['src'] == 'assets/img/retrieved-context-thumbnail.jpg': c['alt'] = 'Illustration of a NeuroPace RNS system implanted in a human head, with the brain shown in lavender'
    if c['src'] == 'assets/img/hckh-program-photo.jpg': c['alt'] = 'Older couple smiling in a park after exercise, towels round their necks'
    if c['src'] == 'assets/img/hckh-program-photo.jpg': c['cta'] = '<a href="project-hckh.html">View the demo <span aria-hidden="true">&rarr;</span></a> ' + c['cta'] + ' <a href="assets/pdf/DL_LOVE-2026_poster.pdf">View the poster <span aria-hidden="true">&rarr;</span></a>'
    c['src'] = LAB_IMG.get(c['src'], c['src'])

# Entries that exist only in this generator (not in _src/home.html)
pubs.append(dict(
    src='assets/img/lab/star-vection.jpg',
    alt='Two people standing inside StreetLab, a curved projection simulator showing a Toronto street scene with a fire truck',
    photo=True,
    kicker='Poster presentation',
    title='Unravelling the Relationship Between Mental Health, Vection, and Hearing Loss: A Lifespan Approach',
    meta='<em>Lei, D.</em>, Hong, L., &amp; Campos, J. L. (2026) &middot; UHN Summer Training and Research (STAR) Program Research Day',
    cta='<a href="assets/pdf/DL_STAR-2026_poster.pdf">View the poster <span aria-hidden="true">&rarr;</span></a>',
    desc=('Older adults with age-related hearing loss (ARHL) fall three times more often, and overlap between the auditory and vestibular systems may link hearing to balance. Over-reliance on vision can amplify vection, the illusory sense of self-motion, and anxiety and depression may shape that experience. Using a global visual motion paradigm, this study asks how vection differs with age, hearing status, and mental health.')))

def lead_bold(text):
    """Apple pattern: the opening statement in white, the rest in grey."""
    m = re.match(r'^(.*?[.!?])(\s+(?=[A-Z&<]).*)$', text, re.S)
    return f'<strong>{m.group(1)}</strong>{m.group(2)}' if m else f'<strong>{text}</strong>'

# About copy (overrides the paragraphs in _src/home.html).
about_ps = [
    'I am an undergraduate thesis student at the University of Toronto (St. George Campus) pursuing the Psychology Research Specialist Program and a major in Cognitive Science, advised by <a href="https://www.psych.utoronto.ca/people/directories/all-faculty/morgan-barense/">Dr. Morgan D. Barense</a>.',
    'An aspiring cognitive neuroscientist, I am interested in generating a scientific account of consciousness. Drawing on converging lines of research in psychology and the computational, clinical, and systems neurosciences, I believe consciousness is the product of a synergy between mind and body. My ultimate research aim is to use altered states of consciousness, such as psychedelic experiences, dream states, epilepsy, and mystical experiences as a vantage point from which to carve consciousness at its joints.',
    'Beyond research aspirations, I am a diligent individual with a skillset in academic writing, data analysis, and graphic design. Outside the lab, I train karate, cycle, and practice yoga. Please feel free to contact me if we share interests!',
]
# About: bold affiliation, programme and advisor, plus a few anchors of the argument.
about = []
for i, p in enumerate(about_ps):
    for k in ['University of Toronto (St. George Campus)', 'Psychology Research Specialist Program',
              'Cognitive Science', 'altered states of consciousness', 'academic writing, data analysis, and graphic design']:
        p = p.replace(k, f'<strong>{k}</strong>', 1)
    p = re.sub(r'(<a href="[^"]+">Dr\. Morgan D\. Barense</a>)', r'<strong>\1</strong>', p)
    about.append(f'        <p>{p}</p>')

def card_html(c, tag='h3'):
    media_cls = 'ap-media' if c['photo'] else 'ap-media contain'
    return f'''      <article class="project-card ap-card">
        <figure class="{media_cls}"><img src="{c['src']}" alt="{c['alt']}" loading="lazy" decoding="async"></figure>
        <div class="ap-text">
          <p class="ap-kicker">{c['kicker']}</p>
          <{tag}>{c['title']}</{tag}>
          <p class="ap-meta">{c['meta']}</p>{(chr(10) + '          <p class="ap-status">' + c['status'] + '</p>') if c.get('status') else ''}
          <p class="ap-desc">{lead_bold(c['desc'])}</p>
          {('<p class="card-cta">' + c['cta'] + '</p>') if c.get('cta') else ''}
        </div>
      </article>
'''

interests_html = '\n'.join(f'          <li>{i}</li>' for i in interests)
skills_html = '\n'.join(f'          <li>{s}</li>' for s in skills)
highlights_html = '\n'.join(f'''          <li class="highlight-item">
            <span class="ap-stat-title">{t}</span>
            <span class="ap-stat-meta">{m}</span>
          </li>''' for t, m in highlights)
# Add the award photo here once the file is in assets/img/lab, e.g.
# {'August 24, 2026': ('assets/img/lab/osnc-award.jpg', 'Darin Lei receiving the Best Undergraduate Poster Presentation certificate at OSNC 2026')}
NEWS_IMG = {'August 24, 2026': ('assets/img/lab/osnc-award.jpg', 'Darin Lei receiving the Best Undergraduate Poster Presentation certificate at OSNC 2026'),
            'February 5, 2026': ('assets/img/lab/love-poster.jpg', 'Darin Lei standing beside the HippoCamera Knowledge Hub poster at the L.O.V.E. Conference 2026')}
# Additional news items (date, body), merged with those in _src/home.html in date order
LAB_NEWS = [('February 5, 2026', 'I had the lovely opportunity to present a research poster at the <strong>2026 Lake Ontario Visionary Establishment (L.O.V.E) Conference</strong>. My poster was an update on the HippoCamera Educational Modules program &mdash; a project that aims to equip older adults with the knowledge and skills necessary to stave off cognitive decline. <a href="assets/pdf/DL_LOVE-2026_poster.pdf">View the poster here</a> and the <a href="https://sites.google.com/view/loveconference/home">conference website</a> for details.')]
from datetime import datetime
news = sorted(news + LAB_NEWS, key=lambda x: datetime.strptime(x[0], '%B %d, %Y'), reverse=True)
def news_item(d, b):
    b = b.replace('</strong>!', '!</strong>')  # keep the exclamation inside the white emphasis
    img = NEWS_IMG.get(d)
    media = f'''
          <figure class="ap-news-media"><img src="{img[0]}" alt="{img[1]}" loading="lazy" decoding="async"></figure>''' if img else ''
    return f'''        <div class="news-item{' has-media' if img else ''}">
          <div class="ap-news-text">
            <p class="ap-date">{d}</p>
            <p class="ap-desc">{b}</p>
          </div>{media}
        </div>'''
news_html = '\n'.join(news_item(d, b) for d, b in news)


avatar = one(r'<img class="hero-avatar"[^>]*src="([^"]+)"', src).group(1)
# Hero style per output: 'split' (portrait panel) or 'avatar' (centred circle). Lab experiment: avatar.
HERO = {'live': 'split', 'lab': 'split'}
# Visible section links in the header on wide screens (the hamburger stays for phones). Lab experiment.
DESKTOP_NAV = {'live': 'apple', 'lab': 'apple'}
# The More menu: 'panel' (small dropdown under the button) or 'mega' (full-width black sheet, as Apple's global menu). Lab experiment: mega.
MORE_STYLE = {'live': 'mega', 'lab': 'mega'}
# Committee-review additions (OSNC poster card, EPIC-AT talk, CV-style skills, project status, graduation line, visible email, print stylesheet). Lab prototype.
PROTO = {'live': True, 'lab': True}
# Cloudflare Web Analytics beacon (no cookies or local storage); emitted on the live home page only
ANALYTICS = '  <!-- Cloudflare Web Analytics --><script type=\'module\' src=\'https://static.cloudflareinsights.com/beacon.min.js\' data-cf-beacon=\'{"token": "5b027d490a3f4799bf9f8fb65f310082"}\'></script><!-- End Cloudflare Web Analytics -->'  # False, True (pill), or 'apple' (thin full-width local nav)

def render(live):
    hero = HERO['live' if live else 'lab']
    proto = PROTO['live' if live else 'lab']
    experience = ''
    analytics = ('\n' + ANALYTICS) if live else ''  # live pages only, so the sandbox and classic copies do not count
    pubs_out = list(pubs)
    projects_out = [dict(c) for c in projects]
    about_out = list(about)
    footer_out = footer
    skills_block = f'''        <ul class="interests-list ap-pills">
{skills_html}
        </ul>'''
    print_link = ''
    if proto:
        osnc = dict(src='assets/img/lab/osnc-neurons.jpg', alt='Rendered neurons with glowing cell bodies against a dark background', photo=True,
            kicker='Poster presentation &middot; Best Undergraduate Poster Award',
            title='Determining the Mechanisms of Temporal Context Recovery in Autobiographical Memory with Ambulatory Intracranial Recording',
            meta='<em>Lei, D.</em>, Barense, M. D., Seger, S., Lohnas, L., &amp; Lega, B. (2026) &middot; Ontario Student Neuroscience Conference (OSNC)',
            cta='<a href="assets/pdf/DL_OSNC-2026_poster.pdf">View the poster <span aria-hidden="true">&rarr;</span></a>',
            desc='Retrieved-context theory predicts that recalling an event reinstates its temporal context, yet this has only been tested in the laboratory. This poster reports the behavioural phase of the thesis, which tests the prediction in real-world autobiographical memory with HippoCamera, and sets out the planned ambulatory intracranial recordings in patients implanted with the NeuroPace RNS system.')
        epic = dict(src='assets/img/lab/epic-at-title.webp', alt='Title slide of The HippoCamera Knowledge Hub Program talk at the AGE-WELL EPIC 2026 conference, with an older man in a cap smiling and the partner logos', photo=True,
            kicker='Conference presentation',
            title='The HippoCamera Knowledge Hub Program',
            meta='<em>Lei, D.</em>, Brachaniec, M., Hong, B., Hughes, E. C., &amp; Barense, M. D. (2026) &middot; AGE-WELL EPIC-AT 7th Annual Conference',
            cta='<a href="https://youtu.be/lrgng-rhZew">Watch the talk <span aria-hidden="true">&rarr;</span></a>',
            desc='A talk at the AGE-WELL Early Professionals, Inspired Careers in AgeTech conference on the Knowledge Hub: how the program was designed with older adults, what the interviews showed about engagement with technology-based memory tools, and where the program goes next.')
        # order: the two papers, then presentations newest first
        papers, posters = [dict(c) for c in pubs_out[:2]], pubs_out[2:]
        for c in papers: c['meta'] = c['meta'] + ', student-reviewed'
        star = [c for c in posters if 'STAR' in c['meta']]; purc = [c for c in posters if 'Undergraduate Research Community' in c['meta']]
        pubs_out = papers + [osnc] + star + [epic] + purc
        STATUS = {'assets/img/lab/rns-illustration.jpg': 'Data collection &middot; October 2026',
                  'assets/img/lab/sleep-memory-1600.jpg': 'Data collection &middot; August 2026',
                  'assets/img/lab/hckh-program-towel.webp': 'Manuscript writing &middot; August 2026'}
        for c in projects_out:
            if c['src'] in STATUS: c['status'] = STATUS[c['src']]
        about_out[0] = about_out[0].replace('</a></strong>.</p>', '</a></strong>. I expect to graduate in <strong>June 2027</strong> and am applying to <strong>PhD programmes in cognitive neuroscience</strong> for entry in autumn 2027.</p>')
        assert 'June 2027' in about_out[0]
        footer_out = footer_out.replace('    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>',
            '    <p class="footer-email"><a href="mailto:darin.lei@mail.utoronto.ca">darin.lei@mail.utoronto.ca</a></p>\n    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>')
        groups = [('Programming &amp; data analysis', 'R, Python, MATLAB, JavaScript, HTML5/CSS, jamovi, JASP, NVivo (qualitative analysis), Taguette'),
                  ('Neuroimaging', 'FSL (FEAT, FLIRT, BET, MELODIC, TBSS, FSLeyes), FreeSurfer'),
                  ('Experiment design &amp; programming', 'PsychoPy, Psychtoolbox (MATLAB), Qualtrics, Lookit, REDCap'),
                  ('Design &amp; graphics', 'Adobe Photoshop, Adobe Lightroom, Figma, Canva, Blender'),
                  ('Training &amp; certification', 'TCPS 2 CORE (research ethics); CIHR Institute of Gender and Health modules; Montreal Cognitive Assessment (MoCA) certification')]
        skills_block = '        <dl class="ap-skills">\n' + '\n'.join(f'          <div class="ap-skill"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in groups) + '\n        </dl>'
        print_link = "\n  <link rel=\"stylesheet\" href=\"assets/css/print.css?v={{ site.time | date: '%s' }}\" media=\"print\">"
        LABS = [
            ('Memory &amp; Perception Lab, University of Toronto', 'Dr. Morgan D. Barense', 'Study Lead and Thesis Student', 'May 2025 &ndash; present',
             'Thesis on temporal context recovery in autobiographical memory using HippoCamera; led the HippoCamera Knowledge Hub study with older adults, from Figma prototypes to semi-structured interviews and thematic analysis.'),
            ('Texas Computational Memory Lab, UTSW Medical Center', 'Dr. Bradley Lega', 'External Research Collaborator', 'January 2026 &ndash; present',
             'Autobiographical Interview and temporal recall dynamics in temporal lobe epilepsy patients implanted with the NeuroPace RNS system; electrode localisation in FreeSurfer; patient tutorials for RNS data syncing in HippoCamera.'),
            ('Levine Lab, Rotman Research Institute, Baycrest', 'Dr. Brian Levine', 'Individual Research Project Student', 'January 2026 &ndash; present',
             'Sleep, targeted memory reactivation and the free recall of a naturalistic experience, using a controlled hospital tour as the memory paradigm.'),
            ('KITE Research Institute, University Health Network', 'Dr. Jennifer L. Campos', 'Summer Research Project Student', 'May &ndash; August 2026',
             'Vection, hearing loss and mental health across the lifespan, using a global visual motion paradigm in the StreetLab simulator.'),
        ]
        exp_rows = '\n'.join(f'''          <li class="ap-exp-item">
            <div class="ap-exp-head"><span class="ap-exp-lab">{lab}</span><span class="ap-exp-when">{when}</span></div>
            <p class="ap-exp-role"><span class="ap-exp-title">{role}</span> &middot; <span class="ap-exp-pi">{pi}</span></p>
            <p class="ap-exp-desc">{desc}</p>
          </li>''' for lab, pi, role, when, desc in LABS)
        experience = f'''
    <section id="experience" class="section ap-card">
      <div class="ap-text">
        <p class="ap-kicker">Training</p>
        <h2>Research Experience</h2>
        <ul class="ap-exp">
{exp_rows}
        </ul>
      </div>
    </section>
'''
    nav = ''; hdr_cls = 'site-header'; navjs = ''; mega = ''
    if DESKTOP_NAV['live' if live else 'lab'] == 'apple' and MORE_STYLE['live' if live else 'lab'] == 'mega':
        mega = f'''
  <div class="mega-scrim" aria-hidden="true"></div>
  <div id="site-mega" class="mega" aria-hidden="true">
    <div class="mega-inner">
      <div class="mega-col mega-col-lead">
        <p class="mega-label">More</p>
        {'<a href="#experience">Research Experience</a>' + chr(10) + '        ' if proto else ''}<a href="#skills">Technical Skills</a>
        <a href="#contact">Contact</a>
      </div>
      <div class="mega-col">
        <p class="mega-label">Get in touch</p>
        <a href="mailto:darin.lei@mail.utoronto.ca">Email</a>
        <a href="https://www.linkedin.com/in/darin-lei/">LinkedIn</a>
        <a href="https://www.researchgate.net/profile/Darin-Lei">ResearchGate</a>
        <a href="https://scholar.google.ca/citations?user=8aW8a2gAAAAJ&amp;hl=en">Google Scholar</a>{chr(10) + '        <a href="https://orcid.org/0009-0009-2868-4305">ORCID</a>' if proto else ''}
      </div>
      <div class="mega-col">
        <p class="mega-label">Elsewhere</p>
        <a href="project-hckh.html">HippoCamera Knowledge Hub</a>
        <a href="{cv}">Curriculum vitae (PDF{', September 2026' if proto else ''})</a>
      </div>
    </div>
  </div>'''
    mode = DESKTOP_NAV['live' if live else 'lab']
    if mode:
        links = ''.join(f'<a href="#{h}">{l}</a>' for h, l in [('about','About'),('highlights','Highlights'),('news','News'),('projects','Projects'),('publications','Publications')])
        if mode == 'apple':
            hdr_cls = 'site-header nav-apple'
            is_mega = MORE_STYLE['live' if live else 'lab'] == 'mega'
            more_btn = '<button class="site-nav-more-btn" type="button" aria-haspopup="true" aria-expanded="false"' + (' aria-controls="site-mega"' if is_mega else '') + '>More <svg viewBox="0 0 12 12" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 4.5l3.5 3.5 3.5-3.5"/></svg></button>'
            if is_mega:
                links += '<div class="site-nav-more site-nav-more-mega">' + more_btn + '</div>'
            else:
                links += ('<div class="site-nav-more">' + more_btn +
                      '<div class="site-nav-panel"><a href="#skills"><span class="site-nav-panel-title">Technical Skills</span><span class="site-nav-panel-sub">Tools and methods</span></a>'
                      '<a href="#contact"><span class="site-nav-panel-title">Contact</span><span class="site-nav-panel-sub">Email and profiles</span></a></div></div>')
            links += f'<a class="site-nav-cta" href="{cv}">Download CV</a>'
            navjs = '\n  <script src="assets/js/nav-pill.js?v={{ site.time | date: \'%s\' }}"></script>'
        else:
            links += ''.join(f'<a href="#{h}">{l}</a>' for h, l in [('skills','Skills'),('contact','Contact')])
        nav = '\n      <nav class="site-nav" aria-label="Sections">' + links + '</nav>'
    title = 'Darin Lei' if live else 'Darin Lei &mdash; Lab'
    robots = '' if live else '<meta name="robots" content="noindex, nofollow">' + chr(10) + '  '
    df = '    <p class="drawer-foot">&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>' if live else drawer_foot
    foot = footer if live else footer.replace('    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>', '    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>' + chr(10) + '    <p class="lab-note">Experimental layout &mdash; not the live site.</p>')
    foot_out = foot.replace('    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>', '    <p class="footer-email"><a href="mailto:darin.lei@mail.utoronto.ca">darin.lei@mail.utoronto.ca</a></p>\n    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>') if proto else foot
    if proto:
        orcid = '''      <a href="https://orcid.org/0009-0009-2868-4305" title="ORCID">
        <svg class="contact-icon" viewBox="0 0 256 256" fill="currentColor" aria-hidden="true">
          <path d="M128 0C57.3 0 0 57.3 0 128s57.3 128 128 128 128-57.3 128-128S198.7 0 128 0zm0 232C70.6 232 24 185.4 24 128S70.6 24 128 24s104 46.6 104 104-46.6 104-104 104zM86.3 186.2H70.9V79.1h15.4v107.1zM78.6 66.9c-5.8 0-10.5-4.7-10.5-10.5s4.7-10.5 10.5-10.5 10.5 4.7 10.5 10.5-4.7 10.5-10.5 10.5zM108.9 79.1h41.6c39.6 0 57 28.3 57 53.6 0 27.5-21.5 53.6-56.8 53.6h-41.8V79.1zm15.4 93.3h24.5c34.9 0 42.9-26.5 42.9-39.7 0-21.5-13.7-39.7-43.7-39.7h-23.7v79.4z"/>
        </svg>
      </a>
'''
        foot_out = foot_out.replace('    </div>\n    <p class="footer-email">', orcid + '    </div>\n    <p class="footer-email">', 1)
        assert 'orcid.org' in foot_out
        foot_out = foot_out.replace('    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>', "    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages. Last updated {{ site.time | date: '%B %Y' }}.</p>", 1)
    page = f'''---
layout: null
title: {'Darin Lei' if live else 'Darin Lei (Lab)'}
permalink: {'/' if live else '/lab.html'}
---
<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__revealReady){{document.documentElement.classList.add('reveal-all');}}}},4000);</script>
  {robots}<title>{title}</title>
  <meta name="description" content="Darin Lei, Honours BSc candidate at the University of Toronto, researching consciousness, autobiographical memory and altered states with Dr. Morgan D. Barense.">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="Darin Lei">
  <meta property="og:description" content="Honours BSc candidate at the University of Toronto, researching consciousness, autobiographical memory and altered states with Dr. Morgan D. Barense.">
  <meta property="og:url" content="https://rynlei.github.io/{'' if live else 'lab.html'}">
  <meta property="og:image" content="https://rynlei.github.io/assets/img/og-home.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="favicon.ico?v={{{{ site.time | date: '%s' }}}}" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png?v={{{{ site.time | date: '%s' }}}}">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/img/favicon-16.png?v={{{{ site.time | date: '%s' }}}}">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png?v={{{{ site.time | date: '%s' }}}}">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/img/apple-touch-icon.png?v={{{{ site.time | date: '%s' }}}}">

  <link rel="stylesheet" href="assets/css/onepage.css?v={{{{ site.time | date: '%s' }}}}">
  <link rel="stylesheet" href="assets/css/lab.css?v={{{{ site.time | date: '%s' }}}}">{print_link}
</head>
<body{' class="proto"' if proto else ''}>

  <header class="{hdr_cls}">
    <div class="site-header-inner">
      <button class="menu-toggle" type="button" aria-controls="site-drawer" aria-expanded="false" aria-label="Open menu">
        <span class="menu-toggle-icon"><span></span><span></span><span></span></span>
      </button>
      <a class="brand brand-mark" href="#home">Darin Lei</a>{nav}
    </div>
  </header>{mega}

  <div class="drawer-scrim" aria-hidden="true"></div>
  <aside id="site-drawer" class="drawer drawer-full" aria-hidden="true">
    <p class="drawer-label">Menu</p>
    <nav class="drawer-nav" aria-label="Site">
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="#highlights">Highlights</a>{chr(10) + '      <a href="#experience">Research Experience</a>' if proto else ''}
      <a href="#news">News</a>
      <a href="#projects">Ongoing Projects</a>
      <a href="#publications">Publications</a>
      <a href="#skills">Skills</a>
      <a href="#contact">Contact</a>
    </nav>
{df}
  </aside>

  <main class="ap">
    <section id="home" class="hero ap-hero ap-hero-dark {'ap-hero-split' if hero == 'split' else 'ap-hero-centre'}">
      {'<figure class="ap-media ap-hero-media"><img src="assets/img/lab/hero-seated.jpg" alt="Darin Lei seated by a window in a wood-panelled hallway" fetchpriority="high"></figure>' if hero == 'split' else '<img class="ap-avatar" src="' + avatar + '" alt="Portrait of Darin Lei" width="160" height="160" fetchpriority="high">'}
      <div class="ap-text">
        <h1>Darin Lei</h1>
        <p class="ap-tagline">{tagline}</p>
        <p class="ap-desc">{lead_bold(lead)}</p>
        <p class="ap-kicker">Research interests</p>
        <ul class="ap-pills">
{interests_html}
        </ul>
        <div class="ap-actions">
          <a class="ap-btn" href="#projects">View Projects</a>
          <a class="ap-btn ap-btn-ghost" href="{cv}">Download CV</a>
        </div>
      </div>
    </section>

    <section id="about" class="section ap-card">
      <figure class="ap-media ap-about-media"><img src="assets/img/lab/about-mri.jpg" alt="Colour-mapped sagittal MRI of a human head" loading="lazy" decoding="async"></figure>
      <div class="ap-text">
        <h2>About</h2>
        <div class="ap-desc">
{chr(10).join(about_out)}
        </div>
      </div>
    </section>

    <section id="highlights" class="section ap-card">
      <div class="ap-text">
        <p class="ap-kicker">Recognition</p>
        <h2>Highlights</h2>
        <ul class="ap-stats">
{highlights_html}
        </ul>
        <p class="section-cta"><a href="{cv}">Download the full CV{' (September 2026)' if proto else ''} <span aria-hidden="true">&rarr;</span></a></p>
      </div>
    </section>
{experience}
    <section id="news" class="section ap-card">
      <div class="ap-text">
        <p class="ap-kicker">Latest</p>
        <h2>News</h2>
{news_html}
        <p class="section-cta"><a href="#contact">Get in touch <span aria-hidden="true">&rarr;</span></a></p>
      </div>
    </section>

    <section id="projects" class="ap-group">
      <div class="section ap-head">
        <p class="ap-kicker">Research</p>
        <h2>Ongoing Projects</h2>
      </div>
{''.join(card_html(c) for c in projects_out)}    </section>

    <section id="publications" class="ap-group">
      <div class="section ap-head">
        <p class="ap-kicker">Writing and talks</p>
        <h2>Selected Publications and Presentations</h2>
      </div>
{''.join(card_html(c) for c in pubs_out)}    </section>

    <section id="skills" class="section ap-card">
      <div class="ap-text">
        <p class="ap-kicker">Tools</p>
        <h2>Technical Skills</h2>
{skills_block}
      </div>
    </section>

  </main>

{foot_out}
  <a href="#home" class="to-top" aria-label="Back to top"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg></a>
  <script src="assets/js/site.js?v={{{{ site.time | date: '%s' }}}}"></script>
  <script src="assets/js/lab-top.js?v={{{{ site.time | date: '%s' }}}}"></script>{navjs}{analytics}
</body>
</html>
'''
    return page

for live, name in ((True, 'index.html'), (False, 'lab.html')):
    page = render(live)
    (root/name).write_text(page)
    print(name, 'written', len(page.splitlines()), 'lines;', len(projects), 'projects', len(pubs), 'publications', len(about), 'about paragraphs')

# classic.html: the previous layout, kept viewable at /classic.html with the
# same content source, so it stays accurate without being the home page.
classic = src.replace('title: Darin Lei\npermalink: /\n', 'title: Darin Lei (Classic)\npermalink: /classic.html\n', 1)
classic = classic.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">',
                          '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="robots" content="noindex, nofollow">', 1)
classic = classic.replace('<title>Darin Lei</title>', '<title>Darin Lei &mdash; Classic layout</title>', 1)
classic = classic.replace('    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>',
                          '    <p>&copy; Copyright 2026 Darin Lei. Hosted by GitHub Pages.</p>\n    <p>Previous layout, kept for reference. <a href="index.html">Go to the current site</a>.</p>', 1)
assert classic != src and 'noindex' in classic and 'classic.html' in classic and 'Classic layout' in classic and 'Previous layout' in classic
(root/'classic.html').write_text(classic)
print('classic.html written', len(classic.splitlines()), 'lines')
