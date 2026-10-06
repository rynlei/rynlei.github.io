"""Generate project-hckh.html (HippoCamera Knowledge Hub demo page) from
index.html's chrome plus the section script below. Run after make_pages.py:
python3 _tools/make_project_hckh.py"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
lab = (ROOT / 'index.html').read_text()
def one(p, s, flags=re.S):
    m = re.search(p, s, flags); assert m, p; return m
header = one(r'<header class="site-header[^"]*">.*?</header>', lab).group(0)
drawer = one(r'<div class="drawer-scrim".*?</aside>', lab).group(0)
footer = one(r'<footer id="contact".*?</footer>', lab).group(0)
for frag in ('header', 'drawer'):
    pass
header = header.replace('href="#home"', 'href="index.html"')
# Page-local row (Apple's product-page bar): this page's own sections, so the
# current-section highlight works here. The home page's sections move to the
# More sheet, where leaving the page belongs.
ROW = [('program', 'Program'), ('expect', 'Memory'), ('cues', 'Cues'), ('practice', 'Activity'), ('prototype', 'Prototype')]
MORE_HERE = [('normal', 'Brain Changes'), ('worried', 'Factsheets'), ('numbers', 'Educational Graphs'), ('habits', 'Memory Strategies'), ('quiz', 'Optional Quizzes &amp; Activities'), ('study', 'The Study')]
HOME = [('index.html', 'Home'), ('index.html#about', 'About'), ('index.html#experience', 'Research Experience'), ('index.html#projects', 'Projects'), ('index.html#publications', 'Publications'), ('index.html#contact', 'Contact')]
row_links = ''.join(f'<a href="#{h}">{l}</a>' for h, l in ROW)
header = re.sub(r'(<nav class="site-nav" aria-label="Sections">).*?(<div class="site-nav-more)', lambda m_: m_.group(1) + row_links + m_.group(2), header, flags=re.S)
assert '#program' in header and 'index.html#about' not in header
m = re.search(r'\n  <div class="mega-scrim".*?\n  </div>', lab, re.S)
mega = m.group(0) if m else ''
if mega:
    col1 = '      <div class="mega-col mega-col-lead">\n        <p class="mega-label">On this page</p>\n' + ''.join(f'        <a href="#{h}">{l}</a>\n' for h, l in MORE_HERE) + '      </div>'
    col2 = '      <div class="mega-col">\n        <p class="mega-label">Darin Lei</p>\n' + ''.join(f'        <a href="{h}">{l}</a>\n' for h, l in HOME) + '      </div>'
    cols = re.findall(r'      <div class="mega-col[^"]*">.*?      </div>', mega, re.S)
    assert len(cols) == 3, len(cols)
    contact = cols[1]
    mega = mega.replace(cols[0], col1).replace(cols[1], contact).replace(cols[2], col2)
    mega = re.sub(r'href="#([a-z]+)"(?![^<]*</a>\s*\n\s*(?:<a|</div>))', r'href="#\1"', mega)  # keep page anchors as they are
# Phone menu: this page's sections first, then a Home group
nav_here = ''.join(f'      <a href="#{h}">{l}</a>\n' for h, l in ROW + MORE_HERE)
nav_home = ''.join(f'      <a href="{h}" class="drawer-home">{l}</a>\n' for h, l in HOME)
drawer = re.sub(r'(<nav class="drawer-nav" aria-label="Site">\n).*?(    </nav>)', lambda m_: m_.group(1) + '      <p class="drawer-group">HippoCamera Knowledge Hub</p>\n' + nav_here + '      <p class="drawer-group">Darin Lei</p>\n' + nav_home + m_.group(2), drawer, flags=re.S)
assert '#program' in drawer and 'index.html#about' in drawer
drawer = drawer.replace('Experimental layout &mdash; not the live site.', 'Experimental project page &mdash; not the live site.')
footer = footer.replace('Experimental layout &mdash; not the live site.', 'Experimental project page &mdash; not the live site.')

FIGMA_Q = 'node-id=2337-12057&amp;starting-point-node-id=2337%3A12057&amp;scaling=contain&amp;content-scaling=fixed&amp;hide-ui=1'
FIGMA_URL = 'https://embed.figma.com/proto/hMAkEa91MlfOQwQvwNAjlJ/HippoCamera-Knowledge-Hub---Winter-2025?' + FIGMA_Q + '&amp;embed-host=share'
FIGMA_FULL = 'https://www.figma.com/proto/hMAkEa91MlfOQwQvwNAjlJ/HippoCamera-Knowledge-Hub---Winter-2025?' + FIGMA_Q
IMG = 'assets/img/lab/hckh/'
TALL = {'maintain-memory.png', 'hub-list.png', 'memory-changes.png', 'memory-in-old-age.png', 'abnormal-vs-normal.png', 'should-i-be-worried.png', 'normal-aging.png', 'distinctive-cues.png', 'creating-cues.png', 'speaking-of-unique.png'}
def phone(file, cap, alt):
    scroll = file in TALL
    cls = ' is-scroll' if scroll else ''
    return (f'<div class="hk-phone{cls}"><div class="hk-ph-wrap"><div class="hk-ph{cls}"' + (' tabindex="0"' if scroll else '') +
            f'><img src="{IMG}{file}" alt="{alt}" loading="lazy" decoding="async"></div></div>'
            f'<p class="hk-cap">{cap}</p></div>')
def section(id_, kicker, h2, desc, phones, side=False):
    n = len(phones)
    ph = ''.join('\n        ' + p for p in phones)
    cls = 'section ap-card hk-sec' + (' hk-side' if side else '')
    return f'''
    <section id="{id_}" class="{cls}">
      <div class="ap-text">
        <p class="ap-kicker">{kicker}</p>
        <h2>{h2}</h2>
        <p class="ap-desc">{desc}</p>
      </div>
      <div class="hk-phones" data-n="{n}">{ph}
      </div>
    </section>'''

S = []
S.append(section('program', 'Knowledge Hub', 'A library, not a leaflet.',
  'Articles and strategies of ten to fifteen minutes each, from the memory changes of older adulthood to the cue-based science behind HippoCamera itself. <strong>Readers choose what they need and go at their own pace.</strong>',
  [phone('hub-landing.png', 'Knowledge Hub', 'Knowledge Hub landing screen asking “Are you interested in memory science?” with a Start exploring button'),
   phone('hub-list.png', 'Articles and strategies', 'Scrolling list of Knowledge Hub cards: Our Memory Function in Older Adulthood, How Distinctive Cues Can Bolster Our Memory, and more')]))
S.append(section('expect', 'Memory in old age', 'It starts by saying what to expect.',
  'Every article opens with an overview and a map of what it covers, <strong>so readers know where they are going before they start.</strong>',
  [phone('memory-in-old-age.png', 'Article opener', 'Article opener titled Memory in Old Age with an overview in bullet points'),
   phone('article-outline.png', 'What the article covers', 'Outline screen “How does our memory change?” listing Normal Changes, Abnormal Changes, Maintaining Memory and Activity')]))
S.append(section('normal', 'Normal aging', 'Most forgetting is normal.',
  'Misplaced keys, a name on the tip of the tongue, a word that will not come. <strong>The program names these for what they are: part of normal aging, and no cause for concern.</strong>',
  [phone('normal-aging.png', 'Normal aging', 'Normal Aging screen with a brain-and-tree illustration and examples such as forgetting where you put your car keys')], side=True))
S.append(section('worried', 'Should I be worried?', 'A guide, not a diagnosis.',
  'One comparison carries the distinction. Forgetting where the car keys are is normal; forgetting how to drive is a sign of concern. <strong>Normal aging is mild and does not affect daily life. Dementia affects the ability to live independently.</strong>',
  [phone('should-i-be-worried.png', 'Normal aging vs sign of concern', 'Should I be worried? screen comparing “You can’t find your car keys” with “You can’t remember how to drive” and a key takeaway box')], side=True))
S.append(section('numbers', 'The numbers', 'Figures that reassure rather than alarm.',
  'Almost 40% of us will notice some memory loss after 65, yet only 5 to 8% of people over 60 might live with dementia. <strong>And not everything declines: speed and working memory fall with age, while world knowledge keeps growing.</strong>',
  [phone('abnormal-vs-normal.png', 'How common is dementia?', 'Abnormal versus Normal Memory Changes screen with a ring chart reading 5–8% of people over 60 might live with dementia'),
   phone('memory-changes.png', 'What changes with age', 'Memory Changes Over Time screen with a graph of world knowledge, working memory, episodic memory and speed of processing across the lifespan')]))
S.append(section('habits', 'Maintaining memory', 'Four habits anyone can start.',
  'Healthy diet, physical exercise, learning new things, staying socially active. <strong>Each is explained in a paragraph, with a reason to believe it.</strong>',
  [phone('maintain-memory.png', 'How can I maintain my memory?', 'How can I maintain my memory? screen with four numbered tips, each with a photograph: healthy diet, physical exercise, learn new things, stay socially active')], side=True))
S.append(section('cues', 'Distinctive cues', 'Then it teaches the app itself.',
  'HippoCamera asks people to record short cues for the moments they want to keep. <strong>The program explains why distinctive cues work, what makes a cue your own, and how to make one.</strong>',
  [phone('distinctive-cues.png', 'Why cues work', 'Distinctive Cues article opener with a monarch butterfly photograph and an overview'),
   phone('speaking-of-unique.png', 'Unique to you', 'Speaking of unique: a butterfly illustration and text explaining that distinctive cues reflect your personal experiences'),
   phone('creating-cues.png', 'How to make one', 'Creating Cues screen, tip 1: capture specific visuals that make it unique, with a photograph of a dog on a walk')]))
S.append(section('practice', 'Activity', 'Then it asks you to try.',
  'A short video of a moment worth keeping, then a choice of cues to go with it. <strong>Readers practise picking the cue that captures the moment best.</strong>',
  [phone('activity.png', 'Watch, then choose', 'Activity screen inviting the reader to watch a video of a dog playing with a garden hose, then choose the audio cue that suits it best')], side=True))
S.append(section('quiz', 'Check your understanding', 'Optional quizzes, instant feedback.',
  'A scenario, three answers, and a response that explains why. <strong>Readers can answer or skip, and the feedback repeats the lesson rather than only marking it right or wrong.</strong>',
  [phone('quiz.png', 'Scenario', 'Check Your Understanding quiz about Rachael forgetting a new acquaintance’s name, with three options and Continue and Skip buttons'),
   phone('quiz-answered.png', 'Choose an answer', 'The same quiz with an option selected and a Done button'),
   phone('quiz-feedback.png', 'Feedback', 'Feedback sheet reading “Right on!” explaining that forgetting an acquaintance’s name is a normal memory change')]))

embed = ''
if FIGMA_URL:
    embed = f'''
    <section id="prototype" class="section ap-card hk-sec">
      <div class="ap-text">
        <p class="ap-kicker">Prototype</p>
        <h2>Try it yourself.</h2>
        <p class="ap-desc">The program as an interactive Figma prototype. <strong>Tap through it the way a user would.</strong></p>
      </div>
      <div class="hk-embed" data-figma="{FIGMA_URL}">
        <button class="hk-embed-poster" type="button" aria-label="Open the interactive prototype">
          <span class="hk-embed-phone"><img src="{IMG}hub-landing.png" alt="" loading="lazy" decoding="async"></span>
          <span class="hk-embed-cta">Open the prototype</span>
          <span class="hk-embed-note">Loads Figma&rsquo;s viewer</span>
        </button>
      </div>
      <p class="hk-embed-full"><a href="{FIGMA_FULL}" target="_blank" rel="noopener">Open full screen in Figma <span aria-hidden="true">&nearr;</span></a></p>
    </section>'''

closing = '''
    <section id="study" class="section ap-card hk-close">
      <div class="ap-text">
        <p class="ap-kicker">The study</p>
        <h2>Built from what older adults told us.</h2>
        <p class="ap-meta"><em>Lei, D.</em>, Hong, B., Hughes, E. C., &amp; Barense, M. D. (2025) &middot; Qualitative study</p>
        <p class="ap-desc"><strong>HippoCamera, a smartphone app shown to improve memory for everyday events, has driven requests for content explaining the science behind it.</strong> This project developed a complementary educational program covering key memory strategies, and interviewed older adults to identify what drives engagement with technology-based memory tools, informing how future interventions can be designed.</p>
        <div class="ap-actions">
          <a class="ap-btn hk-btn-teal" href="https://canva.link/efl2qt7o34hguq3">View the presentation</a>
          <a class="ap-btn hk-btn-teal" href="assets/pdf/DL_LOVE-2026_poster.pdf">View the poster</a>
          <a class="ap-btn hk-btn-teal" href="https://youtu.be/lrgng-rhZew">Watch the talk</a>
          <a class="ap-btn ap-btn-ghost" href="index.html#projects">Back to home</a>
        </div>
        <p class="hk-credit">Screens designed by Darin Lei, in collaboration with Ever C. Hughes, Bryan Hong and Morgan D. Barense, and shaped by feedback from older adults in the Greater Toronto Area.</p>
      </div>
    </section>'''

hero_phones = ''.join('\n        ' + p for p in [
    phone('hub-landing.png', '', 'Knowledge Hub landing screen'),
    phone('article-outline.png', '', 'Article outline screen'),
    phone('distinctive-cues.png', '', 'Distinctive Cues article opener')]).replace('<p class="hk-cap"></p>', '')
# hero phones are decorative previews; drop the scroll affordance there
hero_phones = hero_phones.replace(' is-scroll', '').replace(' tabindex="0"', '')

V = "{{ site.time | date: '%s' }}"
html = f'''---
layout: null
title: HippoCamera Knowledge Hub
permalink: /project-hckh.html
---
<!DOCTYPE html>
<html lang="en-us">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{if(!window.__revealReady){{document.documentElement.classList.add('reveal-all');}}}},4000);</script>
  <title>HippoCamera Knowledge Hub &mdash; Darin Lei</title>
  <meta name="description" content="The HippoCamera Knowledge Hub: a digital educational program on memory and healthy aging for older adults, designed by Darin Lei with the Barense Lab. Screens, prototype and poster.">
  <meta property="og:type" content="article">
  <meta property="og:title" content="HippoCamera Knowledge Hub &mdash; Darin Lei">
  <meta property="og:description" content="A digital educational program on memory and healthy aging for older adults. Screens, interactive prototype and conference poster.">
  <meta property="og:url" content="https://rynlei.github.io/project-hckh.html">
  <meta property="og:image" content="https://rynlei.github.io/assets/img/og-hckh.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="favicon.ico?v={V}" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png?v={V}">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/img/favicon-16.png?v={V}">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/img/favicon-192.png?v={V}">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/img/apple-touch-icon.png?v={V}">

  <link rel="stylesheet" href="assets/css/onepage.css?v={V}">
  <link rel="stylesheet" href="assets/css/lab.css?v={V}">
  <link rel="stylesheet" href="assets/css/project-hckh.css?v={V}">
</head>
<body>

  {header}{mega}

  {drawer}

  <main class="ap hk">
    <section id="top" class="hero ap-hero ap-hero-dark hk-hero">
      <div class="ap-text">
        <p class="ap-kicker">HippoCamera Knowledge Hub</p>
        <h1>Bite-sized memory science.</h1>
        <p class="ap-desc">A knowledge hub embedded within <a href="https://hippocamera.com">HippoCamera</a>, a smartphone app shown to improve memory for everyday events: <strong>short articles and guided activities on how memory changes with age, and how to look after it.</strong></p>
        <div class="ap-actions">
          <a class="ap-btn hk-btn-teal" href="#program">Explore the program</a>
          <a class="ap-btn ap-btn-ghost" href="index.html#projects">Back to home</a>
        </div>
      </div>
      <div class="hk-hero-phones" aria-hidden="true">{hero_phones}
      </div>
    </section>
{''.join(S)}
{embed}
{closing}
  </main>

{footer}
  <a href="#top" class="to-top" aria-label="Back to top"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 14l6-6 6 6"/></svg></a>
  <script src="assets/js/site.js?v={V}"></script>
  <script src="assets/js/lab-top.js?v={V}"></script>
  <script src="assets/js/nav-pill.js?v={V}"></script>
  <script src="assets/js/hckh-embed.js?v={V}"></script>
  <!-- Cloudflare Web Analytics --><script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "5b027d490a3f4799bf9f8fb65f310082"}}'></script><!-- End Cloudflare Web Analytics -->
</body>
</html>
'''
(ROOT / 'project-hckh.html').write_text(html)
print('project-hckh.html written', html.count('\n'), 'lines;', len(S), 'sections;', 'embed' if FIGMA_URL else 'no embed')
