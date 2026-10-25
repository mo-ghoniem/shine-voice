"""
Writes privacy.html from the privacy policy built into the app (MenuScreen.policy() in the app
repo), so the page and the app always say the same thing. Run after changing the app's policy:

    python tools/make_privacy.py
"""
import html
import os
import re

SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MENU = os.path.join(SITE, "..", "DFMVoiceDaemon", "app", "src", "main", "java", "com", "dfm", "voicedaemon", "MenuScreen.java")
MAIL = "support@shinevoiceofficial.com"
UPDATED_EN, UPDATED_AR = "25 October 2026", "٢٥ أكتوبر ٢٠٢٦"

STRING = r'"((?:[^"\\]|\\.)*)"'
POINT = re.compile(r"\{t\(" + STRING + r",\s*" + STRING + r"\),\s*t\(" + STRING + r",\s*" + STRING + r"\)\}", re.S)


def points():
    s = open(MENU, encoding="utf-8").read()
    start = s.index("String[][] parts = {")
    block = s[start:s.index("};", start)]
    found = POINT.findall(block)
    if not found:
        raise SystemExit("No policy points found in " + MENU)
    return [tuple(x.replace('\\"', '"') for x in p) for p in found]


def items(pts, lang):
    out = []
    for en_head, ar_head, en_body, ar_body in pts:
        head, body = (en_head, en_body) if lang == "en" else (ar_head, ar_body)
        out.append(f"    <h3>{html.escape(head)}</h3>\n    <p>{html.escape(body)}</p>")
    return "\n".join(out)


def main():
    pts = points()
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shine Voice — Privacy policy</title>
<meta name="description" content="How the Shine Voice app treats your voice, your contacts and your car's information.">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/icons/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="assets/icons/icon-192.png">
<link rel="apple-touch-icon" href="assets/icons/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=Noto+Kufi+Arabic:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=3">
</head>
<body>
<header class="nav">
  <div class="wrap">
    <a href="index.html" class="brand" style="text-decoration:none">
      <span class="brand-word"><span class="w1">Shine</span><span class="w2">VOICE</span></span>
    </a>
    <div><a href="#ar" class="lang-link" lang="ar">عربي</a><a href="index.html#download" class="btn btn-primary">Download</a></div>
  </div>
</header>

<section style="border-top:none">
  <div class="wrap prose">
    <h2>Privacy policy</h2>
    <p>This applies to the Shine Voice app for the car, in English and in Arabic. Last updated: {UPDATED_EN}.</p>
{items(pts, "en")}
    <h3>Contact</h3>
    <p>Questions about this policy or the app: <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </div>
</section>

<section id="ar" lang="ar" dir="rtl">
  <div class="wrap prose">
    <h2>سياسة الخصوصية</h2>
    <p>تنطبق هذه السياسة على تطبيق شاين للسيارة، بنسختيه العربية والإنجليزية. آخر تحديث: {UPDATED_AR}.</p>
{items(pts, "ar")}
    <h3>التواصل</h3>
    <p>للأسئلة عن هذه السياسة أو عن التطبيق: <span dir="ltr"><a href="mailto:{MAIL}">{MAIL}</a></span>.</p>
  </div>
</section>

<footer>
  <div class="wrap">
    <p>Shine Voice is an independent project, not affiliated with Dongfeng Motor.</p>
    <div class="foot-links"><a href="index.html">Home</a><a href="ar.html" lang="ar">عربي</a></div>
  </div>
  <p class="made-by" dir="ltr">Made with <span class="heart" aria-label="love">❤️</span> by Mohammed Ghoneim</p>
</footer>
</body>
</html>
"""
    open(os.path.join(SITE, "privacy.html"), "w", encoding="utf-8", newline="\n").write(page)
    print(f"privacy.html: {len(pts)} points")
    for p in pts:
        print("  -", p[0])


if __name__ == "__main__":
    main()
