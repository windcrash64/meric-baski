# Track 8 — Imagery Sourcing, Licensing & Delivery

**Purpose:** give the Maven build a legally safe, visually coherent, performance-budgeted photography
system — every non-machine image on the site — plus the exact assets to download.
**Date of research:** 2026-07-28. Every licence clause below was read from the live page on that date.
Every candidate image URL in §5 was HTTP-verified on that date (method in §0).

---

## 0. Method, coverage and gaps

| Source | How it was inspected | Result |
|---|---|---|
| Unsplash | `/license`, `/plus/license`, attribution guideline article, 4 search pages, 2 photo pages | full |
| Pexels | `/license` + **internal JSON API** `www.pexels.com/en-us/api/v3/search/photos` (28 queries × 8 results = 224 candidates), 4 photo pages | full + deep |
| Pixabay | `/service/license-summary/` (headless Chrome — blocks curl/WebFetch with 403), 2 search pages | full |
| Openverse | `/about` (headless Chrome — 403 to plain fetch) + **public API** `api.openverse.org/v1/images` (no key needed) | full |
| Wikimedia Commons | `Commons:Licensing` + MediaWiki API `action=query&generator=search` with `extmetadata` | full |
| Burst (Shopify) | `shopify.com/stock-photos/` + `/legal/terms` | full |
| StockSnap | `/license` (headless Chrome) | full |
| web.dev / caniuse | LCP thresholds, AVIF support % | full |
| Vercel docs | `/docs/caching/cdn-cache` static-file caching | full |

**Verification method for candidates (§5).** Photo IDs came from each platform's own API/DOM, so
they are real records, not guesses. I then HTTP-checked them:

- **All 40 shortlisted Pexels images returned `200` on `images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg`.**
  This is the authoritative existence check.
- Pexels **page** URLs return `403` to `curl` (bot fingerprinting) but `200` to a real browser and to
  WebFetch — I confirmed 4 of them individually that way. **The 403s are not dead links.** Same for
  one Pixabay page (`541626`) whose CDN file returns `200`.
- Unsplash sits behind an Anubis proof-of-work wall (`unsplash.com/.within.website`, HTTP 307/401 to
  curl). Unsplash entries were verified via WebFetch page reads instead; the two most important
  (`Tzm3Oyu_6sk`, `QRykXu51r_0`) were individually confirmed as **free Unsplash License, not Unsplash+**.

**Gap / honesty note.** I did not visually inspect every candidate pixel-by-pixel. Titles, tags,
descriptions and dimensions are from the platforms' own metadata. Before any image ships, a human
must open it at full size and check §3's four-point clearance list. Tags lie by omission — a machine
can carry a visible logo that nobody tagged.

---

## 1. Licence terms, as of 2026-07-28

### 1.1 Summary matrix

| Source | Commercial use | Attribution required | Key restriction that matters to us | Verdict for a client site |
|---|---|---|---|---|
| **Pexels** | Yes | **No** | No implied endorsement; no redistribution to other stock sites; not usable as a trademark | ✅ **Primary source** |
| **Unsplash** (free tier) | Yes | **No** | Cannot compile images to build a competing service | ✅ **Secondary source** — but see §2.1 trap |
| **Pixabay** | Yes | **No** | **Content containing recognisable trademarks/logos cannot be used commercially in relation to goods and services** | ⚠️ **Use, but with the strictest logo screening** |
| **Burst** (Shopify) | Yes | No | CC0 *or* Burst License at Shopify's discretion; no unlawful/immoral use | ✅ Safe, but tiny print-industry catalogue |
| **StockSnap** | Yes | No | CC0. No implied endorsement | ✅ Safe, small catalogue, ageing |
| **Openverse** | Depends per item | **Usually yes** | Aggregator — **does not verify licences** | ⚠️ **Not for hero imagery.** See §2.3 |
| **Wikimedia Commons** | Yes (policy requires it) | **Yes, almost always** (CC BY / BY-SA) | BY-SA is share-alike/viral on derivatives | ⚠️ Reference use only. See §2.4 |

### 1.2 The clauses, quoted

**Unsplash License** — <https://unsplash.com/license>

> "Unsplash grants you an irrevocable, nonexclusive, worldwide copyright license to download, copy,
> modify, distribute, perform, and use images from Unsplash for free, including for commercial
> purposes, without permission from or attributing the photographer or Unsplash."

Restrictions:

> "Images cannot be sold without significant modification."
> "Compiling images from Unsplash to replicate a similar or competing service" *is prohibited.*

We do neither. Building a corporate site is squarely inside the grant.

**Attribution nuance** — <https://help.unsplash.com/en/articles/2511315-guideline-attribution>.
The *License* does not require credit. The *API Guidelines* do:

> "When displaying a photo from Unsplash, your application must attribute Unsplash, the Unsplash
> photographer, and contain a link back to their Unsplash profile."

**We are downloading manually, not calling the API, so the API Guidelines do not bind us.** This
matters: it means we may self-host the files rather than hotlinking the Unsplash CDN (the API
Guidelines would have required hotlinking). Self-hosting is the right call for LCP control.

**Pexels License** — <https://www.pexels.com/license/>

> "All photos and videos on Pexels are free to use."
> "Giving credit to the photographer or Pexels is not necessary but always appreciated."
> "You can modify the photos and videos from Pexels. Be creative and edit them as you like."

Not allowed:

> "Identifiable people may not appear in a bad light or in a way that is offensive."
> "Don't sell unaltered copies of a photo or video, e.g. as a poster, print or on a physical product
> without modifying it first."
> "Don't imply endorsement of your product by people or brands on the imagery."
> "Don't redistribute or sell the photos and videos on other stock photo or wallpaper platforms."
> "Don't use the photos or videos as part of your trade-mark, design-mark, trade-name, business name
> or service mark."

Two of these bite us directly. **"Don't imply endorsement … by people or brands"** — so a stock photo
of a technician must never be captioned as if he is a Maven employee endorsing Maven, and a photo
containing a rival machine must never sit next to "Maven ürünleri". **"Don't use … as part of your
trade-mark"** — so no stock photograph may be composited into the Maven "M." logo or favicon.

**Pixabay Content License** — <https://pixabay.com/service/license-summary/>

Allowed: use for free; no attribution; modify/adapt into new works. Prohibited Uses include:

