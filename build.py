#!/usr/bin/env python3
"""Render the localized site from src/ templates and i18n/<locale>.json.

The templates in src/ are the English pages: readable, openable in a browser, and the
source every translation is taken from. Translatable content is marked on the element
itself and the markers are stripped from the output:

    data-i18n="key"                          the element's inner HTML is the unit
    data-i18n-attr="content:key,alt:key2"    one or more attributes of the element

Inner HTML rather than text, so inline markup (<span class="find">, <b>, &nbsp;) travels
with the sentence it belongs to instead of splitting it into fragments a translator
cannot reorder.

Output goes to the repo root: the English pages there, one directory per locale. It is
committed, so Cloudflare Pages keeps serving plain static files with no build command.

    python3 build.py            render everything
    python3 build.py --extract  refresh i18n/en.json from the templates
    python3 build.py --check    fail if the committed output is stale
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
I18N = os.path.join(ROOT, "i18n")
SITE = "https://assorta.app"

# The picker table comes from the app: tools/sync-from-app.py reads AppLanguage.kt into
# i18n/languages.json, so the native names, the flags, the RTL set and the display order are
# the app's own decisions rather than a second copy that drifts away from them. The two
# region overlays the app carries (values-es-rES, values-fr-rCA) are deltas over es and fr
# and get no row there, which is also right here: their marketing copy would be identical.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "i18n", "languages.json"),
          encoding="utf-8") as _f:
    LANGUAGES = json.load(_f)["languages"]

LOCALES = [l["tag"] for l in LANGUAGES]
LANGUAGE_NAMES = {l["tag"]: l["name"] for l in LANGUAGES}
LANGUAGE_FLAGS = {l["tag"]: l["flag"] for l in LANGUAGES}
RTL = {l["tag"] for l in LANGUAGES if l["rtl"]}

# Which pages exist in which locales. Privacy and Terms are English only - machine-translated
# terms are 30 more versions of a contract that drift from the original (docs/i18n/plan.md).
LOCALIZED_PAGES = ["index.html", "delete-account.html"]
ENGLISH_ONLY_PAGES = ["privacy.html", "terms.html"]

# Paths that live at the root and must gain a ../ inside a locale directory. Everything
# else a page links to (index.html, delete-account.html, #anchors) is local to the locale.
ROOT_PATHS = re.compile(
    r'((?:href|src)=")(favicon\.svg|favicon-32\.png|favicon-180\.png|screens/|privacy\.html|terms\.html)'
)


class TemplateError(Exception):
    pass


def close_of_open_tag(html, i):
    """Index just past the '>' of the tag opening at html[i] == '<', quotes respected."""
    quote = None
    while i < len(html):
        c = html[i]
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == ">":
            return i + 1
        i += 1
    raise TemplateError("unterminated tag")


def matching_close(html, name, start):
    """(start, end) of the </name> that closes the element whose content begins at start."""
    pattern = re.compile(r"</?" + re.escape(name) + r"(?=[\s/>])", re.I)
    depth = 1
    i = start
    while True:
        m = pattern.search(html, i)
        if not m:
            raise TemplateError("no closing </%s>" % name)
        end = close_of_open_tag(html, m.start())
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return m.start(), end
        elif html[end - 2] != "/":
            depth += 1
        i = end


def marked(html):
    """Every marked element, in document order.

    Yields (open_start, open_end, tag_name, text_key, attr_keys, inner_start, inner_end).
    text_key is None when only attributes are marked, in which case the inner span is empty.
    """
    for m in re.finditer(r'\sdata-i18n(?:-attr)?="', html):
        open_start = html.rindex("<", 0, m.start())
        open_end = close_of_open_tag(html, open_start)
        if m.start() > open_end:
            continue  # the match was in a text node, not in a tag
        tag = html[open_start:open_end]
        name = re.match(r"<([A-Za-z][\w-]*)", tag).group(1)

        text_key = None
        km = re.search(r'\sdata-i18n="([^"]+)"', tag)
        if km:
            text_key = km.group(1)

        attr_keys = {}
        am = re.search(r'\sdata-i18n-attr="([^"]+)"', tag)
        if am:
            for pair in am.group(1).split(","):
                attr, _, key = pair.strip().partition(":")
                if not attr or not key:
                    raise TemplateError("bad data-i18n-attr: %r" % am.group(1))
                attr_keys[attr] = key

        if text_key is None:
            inner_start = inner_end = open_end
        else:
            if tag.rstrip().endswith("/>"):
                raise TemplateError("data-i18n on a self-closing <%s>" % name)
            inner_start = open_end
            inner_end = matching_close(html, name, open_end)[0]

        yield open_start, open_end, name, text_key, attr_keys, inner_start, inner_end


def _dedupe(entries):
    """Drop entries nested inside another entry's translated span - a key must be whole."""
    out = []
    for e in entries:
        if any(o[5] <= e[0] < o[6] for o in out if o[3]):
            raise TemplateError("data-i18n nested inside data-i18n at offset %d" % e[0])
        out.append(e)
    return out


