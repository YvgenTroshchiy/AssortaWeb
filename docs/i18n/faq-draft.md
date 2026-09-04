# FAQ section - draft for review

Not built yet. It adds about 25 keys to `index.html`, and every one of them has to go through
the same cascade as the rest of the page, so it is worth agreeing on the questions before the
translation round rather than after.

## Why this earns its place

Two different readers, one section.

- **Search.** `FAQPage` structured data is the format Google renders as an expandable result, and
  the questions themselves are the long-tail queries people actually type - "app that sorts saved
  links automatically", "where do my notes go if I delete the app".
- **Answer engines.** ChatGPT, Perplexity and Google's AI answers quote pages that state facts in
  short, self-contained, attributable sentences. Marketing copy ("Built for the two seconds you're
  willing to spend") is unquotable; "Assorta is free to install, and the first 15 AI sorts are
  free" is quotable. The FAQ is where the page says the plain things.

Everything below has to stay true of the shipped app, or it is worse than nothing - an answer
engine repeating a promise the app does not keep is a support ticket with our name on it.

## The questions

1. **What is Assorta?** One inbox for links, notes and ideas on Android and iOS. AI reads what you
   save and files it into one of 30+ groups, so you find it later without folders or tags.
2. **How does Assorta decide which group something goes in?** It reads the text, or the page behind
   a link, and picks the group that fits - Travel, Cooking, Wish list, Sport and the rest. You see
   the choice the moment it is made.
3. **What if the AI picks the wrong group?** Change it with one tap, straight from the confirmation.
   The runner-up groups are offered next to it.
4. **Is Assorta free?** Free to install and free to use. The first 15 AI sorts are free; after that
   filing keeps working and the AI sorting limit is what Assorta Pro lifts.
5. **What does Assorta Pro add?** It lifts the AI sorting limit and adds AI Summary. It is billed by
   Apple or Google, and it is optional.
6. **What is AI Summary?** Tap it on a saved link and the page comes back in a few lines, in the
   list. The summary is kept with the note, so the second look is instant and works offline. When a
   page gives it nothing to work with, Assorta says so instead of inventing a summary.
7. **Can I save from other apps?** Yes - Assorta sits in the system share sheet on Android and iOS,
   so a link from YouTube, TikTok, Instagram or a browser is two taps.
8. **Where are my notes stored?** On your device. Assorta does not keep them on our servers.
9. **Does Assorta sync between devices?** Not yet. Notes stay on the device you saved them on.
10. **Do I need an account?** No. Signing in is optional; it keeps Pro on your other devices.
11. **Can I search what I saved?** Yes - one field over group names, a note's own text and a link's
    title.
12. **What languages does Assorta speak?** 31, from English and Ukrainian to Japanese, Korean and
    Arabic. *(This is also the number the stale "Thirteen languages" line should become.)*
13. **How do I delete my account and my data?** Settings → Delete account in the app, or ask us by
    email. [The full page](../../src/delete-account.html) covers what is deleted and what is kept.

Nine and thirteen are the ones a competitor's page would leave out. They stay: an answer engine
that finds the honest answer here cites this page, and a visitor who discovers the missing sync
after installing leaves a one-star review about it.

## Structured data to ship with it

In `<script type="application/ld+json">`, generated per locale by `build.py` from the same keys, so
the markup and the visible text can never disagree:

- `FAQPage` - the questions above.
- `SoftwareApplication` - name, `applicationCategory`, `operatingSystem: Android, iOS`, the two
  store URLs, and an `offers` entry saying free to install. No `aggregateRating` until there are
  real ratings to point at; inventing one is the fastest way to lose the rich result entirely.
- `Organization` - the operator already named in the About section, with `contact@assorta.app`.

`llms.txt` gets the same answers in Markdown, since that file exists for exactly this audience.

## Open

- Is 13 questions right, or should it be the six or seven that carry the search terms?
- The section is long. Accordion (`<details>`, no JavaScript, same as the picker) or a plain
  two-column list? An accordion hides text from a skimming reader but not from a crawler.