> "You cannot sell or distribute Content (either in digital or physical form) on a Standalone basis.
> Standalone means where no creative effort has been applied to the Content and it remains in
> substantially the same form as it exists on our website."
>
> **"If Content contains any recognisable trademarks, logos or brands, you cannot use that Content
> for commercial purposes in relation to goods and services. In particular, you cannot print that
> Content on merchandise or other physical products for sale."**
>
> "You cannot use Content in any immoral or illegal way, especially Content which features
> recognisable people."
> "You cannot use Content in a misleading or deceptive way."
> "You cannot use any of the Content as part of a trade-mark, design-mark, trade-name, business name
> or service mark."

And the disclaimer that shifts all risk onto us:

> "Please be aware that certain Content may be subject to additional intellectual property rights
> (such as copyrights, trademarks, design rights), moral rights, proprietary rights, property rights,
> privacy rights or similar. **It is your responsibility to check whether you require the consent of
> a third party or a license to use Content.**"

**This is the single most important clause on this page for us.** Maven is a commercial dealer of
goods. A Pixabay photo showing an HP/Canon/Epson/Roland logo is, by the literal text, *not licensed*
for our use. Pixabay's own search happily returns exactly that — see §2.2.

**Burst** — <https://www.shopify.com/stock-photos/legal/terms>. Dual licence at Shopify's discretion:
CC0, or the Burst License ("You are free to adapt and use the Licensed Content for free for
commercial and noncommercial purposes"). No attribution required. Prohibits unlawful/immoral use,
uses that embarrass or damage the reputation of identifiable persons, compiling a competing service,
and selling unaltered content as digital files. **Safe — but Burst's catalogue is e-commerce/lifestyle
oriented and has almost nothing on industrial printing.** Use it for office/team/handshake filler only.

**StockSnap** — <https://stocksnap.io/license>

> "every single image on StockSnap are governed exclusively by the generous terms of the Creative
> Commons CC0 license."

Permits download, publish, revise, copy, alter, share, personal and commercial use, no attribution.
Its only stated limits are no implied endorsement and no warranty. **Cleanest licence of the set** —
but the catalogue is small and dated; it will not carry the site.

**Openverse** — <https://openverse.org/about>. It is an aggregator run by WordPress (successor to CC
Search), indexing ~800M works. The critical sentence:

> "Openverse does not verify licensing information for individual works, or whether the generated
> attribution is accurate or complete. **Please independently verify the licensing status and
> attribution information before reusing the content.**"

**Wikimedia Commons** — <https://commons.wikimedia.org/wiki/Commons:Licensing>

> "Wikimedia Commons only accepts free content, that is, images and other media files that are not
> subject to copyright restrictions which would prevent them being used *by anyone, anytime, for any
> purpose*."

Commercial use and derivatives are guaranteed. But Commons only polices *copyright*: "Wikimedia
Commons generally only enforces copyright restrictions" — trademark and personality rights are
explicitly out of scope and pushed to `Commons:Non-copyright_restrictions`. In practice nearly
everything usable there is **CC BY 4.0 or CC BY-SA 4.0**, i.e. attribution is mandatory and BY-SA is
share-alike.

---

## 2. The four traps. Read this before picking any image.

### 2.1 Unsplash search mixes free photos with paid Getty images

Unsplash is owned by Getty. Search results silently interleave free Unsplash-License photos with
**Unsplash+ / Getty Images** results that carry a lock icon and require a paid subscription.

Verified: on `unsplash.com/s/photos/large-format-printer`, **five of the top results are credited to
`@gettyimages`** — including the most on-brief images on the page ("Worker in uniform getting printed
sheets from the offset machine", "Automated printing press with white paper roll in industrial shop",
"Side view of powerful printing press with computer monitor in factory shop"). I opened
`/photos/worker-in-unifrom-getting-printed-sheets-from-the-offset-machine-at-the-printing-manufacturing-VwZooA-jsDw`
and it states **"Licensed under the Unsplash+ License"** with a subscription lock.