def extract(html, into):
    for _, _, _, text_key, attr_keys, inner_start, inner_end in _dedupe(list(marked(html))):
        if text_key:
            into[text_key] = html[inner_start:inner_end]


def extract_attrs(html, into):
    for open_start, open_end, _, _, attr_keys, _, _ in marked(html):
        tag = html[open_start:open_end]
        for attr, key in attr_keys.items():
            m = re.search(r'\s' + re.escape(attr) + r'="([^"]*)"', tag)
            if not m:
                raise TemplateError("data-i18n-attr names %s, which the tag does not have" % attr)
            into[key] = m.group(1)


def strip_markers(tag):
    return re.sub(r'\sdata-i18n(?:-attr)?="[^"]*"', "", tag)


def render(html, strings):
    """Substitute every marked element, back to front so earlier offsets stay valid."""
    for entry in reversed(_dedupe(list(marked(html)))):
        open_start, open_end, _, text_key, attr_keys, inner_start, inner_end = entry
        tag = html[open_start:open_end]
        for attr, key in attr_keys.items():
            value = strings.get(key)
            if value is not None:
                tag = re.sub(
                    r'(\s' + re.escape(attr) + r'=")[^"]*(")',
                    lambda m: m.group(1) + value.replace("\\", "\\\\") + m.group(2),
                    tag,
                    count=1,
                )
        tag = strip_markers(tag)
        inner = html[inner_start:inner_end]
        if text_key and strings.get(text_key) is not None:
            inner = strings[text_key]
        html = html[:open_start] + tag + inner + html[inner_end:]
    return html


def keys_of(html):
    keys = []
    for _, _, _, text_key, attr_keys, _, _ in marked(html):
        if text_key:
            keys.append(text_key)
        keys.extend(attr_keys.values())
    return keys


# --- page assembly ---------------------------------------------------------------------

def page_url(locale, page):
    if locale == "en":
        return SITE + "/" if page == "index.html" else SITE + "/" + page
    prefix = SITE + "/" + locale.lower() + "/"
    return prefix if page == "index.html" else prefix + page


def head_links(locale, page):
    """canonical plus the hreflang set - the reason each language gets its own URL."""
    lines = ['<link rel="canonical" href="%s">' % page_url(locale, page)]
    if page in LOCALIZED_PAGES:
        for other in built_locales():
            lines.append(
                '<link rel="alternate" hreflang="%s" href="%s">' % (other, page_url(other, page))
            )
        lines.append('<link rel="alternate" hreflang="x-default" href="%s">' % page_url("en", page))
    return "\n".join(lines)


