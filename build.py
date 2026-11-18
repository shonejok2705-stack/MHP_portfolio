"""Run after editing index.html or en.json:  python3 build.py
Writes: SEO <head> block of index.html, en/index.html, sitemap.xml, robots.txt, llms.txt
"""
import json, re, html, datetime, pathlib

SITE = "https://lutrinae.example.com"  # ponytail: set your real domain here, then re-run (previews need absolute URLs)

ROOT = pathlib.Path(__file__).parent
EN = json.loads((ROOT / 'en.json').read_text(encoding='utf-8'))
SOCIAL = ["https://www.facebook.com/share/18yx4XnLXg/", "https://www.instagram.com/lutrinae27",
          "https://www.tiktok.com/@otterlutrinae", "https://www.threads.com/@lutrinae27"]
PRICES = [("Chụp ảnh chân dung", "Portrait photography", 199000),
          ("Book chụp theo màu", "Colour-themed shoot", 249000),
          ("Chụp sự kiện & kỷ yếu", "Events & yearbooks", 499000)]

META = {
 'vi': dict(url=f"{SITE}/", locale="vi_VN", img="img/og-vi.jpg",
   title="Lutrinae | Chụp ảnh chân dung, kỷ yếu giá HSSV & Lập trình IoT tại TP.HCM",
   desc="Lutrinae: nhiếp ảnh gia & lập trình viên IoT tại TP.HCM. Chụp ảnh chân dung, áo dài, kỷ yếu, sự kiện, book chụp theo màu giá sinh viên chỉ từ 199.000đ. Hỗ trợ đồ án IoT ESP32, Arduino.",
   img_alt="Lutrinae: chụp ảnh chân dung, kỷ yếu giá HSSV và lập trình IoT tại TP.HCM",
   keywords="Lutrinae, chụp ảnh TP.HCM, chụp ảnh Sài Gòn, thợ chụp ảnh TP.HCM, nhiếp ảnh gia TP.HCM, chụp ảnh chân dung, chụp ảnh chân dung giá rẻ, chụp ảnh profile, chụp ảnh áo dài, chụp ảnh Tết, chụp ảnh kỷ yếu, chụp kỷ yếu giá sinh viên, chụp ảnh tốt nghiệp, chụp ảnh sự kiện, chụp ảnh giá HSSV, chụp ảnh sinh viên, book chụp theo màu, chụp ảnh concept, chụp ảnh đường phố, photographer Sài Gòn, lập trình IoT, đồ án IoT, đồ án IoT sinh viên, ESP32, Arduino, nhà thông minh, lập trình viên TP.HCM, Đại học Gia Định",
   service="Dịch vụ chụp ảnh Lutrinae", job="Nhiếp ảnh gia & Lập trình viên IoT", univ="Đại học Gia Định", city="TP. Hồ Chí Minh"),
 'en': dict(url=f"{SITE}/en/", locale="en_US", img="img/og-en.jpg",
   title="Lutrinae | Portrait, Yearbook & Student Photography + IoT Development in Ho Chi Minh City",
   desc="Lutrinae: photographer & IoT developer in Ho Chi Minh City (Saigon). Portrait, áo dài, yearbook, event and colour-themed photo shoots at student prices from 199,000đ. ESP32 & Arduino IoT projects.",
   img_alt="Lutrinae: portrait & yearbook photography at student prices and IoT development in Ho Chi Minh City",
   keywords="Lutrinae, photographer Ho Chi Minh City, Saigon photographer, portrait photographer Saigon, áo dài photo shoot, yearbook photography Vietnam, graduation photos Saigon, event photographer HCMC, student photo shoot price, colour-themed photo shoot, affordable photographer Vietnam, IoT developer Vietnam, ESP32, Arduino, student IoT project, smart home, Gia Dinh University",
   service="Lutrinae Photography", job="Photographer & IoT Developer", univ="Gia Dinh University", city="Ho Chi Minh City"),
}

def strip(t): return html.unescape(re.sub(r'<[^>]+>', '', t)).strip()