The Unsplash+ License (<https://unsplash.com/plus/license>) is a genuinely different product —
it carries an "Unsplash+ Warranty: using Unsplash+ images will not infringe third party IP rights or
publicity rights", up to **US $10,000 per licensed photo** in legal cover. That is real value, but it
costs money and **we have not bought it.**

> **Rule:** on any Unsplash photo page, the free ones say verbatim *"Free to use under the Unsplash
> License"*. If the page says *"Unsplash+"* or the author is `@gettyimages`, walk away. Grabbing the
> preview JPEG of an Unsplash+ image is straightforward copyright infringement against Getty, who are
> the most litigious rights-holder in stock photography.

### 2.2 Brand logos on machines — the defining risk for *this* site

We sell printing machines. Almost every good stock photo of a printing machine has a manufacturer's
logo on it, and that manufacturer is our competitor or our supplier's competitor.

Concrete evidence found during this research:

- Pixabay: `pixabay.com/photos/printers-hp-large-printer-a0-hp-2302607/` — the slug literally contains
  `hp`. Under Pixabay's trademark clause this is **not licensed** for our commercial use.
- Wikimedia Commons: `File:Canon_imagePROGRAF_TX-5310_LARGE_FORMAT_PRINTER.jpg` (CC BY-SA 4.0,
  7398×4058, by Dinkun Chen) — a beautiful, high-res photo of a **Canon** machine. Legally reusable
  under copyright; commercially suicidal for us.
- Pexels tag data exposes brands even when the title does not: photo `17536002` ("Photo printer") is
  tagged `canon`; `5727002` is tagged `epson`; `10960792` is tagged `heidelberg`; `9574509` is tagged
  `xerox`.

Two separate harms, and they are worth separating because they have different remedies:

1. **Licence breach** (Pixabay only — its licence explicitly excludes trademarked content from
   commercial goods/services use). Remedy: don't use that image.
2. **Passing off / misleading advertising** (all sources, and this is the bigger commercial risk). A
   dealer site showing a Roland machine next to "Maven" branding implies a dealership we may not hold.
   In Turkey this engages the Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği and TTK haksız
   rekabet provisions. Remedy: don't use that image, regardless of licence.

> **Hard rule for the build: no third-party manufacturer marks anywhere on the site, in any photo,
> at any size, including out-of-focus background machines and control-panel splash screens.** The
> candidate list in §5 is filtered on this basis, and every entry carries a logo-risk note. When in
> doubt, crop it out or pick a macro shot of a mechanism where no badge is in frame.

### 2.3 AI-generated stock is now polluting the free platforms

This one caught me mid-research and would absolutely have shipped unnoticed.

Pexels returns a large cluster of gorgeous "vintage printing press / graphic design studio" images
under IDs **6620963, 6620970, 6620972, 6620973, 6620977, 6620983, 6620985, 6620989, 6620991, 6620992,
6620993, 6620997, 6620998, 6620999, 6621000, 6621001** and **4348164**. They dominate the results for
`print shop`, `printing press worker`, `offset printing machine` and `ink bottle color`.

All of them belong to the account `@ai25studioai`, whose profile bio reads:

> "AI25.Studio — AI-native cinematic production studio creating hybrid commercials, branded
> storytelling, and premium AI visuals"

Pixabay has the same problem, less subtly — its `printing ink` results include
`pixabay.com/illustrations/ai-generated-chinese-asian-8993846/`.

Why this disqualifies them for Maven:

- **Copyright status is unsettled.** Purely AI-generated output has no human author and in several
  jurisdictions attracts no copyright at all — which means the uploader may have had nothing to
  license to Pexels, and Pexels nothing to license to us. The platform licence is a contract, not a
  guarantee of title.
- **The machines are fake.** These images depict plausible-looking but non-existent presses with
  impossible mechanisms. Our audience is print-shop owners and technicians. They will spot it
  instantly, and it destroys exactly the technical credibility a dealer site exists to build.
- One of them (`4348164`) is described as *"Vibrant Ecoline ink bottles"* — **Ecoline is a Royal
  Talens trademark**, so it trips §2.2 as well.

> **Rule:** before shortlisting any Pexels image, check the contributor. Reject `@ai25studioai` and
> any account whose name or bio contains `ai`, `ai-generated`, `midjourney`, `genai`. On Pixabay,
> reject anything under `/illustrations/` with `ai-generated` in the slug. **None of these IDs appear
> in §5.**

### 2.4 Openverse and Wikimedia cannot carry this site

I tested this rather than assuming it. Openverse API, restricted to the only genuinely
attribution-free licences (`license=cc0,pdm`), query `printing press`:

| Result | Resolution | Verdict |
|---|---|---|
| "Screw Printing Press in a British Library Hallway" | 736×1024 | Museum object |
| "Device of Josse Badius: printing press" | 175×203 | Thumbnail of a woodcut |
| "'Le Antichità di Ercolano…' Royal Printing Press, 1757" | 964×1024 | 18th-c. engraving |
| "cave paintings, e-portfolios, printing press & PLE" | 1024×768 | Conference doodle |
| "Lowe portable printing press" | 450×338 | Unusable |

The unrestricted Openverse query returns Flickr snapshots at 1024×768 under **CC BY-SA 2.0**.

Two conclusions:

1. **Openverse's CC0 pool for our subject matter is historical/archival, low-resolution, and
   completely wrong in tone.** It cannot supply a single hero. Its honest use is as a *last-resort
   long-tail search* when nothing else has a specific object.
2. **CC BY-SA is a trap for our grading plan.** §6 bakes duotone/grade into the delivered files. A
   baked-in colour transform is a derivative work, and BY-SA would force us to license our own
   processed asset under BY-SA and credit it visibly. A CSS-only overlay arguably is not a
   derivative, but "arguably" is not a basis for a client deliverable.

> **Rule: Openverse and Wikimedia Commons are excluded from the shipping asset set.** Use them only
> if we need a specific documentary object (e.g. an ISO 12647 control strip) that exists nowhere
> else — and then credit it properly and do not bake in a grade.

### 2.5 Identifiable people and property

- **Pexels/Unsplash/Pixabay do not guarantee model releases.** Pexels only promises the negative:
  people "may not appear in a bad light or in a way that is offensive". There is no positive release
  warranty. (Unsplash+ *does* carry a warranty — one more reason its images look better on paper.)
- Turkish law is strict here: personal image is protected under **TMK m.24–25** and **FSEK m.86**
  (a person's picture may not be published without consent). A recognisable face used to sell Maven's
  services is a commercial use of that person's likeness.
- **Practical rule: prefer photographs where faces are turned away, obscured, distant, in profile, or
  cropped out.** Hands, backs, silhouettes, and people-at-scale in a wide factory shot are safe and
  happen to be more editorial anyway. This is a design win, not just a legal hedge — it matches the
  restrained aesthetic in Track 1.
- Never put a stock person on `iletisim.html` or `kurumsal.html` in a way that reads as "this is our
  team" or "this is our building". That is both an endorsement-implication breach and plainly
  misleading. **Team and premises photography must eventually be real.** Until it exists, use
  machinery, materials and abstract detail — never fake staff.

---

## 3. Four-point clearance checklist (run per image, before download)

1. **Licence tier** — is it the free tier? (Unsplash: page must read "Free to use under the Unsplash
   License". Not `@gettyimages`, not "Unsplash+".)
2. **Provenance** — is the contributor a human photographer? (Reject `@ai25studioai` and friends.)
3. **Marks** — zoom to 100% and sweep the frame: machine badges, control-panel logos, branded
   toolboxes, wall signage, product packaging, T-shirt prints, vehicle marques. Any competitor or
   OEM mark → reject or crop.
4. **People** — any recognisable face? Prefer not. If unavoidable, ensure the usage cannot read as
   endorsement, employment, or testimony.

Record the outcome in the asset manifest (§8). If an image fails 1 or 2, it never enters the repo.

---

## 4. Recommended sourcing strategy

| Rank | Source | Role | Share of set |
|---|---|---|---|
| 1 | **Pexels** | Workhorse. Best industrial/print coverage, cleanest licence for commercial dealer use, no trademark carve-out, richest metadata (tags expose brands before download) | ~65% |
| 2 | **Unsplash** (free tier only) | Texture, colour, materials, editorial detail. Better art direction, worse industrial coverage | ~25% |
| 3 | **Pixabay** | Ink and consumables only — it is the *only* free source with a real ink/CMYK-press catalogue. Strictest logo screening | ~10% |
| 4 | Burst / StockSnap | Emergency filler (office, hands, generic business). Rarely needed | ~0–5% |
| — | Openverse / Wikimedia | Excluded from shipping set (§2.4) | 0% |

**Concentrate per-slot on one photographer where possible.** Several photographers on Pexels shot
whole coherent series in one location with one lens and one light — using 3 frames from one series
gives instant visual consistency for free. The three to exploit:

- **Auto Records** — a complete vehicle-wrap series at 8192×5464 (IDs 10126657/10126661/10126663/
  10126665/10126666/10162528/10162529). This solves the entire vehicle-wrap slot in one download.
- **Somogro Bangladesh** — a newspaper-press series, warm tungsten, documentary (36376366/36376452/
  36376456/36412293/36345065/36376224).
- **Bornil Sarker** — monochrome print-shop series (37394505/37394506).

---

## 5. Image-needs table — 14 slots, verified candidates

All Pexels direct files follow `https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg`
(append `?auto=compress&cs=tinysrgb&w=2560` for a sized fetch). **All Pexels IDs below returned HTTP
200 on that CDN pattern on 2026-07-28.** Pexels page URLs are
`https://www.pexels.com/photo/<slug>-<ID>/`. Licence column: `PX` = Pexels License, `US` = Unsplash
License (free tier), `PB` = Pixabay Content License. None require attribution.

| Slot | Where it lives | Search query that actually works | Candidates (ID · title · photographer · px) | Source · Licence | Notes |
|---|---|---|---|---|---|
| **HERO-01** Print production floor | `index.html` full-bleed hero | Pexels `printing factory night` / `modern printing facility` | **31788399** · *Modern Printing Facility Interior with Workers* · Manuel Campagnoli (@work2survive) · **8064×6048** ⭐ · verified real facility, Bratislava, **no brand logos in tags** — *the pick*<br>37394506 · *Busy Print Shop with Printing Press and Workers* · Bornil Sarker · 6000×4000<br>36376366 · *Men Working in a Newspaper Printing Factory* · Somogro Bangladesh · 4098×2732 | Pexels · PX | 31788399 is the only free image found with the scale + resolution a full-bleed 2560px hero needs. Crop to 21:9. People are distant/incidental → no release issue |
| **HERO-02** Secondary hero | `urunler.html` header | Pexels `printing press worker` | 37394505 · *Monochrome Print Shop with Worker Operating Machine* · Bornil Sarker · 5961×3974 (already B/W — grades perfectly)<br>36412293 · *Man reviewing prints at a printing press* · Somogro Bangladesh · 4280×2853 | Pexels · PX | 37394505 is native monochrome → zero grading work, instant consistency with §6 |
| **APP-01** Large-format / wide-format machine | `urunler.html` category card | Pexels `large format printer`; Pixabay `plotter large format printer`; Unsplash `printing machine` | 20042067 · *Professional Printer in Print Studio* · WAVYVISUALS · 2558×3845<br>`pixabay.com/photos/plotter-large-format-printer-printer-2138990/` (CDN `photo/2017/03/13/07/33/plotter-2138990_1280.jpg`) ✔200<br>`unsplash.com/photos/printing-machine-Tzm3Oyu_6sk` · Bank Phrom · **verified free tier, no visible brand** | Pexels · PX<br>Pixabay · PB<br>Unsplash · US | ⚠️ **Do NOT use** `pixabay.com/photos/printers-hp-large-printer-a0-hp-2302607/` — HP-branded, breaches Pixabay's trademark clause. Check the 2138990 plotter at 100% for a badge before shipping |
| **APP-02** Vehicle wrap | `urunler.html` / applications | Pexels `vehicle wrap`, `car wrap vinyl installation` | **10126666** · *A Person Heating the Wrap of a Car* · Auto Records · **8192×5464** ⭐<br>**10126665** · *A Man Wrapping a Car Hood* · Auto Records · 8192×5464<br>10162528 · *A Man Putting on a Blue Sticker on the Car Door* · Auto Records · 8192×5464<br>`unsplash.com/photos/a-man-is-working-on-an-orange-car-8MXNZCgAah0` · Andre Tan | Pexels · PX<br>Unsplash · US | Take all three Auto Records frames — one shoot, one lens, identical grade. Hands-and-squeegee framing, no faces. ⚠️ Check the car marque/badge is out of frame; avoid Unsplash's Getty "protective film" results (§2.1) |
| **APP-03** Textile printing | `urunler.html` / applications | Pexels `screen printing textile`, `textile workshop` | **32641559** · *Textile Workshop with Screen Printing Frames in Apucarana* · Rodolfo Gaion · 6000×4000 ⭐<br>33650433 · *Men Screen Printing T-Shirt in Workshop* · James Collington · 3265×4898<br>27893033 · *A man is working on a large piece of fabric* · HONG SON · 6720×4480<br>38357014 · *Industrial textile machinery in Uzbekistan factory* · Dmitriy Steinke · 3213×5712 | Pexels · PX | 32641559 is real, unstaged, no logos — best of the set. 38357014 is a strong vertical for a mobile-first card |
| **APP-04** Packaging & label | `urunler.html` / applications | Pexels `label printing`, `cardboard box printing` | 7217859 · *Man Printing Labels For Boxes* · Blue Bird · 4000×6000<br>9594434 · *Brown Cardboard Boxes on Yellow Surface* · Ron Lach · 5304×6502<br>11678431 · *Stacks of Brown Boxes Near Forklift* · Mark Stebnicki · 8640×5760 | Pexels · PX | ⚠️ Avoid `31447457`/`31447458` (*Laverne* branded packaging) — third-party brand. Prefer unbranded kraft |
| **INK-01** Ink bottles / cartridges | `urunler.html` ink category — **the hard slot, see §7** | Pixabay `printing ink`; Pexels `ink cartridge`, `ink bottle color` | `pixabay.com/photos/ink-paints-print-printing-inks-1602896/` (CDN `photo/2016/08/18/13/03/ink-1602896_1280.jpg`) ✔200 ⭐<br>`pixabay.com/photos/paint-bucket-print-printing-house-1602900/` ✔200<br>**7639358** · *Color Ink Cartridge* · IT services EU · 4241×2829 — verified: tagged Cyan/Magenta/Yellow, **no manufacturer named**<br>33475146 · *Black Printer Toner Cartridge on Wooden Background* · Andrey Matveev · 5824×4368<br>8922455 · *Clear Plastic Bottles with Blue Ink* · Аlex Ugolkov · 4775×3581 | Pixabay · PB<br>Pexels · PX | ⚠️ **Reject 4348164** (*"Ecoline ink bottles"*) — AI-generated **and** trademarked (§2.3). Pixabay 1602896/1602900 are genuine print-house ink, the best free ink photography that exists. Max useful width 1280px → **section-width only, never full-bleed.** Cartridge shots must be screened for an embossed OEM logo |
| **INK-02** CMYK / colour management | `index.html` colour strip; ink category | Pexels `cmyk color swatch`; Pixabay `offset printing cmyk`; Unsplash `cmyk` | 9421350 · *Pantone Color Chart* · Леся Терехова · 6000×4000<br>11229778 · *Pantone Colors Samples in Box* · Erik Mclean · 5472×3648<br>11229781 · *Close up of Swatch Books* · Erik Mclean · 3648×5472<br>`pixabay.com/photos/offset-printing-cmyk-printing-3862769/` ✔200<br>`pixabay.com/photos/cmyk-to-dye-table-printing-inks-1454285/` ✔200<br>`unsplash.com/photos/a-close-up-of-a-pantone-book-with-color-swatches-7RQsi6bxJT4` · Mourizal Zativa | Pexels · PX<br>Pixabay · PB<br>Unsplash · US | ⚠️ **PANTONE is a registered trademark of Pantone LLC.** Under Pixabay's clause a visible Pantone logo is disallowed for commercial use; on Pexels it is allowed but still implies an affiliation. **Crop out the wordmark**, keep only the colour chips. Pixabay 3862769 (an actual CMYK press sheet) is the safest and most on-topic — no marks at all |
| **SVC-01** Technician servicing a machine | `teknik-servis.html` hero | Pexels `engineer repairing machine`, `technician maintenance factory` | **37668423** · *Engineer Inspecting Machinery in Industrial Setting* · abdo alshreef · **7008×4672** ⭐<br>34054471 · *Technician Repairing Industrial Machinery Indoors* · Bulat843 · 2094×3722<br>35072810 · *Male Technician Working on Industrial Machinery* · Bulat843 · 2187×3890 | Pexels · PX | 37668423 is the only one with hero-grade resolution. The Bulat843 series is 9:16 phone-shot — perfect for mobile cards, useless for a desktop hero. ⚠️ Faces visible in the Bulat843 set → crop to hands/torso, and never caption as Maven staff |
| **SVC-02** Mechanism macro | `teknik-servis.html` detail band; section breaks | Pexels `industrial machine detail`, `offset printing machine` | 36311180 · *Black and White Industrial Machinery Close-Up* · Peter Dyllong · 4918×3269 (native B/W)<br>9550363 · *Close-up of a Printing Machine* · Criiv India · 4000×3000<br>8865187 · *Close-Up Shot of a CNC Machine* · Daniel Smyth · 5627×3751<br>`unsplash.com/photos/industrial-printing-press-with-purple-ink-rollers-QRykXu51r_0` · Aleksandr Galichkin (@axga) · **verified free tier, no brand** | Pexels · PX<br>Unsplash · US | Macro shots are the safest imagery on the whole site — logos are almost never in frame. Lean on this slot for section dividers. QRykXu51r_0 (ink rollers) is the single most on-brief free image found |
| **COR-01** Warehouse / stock / logistics | `kurumsal.html` | Pexels `warehouse forklift boxes` | 35665496 · *Forklift Stacking Cardboard in Industrial Warehouse* · Said Alibay · 2268×4032<br>11678431 · *Stacks of Brown Boxes Near Forklift* · Mark Stebnicki · 8640×5760 ⭐ | Pexels · PX | Supports the "dealer/distributor, we hold stock" story. ⚠️ Check forklift marque (Toyota/Linde badges are common and prominent) |
| **COR-02** Substrate / media rolls | `urunler.html` consumables; texture band | Pexels `paper roll industry` | 33036772 · *Stacks of Rolled Paper Tubes in Warehouse* · Alper Murat Kırpık · 6528×4896<br>3724811 · *Stack of rolled paper between green walls* · Brett Sayles · 3822×5745<br>`unsplash.com/photos/shelves-are-stacked-with-colorful-paper-9bE9LGQvTDc` · JACQUELINE BRANDWAYN | Pexels · PX<br>Unsplash · US | Pure material, zero logo risk, zero people. Ideal full-bleed texture band behind a headline |
| **SIG-01** Signage / banner / billboard | applications; `index.html` | Pexels `banner signage`, `billboard advertising` | 4913828 · *Empty billboard on urban pavement in sunshine* · Julia Filirovska · 5411×3607 ⭐ (**blank** billboard — mock up Maven artwork into it)<br>11823077 · *Banners on a Post* · Bryce Carithers · 4728×7084<br>36890732 · *Decorative Banners Displayed at Culinary Festival* · Sóc Năng Động · 5520×3680 | Pexels · PX | **4913828 is the standout:** a blank billboard is third-party-brand-free by construction and lets us composite our own artwork — turning a licence constraint into a design opportunity. ⚠️ Reject `4700105` (Louis Vuitton billboard) and most `billboard advertising` results — they are wall-to-wall third-party brands |
| **DET-01** Colour proofing / loupe | `teknik-servis.html`; quality/colour section | Pixabay `magnifying glass thread counter`, `color chart magnifying glass` | `pixabay.com/photos/magnifying-glass-thread-counter-541626/` (CDN `photo/2014/11/22/12/01/magnifying-glass-541626_1280.jpg`) ✔200 ⭐<br>`pixabay.com/photos/color-chart-magnifying-glass-printer-1175456/` ✔200<br>12884573 · *Hot Stamping Machines on a Table* · Dana Sredojevic · 5263×5829 | Pixabay · PB<br>Pexels · PX | A linen tester on a colour bar is *the* visual shorthand for print quality control, and instantly signals "we know this industry". Both Pixabay files are ≤1280px → small editorial insets only |

**Deliberately not filled from stock: team, premises, and Maven machines.**
`kurumsal.html` team shots and `iletisim.html` office shots must be real photography or nothing —
see §2.5. Machine heroes are Blender renders per the project brief.

---

## 6. Making one visual set out of six sources

Photos from five photographers on three platforms will look like a ransom note unless they are forced
through one pipeline. The goal: **a restrained, editorial, slightly cool, high-contrast monochrome
base, with CMYK used only as accent** — so the colour on the page comes from the Maven identity, not
from whatever white balance a stranger happened to shoot at.

### 6.1 Design tokens

```css
:root{
  /* Maven ink palette */
  --ink:        #0B0B0C;   /* near-black, the "K" */
  --paper:      #F4F4F2;   /* warm off-white stock */
  --cyan:       #00A6E0;
  --magenta:    #E5007D;
  --yellow:     #FFD400;

  /* Duotone endpoints — shadow lifts to this, highlight tints to this */
  --duo-shadow: #0C1A22;   /* cyan-leaning black, not pure black */
  --duo-light:  #F2F5F6;

  /* One grade for the whole site */
  --grade: grayscale(1) contrast(1.12) brightness(0.97) saturate(0);
  --grain-opacity: 0.055;
}
```

### 6.2 Crop ratios — pick three and never deviate

| Use | Ratio | `aspect-ratio` |
|---|---|---|
| Full-bleed hero (desktop) | 21:9 | `21/9` |
| Full-bleed hero (mobile) | 4:5 | `4/5` |
| Product / application card | 3:2 | `3/2` |
| Editorial inset, portrait detail | 4:5 | `4/5` |
| Section texture band | 32:9 | `32/9` |

```css
.m-fig{ position:relative; overflow:hidden; isolation:isolate; background:var(--ink); }
.m-fig > img{ width:100%; height:100%; object-fit:cover; display:block; }
.m-fig--hero{ aspect-ratio:21/9; }
.m-fig--card{ aspect-ratio:3/2; }
.m-fig--band{ aspect-ratio:32/9; }
@media (max-width:768px){ .m-fig--hero{ aspect-ratio:4/5; } }
```

`object-fit:cover` + a fixed `aspect-ratio` is what actually makes mismatched source images agree.
Everything else is refinement. Note several §5 candidates are 9:16 phone shots (Bulat843) and several
are 2:3 portrait — the ratio box absorbs both.

### 6.3 Duotone (the main consistency lever)

Two overlays on a desaturated image: a **dark colour in `screen`** lifts the blacks, a **light colour
in `multiply`** tints the whites. That is a true duotone, and it makes a Bangladeshi press room and a
Brazilian screen-print studio look like the same shoot.

```css
.m-fig--duo > img{ filter:var(--grade); }
.m-fig--duo::before,
.m-fig--duo::after{ content:""; position:absolute; inset:0; pointer-events:none; }
.m-fig--duo::before{ background:var(--duo-shadow); mix-blend-mode:screen; }
.m-fig--duo::after { background:var(--duo-light);  mix-blend-mode:multiply; }
```

CMYK accent variants — use sparingly, one per page maximum, to tie a section to a product family:

```css
.m-fig--duo.is-cyan::before   { background:#06222E; }
.m-fig--duo.is-magenta::before{ background:#2A0518; }
.m-fig--duo.is-yellow::before { background:#2A2205; }
```

For a stronger, more controllable transform, use an inline SVG filter (better tonal control than
blend modes, and it composites in one pass):

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <filter id="maven-duo" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values="0.2126 0.7152 0.0722 0 0
                                         0.2126 0.7152 0.0722 0 0
                                         0.2126 0.7152 0.0722 0 0
                                         0      0      0      1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.047 0.949"/>
      <feFuncG type="table" tableValues="0.102 0.961"/>
      <feFuncB type="table" tableValues="0.133 0.965"/>
    </feComponentTransfer>
  </filter>
</svg>
```

```css
.m-fig--duo-svg > img{ filter:url(#maven-duo) contrast(1.08); }
```

`tableValues="<shadow> <highlight>"` per channel — those numbers are `--duo-shadow` `#0C1A22` and
`--duo-light` `#F2F5F6` normalised to 0–1. Change the palette in one place, the whole site follows.

### 6.4 Grain

A single tiling grain over every image kills the residual difference in sensor noise and JPEG
history between sources. Pure CSS, no asset request:

```css
.m-fig::after{
  /* when not using duotone's ::after — otherwise put grain on a child span */
  content:"";
  position:absolute; inset:0; pointer-events:none; z-index:2;
  opacity:var(--grain-opacity);
  mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'>\
<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/>\
<feColorMatrix type='saturate' values='0'/></filter>\
<rect width='140' height='140' filter='url(%23n)'/></svg>");
  background-size:140px 140px;
}
```

Note `stitchTiles='stitch'` — without it the 140px tile seams visibly. Keep opacity ≤0.06; above that
it reads as a filter, not as film.

### 6.5 Colour-in on interaction

Restraint pays off: keep everything monochrome, and let colour arrive only on hover. It makes the
CMYK identity feel like a deliberate signal rather than decoration, and it pairs with the sliding
underline micro-interaction already specified.

```css
.m-fig--reveal > img{ filter:var(--grade); transition:filter .5s cubic-bezier(.2,.7,.2,1); }
.m-fig--reveal:hover > img,
.m-fig--reveal:focus-within > img{ filter:grayscale(0) contrast(1.04) saturate(1.02); }
.m-fig--reveal:hover::before,
.m-fig--reveal:focus-within::before{ opacity:0; transition:opacity .5s; }

@media (prefers-reduced-motion:reduce){
  .m-fig--reveal > img{ transition:none; }
}
```

### 6.6 Pre-processing before the grade

Do this once per asset at download time, not in CSS:

1. **Straighten and crop to the target ratio** — never rely on `object-fit` to fix a crooked horizon.
2. **Neutralise white balance.** The single biggest source of mismatch; the tungsten press rooms
   (Somogro series) run very warm, the workshop shots cool. Since the base grade is `saturate(0)` this
   mostly cancels itself, but it matters for the `--reveal` hover state.
3. **Match mid-tone luminance** across a row of cards — aim for a mean luma of roughly 0.38–0.45 on
   the graded output. Cards at wildly different exposure are what actually breaks a grid.
4. **Strip EXIF** (privacy — several candidates carry GPS) and **strip the colour profile after
   converting to sRGB**. A stray Adobe RGB profile will render dull in some browsers.

---

## 7. Ink and consumables imagery — the genuinely hard slot

This is worth calling out because it is the one place where free stock will fail us, and it is
commercially central: Maven sells inks and consumables, not just machines.

**What actually exists (verified):**

- **Pixabay is the only source with real print-industry ink.** `1602896` (*Ink Paints / printing inks*)
  and `1602900` (*Paint Bucket / print / printing house*) are genuine ink cans in a working print
  house. `3862769` is a real CMYK offset press sheet. `585262` is ink on a press. **All capped at
  1280px** — Pixabay's older uploads are simply not high-resolution.
- **Pexels ink results are overwhelmingly the wrong industry.** Searching `ink bottle color` returns
  *tattoo* inks (`17865796`, `17865797`), *fountain-pen* ink (`10474474`, `7333604`), and artist's
  acrylics (`19882376`). The one strong industrial candidate is `7639358` (*Color Ink Cartridge*,
  4241×2829, tagged Cyan/Magenta/Yellow, no manufacturer named).
- **Unsplash `ink bottle` is entirely calligraphy and inkwells** — quills, notebooks, fountain pens
  (`bBV9kt-rC4c`, `Efeo3Zm4O5Q`, `zBNWdiF-ZBI`). Wrong century. `1dKq68DpVWs` (jars of coloured
  liquid) is the only usable frame, and only as an abstract.
- **Wide-format ink specifically — 1-litre pouches, 2-litre cartridges, bulk-ink systems, eco-solvent
  and UV-LED bottles — does not exist in free stock at all.** Every image of one on the open web is
  an OEM product shot (Roland/Mimaki/Epson), i.e. someone else's copyrighted marketing asset with
  someone else's trademark on it. There is no free-licensed substitute.

**Be blunt about it: the ink category cannot be photographed from free stock. It has to be rendered.**

**Recommended fallback — and it is the better answer anyway:**

1. **Render the consumables in Blender alongside the machines.** We are already building a glTF
   pipeline for the machine models. An ink pouch, a 1L bottle, a cartridge and a media roll are
   trivial geometry — a box, a cylinder, a bevel — and 90% of the work is the label and the material.
   Model one generic bottle, one pouch, one cartridge; reuse with different label textures.
2. **Design the labels as Maven artwork** — our own typography, our own CMYK chips, our own "M." mark.
   This converts the constraint into brand equity: every ink photo on the site becomes a Maven asset
   we own outright, with zero licence risk, and it *looks* like a real product line.
3. **Standardise the render setup** so consumables and machines share a look: same 3-point HDRI, same
   `--paper` seamless background, same camera focal length (85mm equivalent, shallow-ish DOF), same
   floor shadow. Render at 2400px on the long edge, then push through the §6 grade so they sit with
   the photography.
4. **Use the four verified Pixabay/Pexels ink photos only as *context* shots** — ink in a working
   environment, a press sheet, a technician handling a container — never as the product hero. Their
   ≤1280px ceiling makes that the only honest use anyway.
5. A **CMYK ink-drop / liquid macro** is an excellent abstract for the category header and is easy to
   render or shoot ourselves (ink in water, backlit, 1/1000s). Cheaper than sourcing it.

---

## 8. Technical delivery

### 8.1 Format strategy

AVIF support is **93.42% globally** (caniuse.com/avif, checked 2026-07-28): Chrome 85+, Edge 121+,
Firefox 93+, Safari 16.4+ desktop / iOS 16.0+, Samsung Internet 14+. No IE, no Opera Mini.

Serve a three-tier `<picture>`. Do **not** ship raw JPEG at hero size.

```html
<figure class="m-fig m-fig--hero m-fig--duo">
  <picture>
    <source type="image/avif"
            srcset="/img/hero-print-floor-640.avif   640w,
                    /img/hero-print-floor-960.avif   960w,
                    /img/hero-print-floor-1280.avif 1280w,
                    /img/hero-print-floor-1600.avif 1600w,
                    /img/hero-print-floor-1920.avif 1920w,
                    /img/hero-print-floor-2560.avif 2560w"
            sizes="100vw">
    <source type="image/webp"
            srcset="/img/hero-print-floor-640.webp   640w,
                    /img/hero-print-floor-960.webp   960w,
                    /img/hero-print-floor-1280.webp 1280w,
                    /img/hero-print-floor-1600.webp 1600w,
                    /img/hero-print-floor-1920.webp 1920w,
                    /img/hero-print-floor-2560.webp 2560w"
            sizes="100vw">
    <img src="/img/hero-print-floor-1280.jpg"
         width="2560" height="1097"
         alt="Maven baskı üretim alanında çalışan geniş format makineleri"
         fetchpriority="high" decoding="async">
  </picture>
</figure>
```

`width`/`height` must be the **intrinsic ratio** of the delivered crop (2560×1097 = 21:9), not the
source file's dimensions. This is what reserves layout space and holds CLS at 0.

### 8.2 Breakpoints

Full-bleed (`sizes="100vw"`): **640, 960, 1280, 1600, 1920, 2560**. Six steps covers 1× phones
through 2× laptops and 1440p desktops without generating dead weight. Skip 3200/3840 — a 21:9 hero at
3840 is >400 KB even in AVIF and buys nothing perceptible.

Cards in a 3-up grid (`sizes="(max-width:768px) 100vw, (max-width:1200px) 50vw, 33vw"`):
**400, 600, 800, 1200**.

Editorial insets (`sizes="(max-width:768px) 100vw, 45vw"`): **480, 720, 960**.

### 8.3 LCP budget

Target: **LCP ≤ 2.5 s at the 75th percentile**, per web.dev/articles/lcp ("Good LCP values are 2.5
seconds or less, poor values are greater than 4.0 seconds"). The hero `<img>` is the LCP element on
`index.html`.

| Asset | Format | Budget |
|---|---|---|
| Hero @1920w | AVIF q45–50 | **≤ 160 KB** (hard ceiling 200 KB) |
| Hero @1920w | WebP q72 | ≤ 280 KB |
| Hero @1280w | AVIF | ≤ 90 KB |
| Card @800w | AVIF | ≤ 55 KB |
| Inset @720w | AVIF | ≤ 40 KB |
| **Total images above the fold** | — | **≤ 250 KB** |

Because the grade is monochrome (§6), AVIF compresses far better than these numbers assume —
desaturated images carry almost no chroma data. Expect the 1920w hero around 100–130 KB in practice.
That is a real, free win from the art direction.

Preload the hero. Without this the browser cannot start the fetch until CSS resolves:

```html
<link rel="preload" as="image"
      imagesrcset="/img/hero-print-floor-1280.avif 1280w,
                   /img/hero-print-floor-1920.avif 1920w,
                   /img/hero-print-floor-2560.avif 2560w"
      imagesizes="100vw" type="image/avif" fetchpriority="high">
```

Also: **no CSS `background-image` for the hero.** Background images are discovered late and cannot be
preloaded via `srcset`. Use `<img>` + `object-fit:cover` (§6.2) — that is precisely why the ratio box
is built that way.

### 8.4 Lazy-loading rules

| Position | Attributes |
|---|---|
| Hero / LCP | `fetchpriority="high"`, `decoding="async"`, **no** `loading="lazy"` |
| Anything else above the fold | `decoding="async"`, no `loading` attribute (defaults to eager) |
| Below the fold | `loading="lazy" decoding="async"` |
| Carousel slide 1 | eager, `fetchpriority="high"` if it is the LCP element |
| Carousel slides 2–n | `loading="lazy"` |
| 3D model poster frame | eager (it is what the user sees before the glTF loads) |

Never put `loading="lazy"` on the LCP image — it demotes fetch priority and is a common self-inflicted
LCP regression.

For the product-page carousel, preload only the *next* slide on interaction rather than eager-loading
the set. And gate the three.js/glTF payload behind an intersection observer or an explicit
"3D görünüm" button — a machine model will dwarf every image on the page, and it must not compete
with the LCP image for bandwidth.

### 8.5 Generation pipeline

`sharp` (libvips) — one script, deterministic, no service dependency:

```js
// tools/build-images.mjs   →  node tools/build-images.mjs
import sharp from 'sharp';
import { readdir, mkdir } from 'node:fs/promises';
import path from 'node:path';

const SRC = 'assets/originals';
const OUT = 'img';
const WIDTHS = [640, 960, 1280, 1600, 1920, 2560];

await mkdir(OUT, { recursive: true });

for (const file of await readdir(SRC)) {
  const base = path.parse(file).name;
  const input = path.join(SRC, file);

  for (const w of WIDTHS) {
    const pipe = sharp(input)
      .rotate()                                   // honour EXIF orientation, then drop it
      .resize({ width: w, withoutEnlargement: true })
      .toColorspace('srgb');

    await pipe.clone().avif({ quality: 48, effort: 6 })
      .toFile(`${OUT}/${base}-${w}.avif`);
    await pipe.clone().webp({ quality: 72 })
      .toFile(`${OUT}/${base}-${w}.webp`);
  }

  await sharp(input).rotate().resize({ width: 1280 })
    .jpeg({ quality: 78, mozjpeg: true, chromaSubsampling: '4:2:0' })
    .toFile(`${OUT}/${base}-1280.jpg`);            // universal fallback
}
```

`sharp` strips EXIF (including GPS) by default unless `withMetadata()` is called — which satisfies
§6.6 step 4 for free. `effort: 6` roughly doubles encode time versus the default but cuts AVIF size
another 8–12%; worth it for a build that runs rarely.

### 8.6 Vercel caching

Static files are **automatically cached on Vercel's CDN for the lifetime of the deployment**, and
"if a static file is unchanged, the cached value can persist across deployments due to the hash used
in the filename" (vercel.com/docs/caching/cdn-cache).

Our filenames are not content-hashed, so pin the headers explicitly. Because every filename encodes
its width and the content never changes in place, `immutable` is safe:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "headers": [
    {
      "source": "/img/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

One year is Vercel's documented maximum cache time. If an image must be replaced, change the filename
(e.g. `-v2`) rather than the bytes — that is the whole contract `immutable` implies.

---

## 9. Compliance artefacts to build

Even though **no source in our shipping set requires attribution**, a client-facing corporate site
should be able to prove provenance on demand. Two files, both cheap:

**`assets/originals/MANIFEST.json`** — one record per image, committed alongside the originals:

```json
[
  {
    "slot": "HERO-01",
    "file": "hero-print-floor.jpg",
    "source": "Pexels",
    "license": "Pexels License",
    "license_url": "https://www.pexels.com/license/",
    "page": "https://www.pexels.com/photo/modern-printing-facility-interior-with-workers-31788399/",
    "photographer": "Manuel Campagnoli",
    "photographer_url": "https://www.pexels.com/@work2survive",
    "downloaded": "2026-07-28",
    "attribution_required": false,
    "checks": { "license_tier": "free", "ai_generated": false, "third_party_marks": "none", "identifiable_faces": "distant only" }
  }
]
```

The `checks` block is the §3 checklist, recorded. If a client ever asks "where did this come from",
the answer is one file away — and if a photographer's licence terms change, we know exactly which
assets are affected.

**A colophon** — a short credits block in the footer of `kurumsal.html`, or a `/renkler-ve-gorseller`
page: *"Görseller: Pexels, Unsplash ve Pixabay katkıda bulunanları. Makine görselleri Maven
tarafından üretilmiştir."* Costs nothing, reads as professional, and pre-empts the question.

---

## 10. Decisions this track hands to the build

1. **Pexels is the primary source (~65%), Unsplash secondary (~25%), Pixabay for ink only (~10%).**
   Openverse and Wikimedia Commons are excluded from the shipping set.
2. **Reject every `@ai25studioai` image** — 17 IDs, and they rank top-3 for our best queries.
3. **On Unsplash, verify "Free to use under the Unsplash License" on every photo page.** ~5 of the
   top results per industrial query are paid Getty/Unsplash+.
4. **Zero third-party manufacturer marks anywhere.** This is a commercial rule (passing off), not
   only a licence rule, and it is why §5 favours macro and material shots.
5. **No stock people presented as Maven staff, and no faces on `kurumsal`/`iletisim`.**
6. **The ink category is rendered in Blender, not photographed.** Free stock does not contain
   wide-format ink, and the render is the better asset anyway.
7. **One duotone grade + one grain overlay + three crop ratios** across every photograph, colour
   arriving only on hover.
8. **AVIF → WebP → JPEG `<picture>`, six hero widths (640–2560), hero preloaded with
   `fetchpriority="high"`, ≤160 KB at 1920w, LCP ≤2.5 s p75.**
9. **`Cache-Control: public, max-age=31536000, immutable` on `/img/(.*)` in `vercel.json`;** replace
   images by renaming, never in place.
10. **Ship `MANIFEST.json` with a recorded §3 clearance check per asset.**

---

*Compiled 2026-07-28. Licence quotations are verbatim from the pages cited. Candidate image
existence verified by HTTP as described in §0 — but every image still needs the §3 visual check by a
human before it ships.*