def picker(locale, page, strings):
    """The language control: a <details> holding one <a> per locale.

    <details> rather than a scripted popover, so the menu opens with JavaScript off and a
    crawler follows the links - which is how the other locales get discovered at all. The
    hrefs are root-absolute (`/de/`), unlike the assets around them: they have to name the
    canonical form of each URL, and a relative `../de/index.html` would advertise a second
    spelling of a page whose canonical says `/de/`. The cost is that the picker is the one
    part of a page opened over file:// that does not work.

    The flags and the order are the app's, and so is the globe on the first row: a flag names
    a country and a country is not a language, so it is there to help the eye find a row, and
    the name beside it is what identifies the entry. The globe holds that column open on the
    one row that has no country.
    """
    target = page if page in LOCALIZED_PAGES else "index.html"

    def row(flag, label, href, extra=""):
        return ('<a%s href="%s"><span class="flag" aria-hidden="true">%s</span>%s</a>'
                % (extra, href, flag, label))

    items = [row("\U0001F310", strings.get("lang.system", "System"),
                 page_url("en", target)[len(SITE):], ' class="lang-auto"')]
    for other in built_locales():
        href = page_url(other, target)[len(SITE):]
        extra = ' hreflang="%s" lang="%s"' % (other, other)
        if other == locale:
            extra += ' class="on" aria-current="page"'
        items.append(row(LANGUAGE_FLAGS[other], LANGUAGE_NAMES[other], href, extra))

    return (
        '<details class="lang">'
        '<summary class="lang-btn">'
        '<svg class="lang-globe" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
        '<path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/></svg>'
        '<span class="lang-now">%s</span>'
        '<svg class="lang-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
        "</summary>"
        '<div class="lang-menu">%s</div>'
        "</details>"
    ) % (LANGUAGE_NAMES[locale], "".join(items))


def runtime_strings(strings):
    """Strings the inline scripts need, handed over as data rather than baked into the code."""
    wanted = {k: v for k, v in strings.items() if k.startswith("js.") or k.startswith("group.")}
    return "<script>window.__I18N__=%s;</script>" % json.dumps(wanted, ensure_ascii=False)


def build_page(template, locale, page, strings):
    html = render(template, strings)
    html = html.replace("<!--i18n:head-->", head_links(locale, page))
    html = html.replace("<!--i18n:picker-->", picker(locale, page, strings))
    html = html.replace("<!--i18n:runtime-->", runtime_strings(strings))
    lang_attr = 'lang="%s"' % locale
    if locale in RTL:
        lang_attr += ' dir="rtl"'
    html = re.sub(r'<html lang="[^"]*"', "<html " + lang_attr, html, count=1)
    if locale != "en":
        html = ROOT_PATHS.sub(lambda m: m.group(1) + "../" + m.group(2), html)
    return html