def head(lang, page):
    m = META[lang]; e = lambda t: html.escape(t, quote=True)
    faq = [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
           for q, a in re.findall(r'<span class="q">.*?</svg></span>(.*?)</span>.*?<p class="ans">(.*?)</p>', page)]
    person = {"@type": "Person", "@id": f"{SITE}/#person", "name": "Lutrinae", "alternateName": "Mai Hồng Phúc",
              "jobTitle": m['job'], "image": f"{SITE}/img/p6.avif", "url": m['url'], "sameAs": SOCIAL,
              "affiliation": {"@type": "CollegeOrUniversity", "name": m['univ']},
              "address": {"@type": "PostalAddress", "addressLocality": m['city'], "addressCountry": "VN"},
              "knowsAbout": ["Portrait photography", "Yearbook photography", "Event photography", "Áo dài photography",
                             "Internet of Things", "ESP32", "Arduino", "C/C++", "Python", "Adobe Photoshop", "Adobe Premiere Pro",
                             "Adobe After Effects", "Adobe InDesign", "Alight Motion"]}
    service = {"@type": "ProfessionalService", "@id": f"{SITE}/#service", "name": m['service'], "url": m['url'],
               "image": f"{SITE}/{m['img']}", "founder": {"@id": f"{SITE}/#person"}, "sameAs": SOCIAL,
               "priceRange": "199.000đ – 499.000đ", "currenciesAccepted": "VND",
               "address": {"@type": "PostalAddress", "addressLocality": m['city'], "addressRegion": "Hồ Chí Minh", "addressCountry": "VN"},
               "areaServed": {"@type": "City", "name": m['city']},
               "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": vi if lang == 'vi' else en},
                               "priceSpecification": {"@type": "PriceSpecification", "minPrice": p, "priceCurrency": "VND"},
                               "eligibleCustomerType": "Student"} for vi, en, p in PRICES]}
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Lutrinae", "inLanguage": ["vi", "en"], "publisher": {"@id": f"{SITE}/#person"}},
        {"@type": "ProfilePage", "url": m['url'], "name": m['title'], "description": m['desc'], "inLanguage": lang,
         "isPartOf": {"@id": f"{SITE}/#website"}, "mainEntity": {"@id": f"{SITE}/#person"}, "primaryImageOfPage": f"{SITE}/{m['img']}"},
        person, service, {"@type": "FAQPage", "inLanguage": lang, "mainEntity": faq}]}
    up = '../' if lang == 'en' else ''
    icon = "data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230071e3'/%3E%3Ctext x='32' y='45' font-family='Arial' font-weight='700' font-size='38' fill='white' text-anchor='middle'%3EL%3C/text%3E%3C/svg%3E"
    return f'''<!-- SEO (generated by build.py, edit there) -->
<title>{e(m['title'])}</title>
<meta name="description" content="{e(m['desc'])}">
<meta name="keywords" content="{e(m['keywords'])}">
<meta name="author" content="Lutrinae">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="geo.region" content="VN-SG"><meta name="geo.placename" content="{e(m['city'])}">
<meta name="theme-color" content="#f5f5f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{m['url']}">
<link rel="alternate" hreflang="vi" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<link rel="icon" href="{icon}">
<link rel="apple-touch-icon" href="{up}img/og-{lang}.jpg">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Lutrinae">
<meta property="og:title" content="{e(m['title'])}">
<meta property="og:description" content="{e(m['desc'])}">
<meta property="og:url" content="{m['url']}">
<meta property="og:locale" content="{m['locale']}">
<meta property="og:locale:alternate" content="{META['en' if lang == 'vi' else 'vi']['locale']}">
<meta property="og:image" content="{SITE}/{m['img']}">
<meta property="og:image:secure_url" content="{SITE}/{m['img']}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(m['img_alt'])}">
<meta property="profile:username" content="lutrinae27">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(m['title'])}">
<meta name="twitter:description" content="{e(m['desc'])}">
<meta name="twitter:image" content="{SITE}/{m['img']}">
<meta name="twitter:image:alt" content="{e(m['img_alt'])}">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
<!-- /SEO -->'''

