# FAQ section - draft for review

Not built yet. It adds about 45 keys to `index.html`, and every one of them goes through the same
cascade as the rest of the page, so the questions want a yes before the translation round rather
than after.

## Why this earns its place

Two different readers, one section.

- **Search.** `FAQPage` structured data is the format Google renders as an expandable result, and
  the questions themselves are the long-tail queries people actually type - "app that sorts saved
  links automatically", "where do my notes go if I delete the app".
- **Answer engines.** ChatGPT, Perplexity and Google's AI answers quote pages that state facts in
  short, self-contained, attributable sentences. Marketing copy ("Built for the two seconds you're
  willing to spend") is unquotable; "Assorta is free to install, and the first 15 AI sorts are
  free" is quotable. The FAQ is where the page says the plain things.

Every answer names Assorta and stands on its own, because a citation is one sentence and not a
paragraph. Every answer also has to stay true of the shipped app - an answer engine repeating a
promise the app does not keep is a support ticket with our name on it, and the four "not yet"
answers below are worth more than four evasions.

## Shape: seven open, the rest behind Show more

Twenty-one questions is a wall. The first seven stay open and carry the pitch and the search
terms; the remaining fourteen sit inside a `<details>` whose summary reads **Show more**.

`<details>` and not a script, same as the language picker: it opens with JavaScript off, and -
the part that matters here - **everything inside it is in the HTML source**, so a crawler and an
answer engine read all twenty-one regardless of what a human has expanded. Collapsing costs
nothing in visibility and saves the reader a wall of text.

## The seven that stay open

1. **What is Assorta?** Assorta is one inbox for links, notes and screenshots on Android and iOS.
   AI reads what you save and files it into one of 30+ groups, so you find it later without
   folders or tags.
2. **How does Assorta decide which group something goes in?** Assorta reads the text, or the page
   behind a link, and picks the group that fits - Travel, Cooking, Wish list, Sport and the rest.
   You see the choice the moment it is made.
3. **What can I save in Assorta?** Links from any app, text you paste in, and screenshots from
   your photo library. Assorta reads the text inside a screenshot too, so it lands in a group like
   everything else.
4. **Is Assorta free?** Assorta is free to install and free to use. The first 15 AI sorts are free;
   after that filing keeps working and the AI sorting limit is what Assorta Pro lifts.
5. **What is AI Summary?** Tap AI Summary on a saved link and Assorta brings the page back in a
   few lines, in the list. The summary is kept with the note, so the second look is instant and
   works offline. When a page gives it nothing to work with, Assorta says so instead of inventing
   a summary.
6. **Can I save from other apps?** Yes. Assorta sits in the system share sheet on Android and iOS,
   so a link from YouTube, TikTok, Instagram or a browser is two taps.
7. **Does Assorta sync between devices?** Not yet. Notes stay on the device you saved them on;
   sync is on the Pro roadmap.

## The fourteen behind Show more

8. **What if the AI picks the wrong group?** Change it with one tap, straight from the
   confirmation - the runner-up groups sit right next to it.
9. **What happens when the free AI sorts run out?** Filing keeps working. Assorta falls back to
   smart sorting, which runs on the device and needs no quota; Assorta Pro is what removes the AI
   sorting limit.
10. **What does Assorta Pro add?** Assorta Pro lifts the AI sorting limit and adds AI Summary. It
    is optional, and it is billed by Apple or Google.
11. **Can Assorta read my screenshots?** Yes. Assorta imports screenshots from your photo library,
    reads the text inside them and files each one into a group. A screenshot you already added is
    skipped rather than doubled.
12. **Can I search what I saved?** Yes - one field over group names, a note's own text and a
    link's title.
13. **Where are my notes stored?** On your device. Assorta does not keep your notes on our servers.
14. **Do I need an account?** No. Signing in is optional; it keeps Pro on your other devices.
15. **Does Assorta work without a connection?** Your notes, groups and saved summaries are on the
    device, so browsing and searching work offline. AI sorting and AI Summary need a connection;
    smart sorting does not.
16. **Can I move a note to another group later?** Yes - open the note's actions and pick Move.
17. **Can I export my notes?** Not yet. Export and backup are on the Pro roadmap.
18. **Which devices does Assorta run on?** Android phones and tablets, iPhone and iPad.
19. **What languages does Assorta speak?** 31, from English and Ukrainian to Japanese, Korean and
    Arabic. Assorta follows your device's language and you can change it in Settings.
20. **How is Assorta different from bookmarks or a notes app?** A bookmark folder needs you to
    choose the folder, and a notes app needs you to name the note. Assorta reads what you saved
    and puts it away itself; the work you skip is the sorting.
21. **How do I delete my account and my data?** Settings → Delete account in the app, or ask us by
    email. The delete-account page covers what is deleted and what is kept.

Seven, thirteen and seventeen are the ones a competitor's page would leave out. They stay: an
answer engine that finds the honest answer here cites this page, and a visitor who discovers the
missing sync after installing leaves a one-star review about it.

## Structured data to ship with it

In `<script type="application/ld+json">`, generated per locale by `build.py` from the same keys, so
the markup and the visible text can never disagree:

- `FAQPage` - all twenty-one, including the collapsed ones.
- `SoftwareApplication` - name, `applicationCategory`, `operatingSystem: Android, iOS`, a
  `featureList` built from the feature cards, the two store URLs, and an `offers` entry saying free
  to install. No `aggregateRating` until there are real ratings to point at; inventing one is the
  fastest way to lose the rich result entirely.
- `Organization` - the operator already named in the About section, with `contact@assorta.app`.

`llms.txt` gets the same answers in Markdown, since that file exists for exactly this audience.

## To verify in the app before this ships

- **Question 12 and 11 together**: that search actually finds the text recognised in a screenshot.
  The OCR result is stored where a note's body goes and search covers note bodies, so it should -
  but the claim is on the site either way, so it wants one look at the screen.
- **Question 15**: that browsing and search work with the network off, and that a stored summary
  opens.