def js_strings():
    """English for the keys no template carries - they are only read by the inline scripts."""
    path = os.path.join(SRC, "strings.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load(locale):
    path = os.path.join(I18N, locale + ".json")
    if locale == "en" or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def template_keys():
    """Every key a page needs. A locale that misses one is not offered - a half-translated
    page is worse than an English one, because the visitor cannot get back to English."""
    keys = set(js_strings())
    for page in LOCALIZED_PAGES:
        keys.update(keys_of(open(os.path.join(SRC, page), encoding="utf-8").read()))
    return keys


def outputs():
    """{relative path: content} for the whole site."""
    templates = {p: open(os.path.join(SRC, p), encoding="utf-8").read()
                 for p in LOCALIZED_PAGES + ENGLISH_ONLY_PAGES}
    files = {}
    for page in LOCALIZED_PAGES + ENGLISH_ONLY_PAGES:
        files[page] = build_page(templates[page], "en", page, {})
    for locale in built_locales():
        if locale == "en":
            continue
        strings = load(locale)
        for page in LOCALIZED_PAGES:
            files[locale.lower() + "/" + page] = build_page(templates[page], locale, page, strings)
    return files


_built = None


def built_locales():
    """Locales that have a translation file - the only ones a picker or hreflang may name."""
    global _built
    if _built is None:
        needed = template_keys()
        # LOCALES order is the app's picker order, English in its alphabetical slot rather
        # than pulled to the front - the app lists it there and a list that is alphabetical
        # except for one row reads as a sorting bug.
        _built = [l for l in LOCALES if l == "en" or needed <= set(load(l))]
    return _built


def incomplete_locales():
    needed = template_keys()
    out = {}
    for locale in LOCALES:
        if locale == "en":
            continue
        strings = load(locale)
        if strings and not needed <= set(strings):
            out[locale] = sorted(needed - set(strings))
    return out


def sitemap():
    urls = []
    for locale in built_locales():
        for page in LOCALIZED_PAGES:
            urls.append(page_url(locale, page))
    for page in ENGLISH_ONLY_PAGES:
        urls.append(page_url("en", page))
    body = "\n".join("  <url><loc>%s</loc></url>" % u for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- Generated by build.py - edit the page list there, not here. Announced by the\n"
        "     Sitemap line in robots.txt. lastmod is deliberately omitted: a hand-maintained\n"
        "     date goes stale and search engines discount timestamps they cannot trust. -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n"
    )


# --- translation integrity ---------------------------------------------------------------

TAG_NAMES = re.compile(r"</?([a-zA-Z][\w-]*)")
ATTRS = re.compile(r'\b(id|href|class|rel|target|aria-hidden)="([^"]*)"')


def lint_locale(locale, base, strings):
    """Values carry HTML, so a translator can quietly drop a tag, an id the script looks up,
    or the href of a link. None of that shows up as a missing key - it shows up as a broken
    page in one language nobody on the team reads."""
    problems = []
    for key, en in sorted(base.items()):
        value = strings.get(key)
        if value is None:
            continue
        want, got = sorted(TAG_NAMES.findall(en)), sorted(TAG_NAMES.findall(value))
        if want != got:
            problems.append((key, "tags %s -> %s" % (want or "none", got or "none")))
            continue
        want_attrs = sorted(ATTRS.findall(en))
        got_attrs = sorted(ATTRS.findall(value))
        if want_attrs != got_attrs:
            missing = [a for a in want_attrs if a not in got_attrs]
            if missing:
                problems.append((key, "lost %s" % ", ".join('%s="%s"' % a for a in missing)))
    return problems


SCRIPTS = re.compile(r"<(script|style)\b.*?</\1>", re.S)
BARE_AMP = re.compile(r"&(?!#?\w{1,8};)")


def lint_output(files):
    """What the rendered page must never contain. A bare `&` is the one that actually
    shipped: the app writes its group as "Movies &amp; TV" and a well-meaning unescape in
    the sync script turned it into "Movies & TV" in seven languages at once."""
    problems = []
    for path, html in sorted(files.items()):
        if not path.endswith(".html"):
            continue
        if "data-i18n" in html:
            problems.append((path, "a translation marker survived into the output"))
        if "<!--i18n:" in html:
            problems.append((path, "an i18n placeholder was never filled"))
        if '<link rel="canonical"' not in html:
            problems.append((path, "no canonical link"))
        m = BARE_AMP.search(SCRIPTS.sub("", html))
        if m:
            problems.append((path, "bare & in the markup, not an entity"))
    return problems


def lint():
    base = load_base()
    bad = 0
    for locale in LOCALES:
        if locale == "en":
            continue
        strings = load(locale)
        if not strings:
            continue
        for key, problem in lint_locale(locale, base, strings):
            print("  %-6s %-26s %s" % (locale, key, problem))
            bad += 1
    for path, problem in lint_output(outputs()):
        print("  %-28s %s" % (path, problem))
        bad += 1
    print("%d markup problem(s)" % bad)
    return 1 if bad else 0


def load_base():
    path = os.path.join(I18N, "en.json")
    if not os.path.exists(path):
        sys.exit("no i18n/en.json - run python3 build.py --extract first")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""

    if mode == "--lint":
        return lint()

    if mode == "--extract":
        os.makedirs(I18N, exist_ok=True)
        strings = dict(js_strings())
        for page in LOCALIZED_PAGES:
            html = open(os.path.join(SRC, page), encoding="utf-8").read()
            extract(html, strings)
            extract_attrs(html, strings)
        with open(os.path.join(I18N, "en.json"), "w", encoding="utf-8") as f:
            json.dump(strings, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("i18n/en.json: %d keys" % len(strings))
        return 0

    files = dict(outputs())
    files["sitemap.xml"] = sitemap()

    if mode == "--check":
        stale = []
        for path, content in files.items():
            full = os.path.join(ROOT, path)
            if not os.path.exists(full) or open(full, encoding="utf-8").read() != content:
                stale.append(path)
        if stale:
            print("stale output, run python3 build.py:\n  " + "\n  ".join(sorted(stale)))
            return 1
        print("output is up to date (%d files)" % len(files))
        return 0

    for path, content in sorted(files.items()):
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(path) else None
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
    print("%d files, %d locales" % (len(files), len(built_locales())))
    for locale, missing in sorted(incomplete_locales().items()):
        print("  %s left out, %d keys missing (first: %s)" % (locale, len(missing), missing[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