def set_head(page, lang):
    return re.sub(r'<!-- SEO.*?<!-- /SEO -->', lambda _: head(lang, page), page, count=1, flags=re.S)

def translate(page):
    def text(m):
        key = ' '.join(html.unescape(m.group(2)).split())
        return m.group(1) + m.group(2).replace(m.group(2).strip(), html.escape(EN[key], quote=False)) + '<' if key in EN else m.group(0)
    def attr(m):
        v = html.unescape(m.group(2))
        return f'{m.group(1)}="{html.escape(EN[v])}"' if v in EN else m.group(0)
    a, b = page.index('<body'), page.index('</body>')
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', page[a:b], flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(>)([^<]+)<', text, parts[i])
        parts[i] = re.sub(r'\b(alt|aria-label|title)="([^"]*)"', attr, parts[i])
    return page[:a] + ''.join(parts) + page[b:]

vi = (ROOT / 'index.html').read_text(encoding='utf-8')
vi = set_head(vi, 'vi')
(ROOT / 'index.html').write_text(vi, encoding='utf-8')

en = translate(vi).replace('<html lang="vi">', '<html lang="en">', 1)
en = re.sub(r'(src|poster)="img/', r'\1="../img/', en)
en = en.replace('<a class="lang-btn" href="en/" hreflang="en"', '<a class="lang-btn" href="../" hreflang="vi"', 1)
en = set_head(en, 'en')
(ROOT / 'en').mkdir(exist_ok=True)
(ROOT / 'en' / 'index.html').write_text(en, encoding='utf-8')

left = sorted({' '.join(t.split()) for t in re.findall(r'>([^<]*[ăâđêôơưáàảãạéèẻẽẹíìỉĩịóòỏõọúùủũụýỳỷỹỵ][^<]*)<', re.sub(r'<(script|style)\b.*?</\1>', '', en[en.index('<body'):], flags=re.S), re.I)})
left = [t for t in left if html.unescape(t) not in EN.values() and t != 'đ']  # áo dài / đ stay Vietnamese on purpose
if left: print('untranslated (add to en.json):', *left, sep='\n  ')

today = datetime.date.today().isoformat()
alts = '\n'.join(f'    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>' for h, u in [('vi', f'{SITE}/'), ('en', f'{SITE}/en/'), ('x-default', f'{SITE}/')])
urls = ''.join(f'''  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n{alts}\n    <image:image><image:loc>{SITE}/{img}</image:loc></image:image>\n  </url>\n'''
               for u, img in [(f'{SITE}/', 'img/og-vi.jpg'), (f'{SITE}/en/', 'img/og-en.jpg')])
(ROOT / 'sitemap.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{urls}</urlset>
''', encoding='utf-8')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /assets/\n\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')

faq_vi = '\n'.join(f'- **{q["name"]}** {q["acceptedAnswer"]["text"]}' for q in json.loads(re.search(r'"FAQPage".*?"mainEntity": (\[.*?\])\}\]\}', head('vi', vi)).group(1)))
(ROOT / 'llms.txt').write_text(f'''# Lutrinae

> Lutrinae is a photographer and IoT developer in Ho Chi Minh City (Saigon), Vietnam, and an Information Technology (IoT) student at Gia Dinh University. Offers portrait, áo dài, yearbook, event and colour-themed photo shoots at student prices, plus small IoT / ESP32 / Arduino projects.

- Vietnamese site: {SITE}/
- English site: {SITE}/en/

## Services & starting prices (student rates, VND, reference only)
''' + ''.join(f'- {en}: from {p:,}đ\n' for _, en, p in PRICES) + f'''
Prices exclude venue, outfits, make-up and travel outside Ho Chi Minh City. Exact quote after a chat.

## Contact (direct message)
''' + ''.join(f'- {u}\n' for u in SOCIAL) + f'''
## FAQ (Vietnamese)
{faq_vi}
''', encoding='utf-8')
print('built', SITE)
