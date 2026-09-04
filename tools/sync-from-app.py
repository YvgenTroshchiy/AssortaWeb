#!/usr/bin/env python3
"""Copy from the app everything the site must not decide for itself.

The chip cloud, the demo grid and the phone mockups all name the app's own groups, and
those are already translated in every app locale as `information_tag_*`. Taking them from
there rather than from a translator is the only way the site cannot end up calling a group
something the app does not.

Two site chips have no exact app key and are left to ordinary translation, flagged below.

The language picker is the same story. `AppLanguage.kt` already holds, for every locale, its
native name, its flag, whether it is RTL and the order the app lists it in - decisions that
were argued once there (a flag names a country and a country is not a language; the order is
Latin names alphabetically with diacritics folded, then the other scripts in Unicode block
order). The site reads that table out into `i18n/languages.json` rather than keeping a second
copy that drifts. It lives in `src/` and not in `i18n/`, which holds translation files only:
the detector suite globs that directory and would read a stray index as a locale named
"languages". `lang.system` - the "follow the device" row - comes from the app's
`settings_language_system`, already translated everywhere.

    python3 tools/sync-from-app.py [--languages] [path-to-AssortaKMP]

`--languages` writes only i18n/languages.json and leaves the translation files alone.
"""

import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_APP = os.path.join(os.path.dirname(ROOT), "AssortaKMP")
RESOURCES = "shared/src/commonMain/composeResources"

# site key -> the app string that names the same group.
# The site says "Shopping" where the app says "Shopping list" and "Movies" where the app
# says "Movies & TV"; the English page keeps its own shorter wording (that copy was not
# part of this change), every other locale takes the app's.
GROUPS = {
    "wishList": "wish_list", "shopping": "shopping_list", "travel": "travel",
    "cooking": "cooking", "health": "health", "sport": "sport", "movies": "movies",
    "books": "books", "music": "music", "inspiration": "inspiration", "ideas": "ideas",
    "work": "work", "tasks": "tasks", "education": "education", "finance": "finance",
    "tech": "tech", "family": "family", "home": "home", "beauty": "beauty",
    "personal": "personal", "auto": "auto",
}

# "Hobby" is on a mockup tile but is not one of the app's groups - see docs/i18n/plan.md.
UNMAPPED = ["hobby"]

# The picker's "follow the device" row, verbatim from the app's own setting.
SYSTEM_KEY = "settings_language_system"

APP_LANGUAGE = "shared/src/commonMain/kotlin/com/troshchiy/assorta/locale/AppLanguage.kt"
ENTRY = re.compile(
    r'^\s*[A-Z_]+\("(?P<tag>[\w-]+)",\s*"(?P<name>[^"]+)",\s*"(?P<flag>[^"]+)"'
    r'(?:,\s*isRtl\s*=\s*(?P<rtl>true|false))?\)',
    re.M,
)

# site locale -> the app's resource folder for it.
FOLDERS = {
    "ar": "values-ar", "cs": "values-cs", "da": "values-da", "de": "values-de",
    "el": "values-el", "es": "values-es", "fi": "values-fi", "fr": "values-fr",
    "he": "values-he", "hi": "values-hi", "hu": "values-hu", "id": "values-id",
    "it": "values-it", "ja": "values-ja", "ko": "values-ko", "nb": "values-nb",
    "nl": "values-nl", "pl": "values-pl", "pt-BR": "values-pt-rBR",
    "pt-PT": "values-pt-rPT", "ro": "values-ro", "ru": "values-ru", "sk": "values-sk",
    "sv": "values-sv", "th": "values-th", "tr": "values-tr", "uk": "values-uk",
    "vi": "values-vi", "zh-CN": "values-zh-rCN", "zh-TW": "values-zh-rTW",
}

# The XML escapes an apostrophe for Android's parser; the site does not need that. The
# entity escapes are left alone on purpose: these values land inside an HTML fragment, so
# "Movies &amp; TV" is already correct there, and unescaping it would emit a bare "&".
UNESCAPE = [("\\'", "'"), ('\\"', '"')]


def read_strings(path):
    xml = io.open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'<string name="([^"]+)">(.*?)</string>', xml, re.S):
        value = m.group(2)
        for a, b in UNESCAPE:
            value = value.replace(a, b)
        out[m.group(1)] = value
    return out


def read_languages(app):
    """The picker table, parsed out of the enum that is the app's own picker."""
    source = io.open(os.path.join(app, APP_LANGUAGE), encoding="utf-8").read()
    body = source[source.index("enum class AppLanguage"):]
    out = []
    for m in ENTRY.finditer(body):
        out.append({
            "tag": m.group("tag"),
            "name": m.group("name"),
            "flag": m.group("flag"),
            "rtl": m.group("rtl") == "true",
        })
    if len(out) < 20:
        sys.exit("parsed only %d languages out of AppLanguage.kt - the enum shape changed" % len(out))
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    app = args[0] if args else DEFAULT_APP
    base = os.path.join(app, RESOURCES)
    if not os.path.isdir(base):
        sys.exit("no app resources at %s" % base)

    languages = read_languages(app)
    with io.open(os.path.join(ROOT, "src", "languages.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_from": APP_LANGUAGE, "languages": languages},
                  f, ensure_ascii=False, indent=2)
        f.write(u"\n")
    if "--languages" in argv:
        print("%d languages into src/languages.json" % len(languages))
        return 0

    for locale, folder in sorted(FOLDERS.items()):
        strings = read_strings(os.path.join(base, folder, "strings.xml"))
        target = os.path.join(ROOT, "i18n", locale + ".json")
        existing = {}
        if os.path.exists(target):
            existing = json.load(io.open(target, encoding="utf-8"))

        system = strings.get(SYSTEM_KEY)
        if system is None:
            sys.exit("%s: no %s" % (folder, SYSTEM_KEY))
        existing["lang.system"] = system

        for key, app_key in GROUPS.items():
            value = strings.get("information_tag_" + app_key)
            if value is None:
                sys.exit("%s: no information_tag_%s" % (folder, app_key))
            existing["group." + key] = value

        os.makedirs(os.path.dirname(target), exist_ok=True)
        with io.open(target, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write(u"\n")

    print("%d languages into src/languages.json" % len(languages))
    print("%d locales, %d group names + lang.system each (%s still translated by hand)"
          % (len(FOLDERS), len(GROUPS), ", ".join(UNMAPPED)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
