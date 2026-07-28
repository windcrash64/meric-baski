# Track 6 — Design Direction & Micro-Interactions

**Project:** Maven — corporate identity site for a Turkish digital-printing-machine + ink dealer
**Repo:** `C:/claude/projects/meric-baski`
**Constraints this doc respects:** static output (Vercel), TR default + EN, scale to more locales, mobile + desktop.
**Date:** 2026-07-28
**Status of claims:** everything marked ✅ VERIFIED was checked live in this session (browser render, font binary inspection, or an API response). Everything else is cited.

---

## 0. The one-paragraph brief

Maven should look like **a precision instrument's documentation, not a brochure**. Black ink on paper, hairline rules, tabular numbers, all-caps micro-labels in mono, and enormous restraint — then exactly one CMYK accent per view, used as a *mark* (a rule, a square, a swept underline), never as decoration. Motion is **linear and mechanical, not bouncy**: things slide, sweep and wipe along axes; nothing springs, nothing floats. The CMYK pixel cluster from the logo is the only place all three process colours are allowed to touch. If a section could appear on a Webflow template for a dental clinic with the colours swapped, it is wrong.

---

## 1. Reference sites — what to steal, specifically

I browsed these live rather than quoting listicles. Screenshots were captured during research.

### 1.1 Durst Virtual Showroom — `https://showroom.durst-group.com/en/P5-350-HS` ✅ VERIFIED (browsed)

**This is the single most valuable reference in this document.** It is a direct competitor-class vendor doing exactly the product page we have to build.

What it does, precisely:

- **50/50 split product page.** Left half = the machine on pure white with **callout hotspot labels** leadered onto machine parts (`Multitrack 6`, `Double sided printing`, `LED curing technology`, `Corrugated printing`, `Dual roll`, `Multiroll`, `Safe ink refill`). Right half = a scrolling accordion.
- **The accordion section names are literally:** `DESCRIPTION` / `TECHNICAL DATA` / `FEATURES` / `APPLICATIONS`. Steal this IA verbatim (TR: `AÇIKLAMA` / `TEKNİK VERİLER` / `ÖZELLİKLER` / `UYGULAMALAR`). Only the first is open by default.
- **Persistent sticky bottom action bar** with 4 outlined buttons + line icons: `DOWNLOADS`, `MAKE CONTACT`, `GET PRINT SAMPLES`, `REQUEST LIVE DEMO`. This is the highest-value steal after the accordion — a machine page's job is to produce an enquiry, and Durst keeps the four conversion actions nailed to the viewport bottom at all times.
- **All-caps breadcrumb with `>` separators**: `VIRTUAL SHOWROOM > LARGE FORMAT PRINTING > P5 350/HS`.
- Zero rounded corners, zero drop shadows, 1px black hairlines only, pure `#FFF` ground.
- **The only colour on the entire page is the CMYK ink strip on the machine itself.** Colour comes from the product, not the chrome. This is exactly the discipline we want, and it validates the palette rule in §3.

**Steal:** the four-section accordion names, the sticky 4-action bar, the hotspot-annotated machine, breadcrumb style, and the "colour comes from the product" rule.
**Don't steal:** their body copy is a wall of unbroken text with missing spaces after full stops ("technology.With a printing width"). Their type is also cramped at small sizes.

### 1.2 swissQprint — `https://www.swissqprint.com/ch/en/` ✅ VERIFIED (browsed)

- **Top-level nav is `Printers · Applications · Inks · Showcases · Company`.** This is the IA precedent that matters most for us: a machine vendor who also sells consumables puts **`Inks` as a first-class top-level nav item**, not buried under products. Our client sells machines *and* inks — mirror this (`Makineler · Uygulamalar · Mürekkepler · Referanslar · Kurumsal`).
- Huge, *light-weight* centred display type; a single pill CTA (`Let's meet in person ›`) with a chevron.
- One accent colour only (a red, used solely in the logo's `Q`).

**Steal:** the nav IA, the "Inks as top-level" decision, single-accent discipline, chevron-suffixed CTA.
**Don't steal:** the homepage visual language itself is soft and generic — light-grey pill buttons, centred everything, rounded corners. It reads corporate-safe, not engineered. We are aiming harder than this.

### 1.3 Teenage Engineering — `https://teenage.engineering/` ✅ VERIFIED (browsed + computed styles read)

The canonical "engineered, not templated" site.

- Computed body style read live: `font-size: 23.5px`, `line-height: 35.27px` (**ratio exactly 1.5**), `color: #000`, `background: #fff`. **Their body text is set enormous.** Most B2B sites set 16px body; TE sets ~23px. Large body copy on a white ground is a large part of why it reads confident.
- Nav is **pictogram-led**: each nav group has a hand-drawn geometric icon above it, with a sub-list of small links beneath (`products → instruments / audio / designs`). No nav bar, no underlines, no hover chrome.
- Pure black on pure white, one flat colour block at a time.

**Steal:** oversized body copy (we'll land ~19–20px, see §2.4), the icon-over-nav-group idea for the mega-menu, absolute black/white discipline.
**Don't steal:** their playfulness (rounded display face, orange coupon) — wrong register for industrial B2B.

### 1.4 Awwwards "minimal" collection — `https://www.awwwards.com/websites/minimal/` ✅ VERIFIED (fetched)

Current entries worth a look for motion craft (fetched live 2026-07-28): `monolayer.dev`, `bamlab.ch`, `fmrg.studio`, `cantor8.io`, `evolt.dev`, `jera-capital.com`, `coffee-tech.com` (Developer Award + SOTD, 2026-07-16), `houseofhoney.com` (Developer Award + SOTD, 2026-07-14), `mountstreetprinters.com`.

⚠️ **Caveat, stated honestly:** I fetched this list live but only deep-browsed `mountstreetprinters.com`, which turned out to be a *luxury stationery* printer — warm, craft, pastel. Not our register; I would not lean on it. Treat the rest of this list as a shortlist to review by eye, not as verified recommendations.

⚠️ **The Awwwards `/websites/industrial/` collection is keyword-matched, not curated** — it returns `Chrome Industries`, `Blink Industries`, `Beauty For All Industries` etc. Sites that merely have "industrial" in the *name*. It is useless for this purpose. Don't waste time there.

### 1.5 Named in trade press, not personally verified

`iCOMAT` (Bristol aerospace composites) is repeatedly cited as an Awwwards-recognised industrial site using a clinical, minimal interface with generous whitespace and high-definition production imagery ([valmax.agency](https://valmax.agency/insights/best-manufacturing-websites-of-2026/)). I did not browse it; verify before copying.

---

## 2. Typography

### 2.1 The Turkish problem, solved properly

This is the section most likely to be got wrong, so it was verified against font binaries and a live browser render rather than assumed.

#### Finding A — Turkish **requires** the `latin-ext` subset ✅ VERIFIED

I pulled the live Google Fonts CSS2 response with a modern UA and read the actual `unicode-range` declarations:

```
/* latin */
unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA,
               U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, ...

/* latin-ext */
unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF,
               U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, ...
```

Mapping the Turkish alphabet against those ranges:

| Char | Codepoint | In `latin`? | In `latin-ext`? |
|---|---|---|---|
| ç Ç ö Ö ü Ü | U+00E7/C7, F6/D6, FC/DC | ✅ yes (U+0000-00FF) | — |
| ı | U+0131 | ✅ yes (explicitly listed) | ✅ |
| **İ** | U+0130 | ❌ **NO** | ✅ |
| **ğ Ğ** | U+011F / U+011E | ❌ **NO** | ✅ |
| **ş Ş** | U+015F / U+015E | ❌ **NO** | ✅ |

**Consequence:** a site that loads only the `latin` subset renders `ğ`, `Ğ`, `ş`, `Ş` and `İ` from a *fallback font*. On a Turkish site that is roughly every third word — the text silently becomes a two-font ransom note. Curiously `ı` alone is in `latin`, which is why this bug often survives casual review: "Baskı" looks fine, "Çözümleri" looks fine, but "İşleme" and "Yağız" break.

**→ Always ship `latin` + `latin-ext`. Non-negotiable.**

#### Finding B — `text-transform: uppercase` needs `lang="tr"` ✅ VERIFIED IN BROWSER

Turkish is a *casing-locale* language: `i` uppercases to `İ` (dotted), not `I`. I rendered both cases in Chromium and screenshotted the result:

| Markup | Rendered output |
|---|---|
| `<div lang="tr" style="text-transform:uppercase">istanbul işıklı</div>` | **İSTANBUL İŞIKLI** ✅ correct — both `i` → `İ`, and `ı` → `I` |
| `<div lang="en" style="text-transform:uppercase">istanbul işıklı</div>` | **ISTANBUL IŞIKLI** ❌ wrong — `i` → `I`, losing the dot |

Our design language leans hard on all-caps micro-labels (eyebrows, nav, buttons, spec headers). **If `<html lang>` is wrong, every uppercase label on the site is misspelled in Turkish.** Set `<html lang="tr">` on TR pages and `lang="en"` on EN pages; the locale switcher must swap it.

#### Finding C — the reverse gotcha, caught in my own test page ✅ VERIFIED

My specimen page was `<html lang="tr">`, and its CSS labels used `text-transform: uppercase`. The screenshot came back reading **`ARCHİVO`**, **`GEİST`**, **`MARTİAN`**, **`TURKİSH`** — English words given Turkish casing.

**→ Latin brand names, model codes and English terms inside a Turkish page must be marked `lang="en"`** (or avoid `text-transform` on them), or `Digital`→`DİGİTAL`, `Print`→`PRİNT`. This will bite on machine model names and vendor brands, which are exactly the strings we set in caps.

```html
<p class="eyebrow" lang="en">DIGITAL PRINTING</p>   <!-- stays DIGITAL PRINTING -->
<p class="eyebrow">dijital baskı</p>                 <!-- becomes DİJİTAL BASKI -->
```

#### Finding D — glyph coverage confirmed in the shipped binaries ✅ VERIFIED

I downloaded every subset `.woff2` Google serves for each candidate and read the `cmap` table with `fontTools`, checking all 18 Turkish-relevant codepoints (`ı İ ğ Ğ ş Ş ç Ç ö Ö ü Ü â â î î û û`):

| Family | Glyphs in cmap | Turkish set |
|---|---|---|
| Inter | 1622 | ✅ COMPLETE |
| IBM Plex Sans | 778 | ✅ COMPLETE |
| Geist Mono | 762 | ✅ COMPLETE |
| JetBrains Mono | 663 | ✅ COMPLETE |
| Space Grotesk | 634 | ✅ COMPLETE |
| Geist | 604 | ✅ COMPLETE |
| Archivo | 560 | ✅ COMPLETE |
| Newsreader | 525 | ✅ COMPLETE |
| Instrument Sans | 321 | ✅ COMPLETE |
| Instrument Serif | 319 | ✅ COMPLETE |
| IBM Plex Mono | 676 | ✅ COMPLETE |

All are SIL OFL, free for commercial use. Additionally rendered live in-browser — see the specimen screenshot; `ı İ ğ Ğ ş Ş ç Ç ö Ö ü Ü â î û` all draw correctly in every face above.

#### Finding E — variable axes available on Google Fonts ✅ VERIFIED (read from `fvar`)

| Family | Axes | Note |
|---|---|---|
| **Archivo** | `wght 100–900`, **`wdth 62–125`** | Widest range of any candidate. One family covers condensed-industrial → extended-poster. |
| Instrument Sans | `wght 400–700`, `wdth 75–100` | |
| Inter | `wght 100–900`, `opsz 14–32` | |
| Geist / Geist Mono | `wght 100–900` | |
| IBM Plex Sans | `wght 100–700` | |
| JetBrains Mono | `wght 100–800` | |
| Space Grotesk | `wght 300–700` | |
| Martian Mono | `wght 100–800`, `wdth 75–112.5` | |
| Newsreader | `wght 200–800`, `opsz 6–72` | |
| **IBM Plex Mono** | **none — STATIC ONLY** | 15 static files. Budget 2 weights max. |

I rendered `DİJİTAL BASKI ÇÖZÜMLERİ` in Archivo at `wdth 62` and `wdth 125` — both hold up and look genuinely industrial. The width axis is the cheapest way to get a distinctive headline voice without a second font file.

### 2.2 Three concrete pairings (all SIL OFL, all Turkish-verified)

#### ▶ Pairing A — "Swiss Machine" — **RECOMMENDED**

| Role | Family | Config |
|---|---|---|
| Display + body | **Archivo** variable | `wght 100–900`, `wdth 62–125` |
| Spec tables, eyebrows, model numbers, nav labels | **IBM Plex Mono** | static 400 + 500 only |

**Two families total.** Archivo is a neutral American-grotesque with a genuinely industrial skeleton; the `wdth` axis gives headline drama (set display at `wdth 78–86` for a tight, machined look) while body sits at `wdth 100 / wght 400`. IBM Plex Mono carries the engineering-documentation pedigree and is unmistakably "technical" without cosplay. This pairing is disciplined, loads in two files, and reads as a system rather than a mood board. **Pick this unless there's a reason not to.**

#### ▶ Pairing B — "Editorial Contrast"

| Role | Family |
|---|---|
| Display (large only, ≥40px) | **Instrument Serif** (400 + italic only) |
| Body + UI | **Instrument Sans** variable (`wght 400–700`, `wdth 75–100`) |
| Specs / mono | **Geist Mono** variable |

More magazine than machine shop. The serif at large sizes gives the "editorial" the client asked for and creates real hierarchy contrast. Risk: Instrument Serif has only one weight — it must never be used below ~32px or for anything functional.

#### ▶ Pairing C — "Neutral Tech"

| Role | Family |
|---|---|
| Display + body | **Geist** variable (`wght 100–900`) |
| Specs / mono | **Geist Mono** variable |
| Rare pull-quotes | **Newsreader** (`opsz 6–72`) |

Maximum neutrality, superfamily coherence (Geist + Geist Mono are designed together). Risk: Geist is Vercel's typeface and is now extremely common in dev-adjacent products — it may read "AI startup" rather than "industrial supplier".

**Avoid:** Inter (correct but exhausted — it is the default-looking choice and undercuts "not templated"), Space Grotesk (its quirky `g`/`ı` fight a technical register), Poppins/Montserrat (instant template signal).

### 2.3 Self-host, don't hotlink

Do not `<link>` to `fonts.googleapis.com`. Reasons: an extra origin on the critical path, and Turkish clients increasingly ask about **KVKK** (the Turkish GDPR analogue) — serving fonts from Google leaks visitor IPs to a third party. Self-hosting also lets us subset.

Exact subsetting command (fonttools; the `latin` + `latin-ext` union plus Turkish specifics):

```bash
pyftsubset "Archivo[wdth,wght].ttf" \
  --output-file=archivo-var.woff2 --flavor=woff2 \
  --layout-features="kern,liga,calt,locl,case,tnum,frac" \
  --unicodes="U+0000-00FF,U+0100-024F,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,\
U+02DA,U+02DC,U+2000-206F,U+2074,U+20A0-20AB,U+20AC,U+2122,U+2212,U+2215" \
  --no-hinting --desubroutinize
```

- `locl` is **required** — it carries locale-specific forms including Turkish `i`/`ı` behaviour.
- `case` fixes punctuation alignment in our all-caps labels (hyphens, parentheses ride too low otherwise).
- `tnum` gives tabular figures for spec tables (§2.5).
- Keep `U+0100-024F` whole rather than cherry-picking — it's small and covers future locales (Polish, Czech, Romanian) for free, which serves the "scale to more locales" constraint.

Loading:

```html
<link rel="preload" href="/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
```
```css
@font-face{
  font-family:"Archivo"; src:url("/fonts/archivo-var.woff2") format("woff2-variations");
  font-weight:100 900; font-stretch:62% 125%; font-display:swap;
}
/* CLS guard: match fallback metrics so the swap doesn't reflow */
@font-face{
  font-family:"Archivo-fallback"; src:local("Arial");
  size-adjust:97%; ascent-override:92%; descent-override:24%; line-gap-override:0%;
}
:root{ --font-sans:"Archivo","Archivo-fallback",system-ui,sans-serif; }
```

Preload **only** the two files above the fold (display + body if separate). Preloading the mono is usually wrong — it appears in eyebrows and spec tables, mostly below the fold.

### 2.4 Type scale

Fluid, `clamp()`-based, no breakpoint jumps. Ratio ≈1.2 at mobile widening to ≈1.333 at desktop (the viewport does the work).

```css
:root{
  --step--2: clamp(0.69rem, 0.67rem + 0.11vw, 0.75rem);   /* 11→12  mono micro-labels */
  --step--1: clamp(0.83rem, 0.79rem + 0.2vw,  0.94rem);   /* 13→15  captions, spec cells */
  --step-0 : clamp(1.0rem,  0.94rem + 0.31vw, 1.19rem);   /* 16→19  BODY */
  --step-1 : clamp(1.2rem,  1.1rem  + 0.5vw,  1.58rem);   /* 19→25  lead paragraph */
  --step-2 : clamp(1.44rem, 1.28rem + 0.8vw,  2.11rem);   /* 23→34  h3 */
  --step-3 : clamp(1.73rem, 1.47rem + 1.3vw,  2.81rem);   /* 28→45  h2 */
  --step-4 : clamp(2.07rem, 1.66rem + 2.1vw,  3.75rem);   /* 33→60  h1 */
  --step-5 : clamp(2.49rem, 1.83rem + 3.3vw,  5.0rem);    /* 40→80  hero */
  --step-6 : clamp(2.99rem, 1.9rem  + 5.4vw,  6.67rem);   /* 48→107 statement/marquee */
}
```

Body lands at **19px on desktop** — deliberately larger than the B2B default of 16px, following the Teenage Engineering measurement (23.5px) but pulled back for denser technical copy.

### 2.5 Tracking, leading, and where mono earns its place

| Role | Size | Weight / width | Tracking | Leading |
|---|---|---|---|---|
| Hero / statement | `--step-5/6` | `wght 600`, `wdth 82` | **`-0.03em`** | `0.95` |
| H1 | `--step-4` | `wght 600`, `wdth 88` | `-0.025em` | `1.02` |
| H2 | `--step-3` | `wght 600` | `-0.02em` | `1.08` |
| H3 | `--step-2` | `wght 500` | `-0.015em` | `1.15` |
| Lead paragraph | `--step-1` | `wght 400` | `-0.01em` | `1.45` |
| Body | `--step-0` | `wght 400` | `0` | **`1.6`** |
| Spec table cell | `--step--1` | mono 400 | `0` | `1.5` |
| **Eyebrow / micro-label** | `--step--2` | **mono 500** | **`+0.14em`** | `1` |
| Button label | `--step--1` | `wght 500` | `+0.02em` | `1` |

**Rules:**
- **Negative tracking scales with size.** Large type needs tightening; small type needs loosening. Never apply one tracking value globally.
- **Mono is used in exactly four places** — and nowhere else, or it becomes a costume:
  1. Eyebrow / section micro-labels (`TEKNİK VERİLER`, `01 — MAKİNELER`)
  2. Spec-table values and units (`1.440 dpi`, `3.200 mm`, `12 renk`)
  3. Model / SKU codes (`MX-3200 UV`)
  4. Numeric counters and the section index numbers
- **`font-variant-numeric: tabular-nums`** on every spec table and every count-up. Without it, animated numbers jitter horizontally and spec columns fail to align.
- `text-wrap: balance` on all headings (h1–h3), `text-wrap: pretty` on paragraphs. ✅ Baseline **newly available since 2024-05-13** (Chrome 114, Firefox 121, Safari 17.5) — safe to ship, degrades to normal wrapping.

### 2.6 Turkish copy details that betray a foreign build

- **Numbers:** Turkish uses `.` for thousands and `,` for decimals — `1.440 dpi`, `3,2 m`, `0,25 s`. Format count-ups with `new Intl.NumberFormat('tr-TR')`, never a hand-rolled regex.
- **Hyphenation:** set `lang="tr"` (already required by §2.1-B) and `hyphens: auto` — Turkish is agglutinative and produces very long words (`değerlendirilebilmesi`) that will overflow narrow columns otherwise.
- Turkish body copy runs **~15–20% longer than English**. Design every card, button and nav item to survive that; test with the longest TR string, not the English one.

---

## 3. Colour — black + CMYK without the 1990s print-shop look

### 3.1 Why this is a trap

The failure mode is obvious: cyan + magenta + yellow together, at full saturation, in the chrome — that is a photocopier-shop flyer. The fix is not to desaturate the CMYK (that kills the brand); it is to **starve it of area and forbid co-occurrence**.

### 3.2 The measured problem ✅ VERIFIED (WCAG 2.x contrast computed)

I computed relative luminance and contrast ratios for the standard process colours:

| Colour | Hex | on `#FFFFFF` | Grade | on `#0B0B0C` | Grade |
|---|---|---|---|---|---|
| Process Cyan (SWOP) | `#00AEEF` | **2.53** | ❌ FAIL | **7.78** | ✅ AAA |
| Euro Cyan | `#009FE3` | 2.97 | ❌ FAIL | 6.62 | ✅ AA |
| Process Magenta (SWOP) | `#EC008C` | 4.25 | ⚠️ large/UI only | 4.63 | ✅ AA |
| Euro Magenta | `#E6007E` | 4.50 | ✅ AA (just) | 4.37 | ⚠️ large/UI |
| Process Yellow (SWOP) | `#FFF200` | **1.17** | ❌❌ FAIL | **16.82** | ✅ AAA |

**The decisive insight: the CMYK trio is a *dark-background* palette.** On white, cyan is unusable for text (2.53) and yellow is catastrophic (1.17). On near-black, cyan (7.78) and yellow (16.82) are superb. This isn't a limitation — it's the design direction. **Colour belongs in the dark sections.** Light sections stay black-on-white with colour appearing only as non-text marks.

Darkened variants for when an accent *must* carry text on white (computed, most-vivid-passing):

| Need | Hex | Ratio on white |
|---|---|---|
| Cyan, AA body text | `#00668F` | 6.37 ✅ AA |
| Cyan, AA large/UI (3:1) | `#0086C9` | 4.00 ✅ |
| Magenta, AA body text | `#A8005E` | 7.43 ✅ AAA |
| Magenta, AA large/UI | `#C7006F` | 5.74 ✅ AA |
| Yellow, AA body text | `#827821` | 4.51 ✅ AA (ugly — avoid; use black on yellow instead) |

### 3.3 The palette

```css
:root{
  /* ---- Structure (this is 92% of the site) ---- */
  --ink:        #0B0B0C;   /* near-black. NOT #000 — pure black flares on OLED */
  --paper:      #FFFFFF;
  --bone:       #F2F1ED;   /* warm off-white, alternate light section  (17.41 on ink) */
  --graphite:   #16171A;   /* raised panel on dark; only 1.10 vs ink — use a rule, not fill alone */
  --rule:       #E3E1DC;   /* hairline on light */
  --rule-dark:  #26272B;   /* hairline on dark */
  --muted:      #5A5F66;   /* secondary text on light   6.43 ✅ AA */
  --muted-dark: #9BA1A9;   /* secondary text on dark    7.56 ✅ AAA */

  /* ---- Process accents: MARKS on light, TEXT on dark ---- */
  --cyan:       #00AEEF;
  --magenta:    #EC008C;
  --yellow:     #FFF200;

  /* ---- Accessible text variants for light backgrounds ---- */
  --cyan-ink:    #00668F;  /* 6.37 ✅ links on white */
  --magenta-ink: #A8005E;  /* 7.43 ✅ */

  --focus:      #00AEEF;   /* focus ring — cyan on both grounds, see 3.5 */
}
```

⚠️ Note `--graphite` on `--ink` is only **1.10:1**. A dark panel is invisible by fill alone — it must be delimited by a `--rule-dark` hairline. This is a real trap in dark sections.

### 3.4 Usage ratios — enforce these

| Share of any given viewport | Element |
|---|---|
| **~92%** | `--ink` / `--paper` / `--bone` / `--muted` / rules |
| **~6%** | Exactly **one** process accent, chosen per section |
| **~2%** | The full CMYK trio together — **logo pixel cluster only**, plus at most one hero moment per page |

**Hard rules:**
1. **One accent per section.** Never two. Rotate down the page — cyan for `MAKİNELER`, magenta for `MÜREKKEPLER`, yellow for `TEKNİK SERVİS`. The rotation itself becomes a wayfinding system: a visitor learns "magenta = consumables".
2. **On light grounds, accents are never text.** They are: a 2px underline sweep, a 4px section rule, a 12px logo square, a chart bar, a hover fill. Text stays `--ink`; links use `--cyan-ink`.
3. **On dark grounds, accents may be text** — `--cyan` on `--ink` is AAA (7.78) and `--yellow` on `--ink` is 16.82. This is where the brand gets to shout.
4. **Yellow needs black on it, never white.** `#FFF200` + `--ink` = 16.82 ✅. `#FFF200` + white = 1.17 ❌.
5. **No gradients. No colour-tinted shadows. No glassmorphism.** A CMYK brand earns credibility from flatness — ink is flat.

### 3.5 Focus states

`--cyan` `#00AEEF` scores 2.53 on white — below the **3:1** required by WCAG 2.2 SC 1.4.11 for UI components. Solve it with a **two-tone focus ring** that works on any ground:

```css
:where(a,button,input,select,summary,[tabindex]):focus-visible{
  outline: 2px solid var(--ink);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--cyan);   /* cyan reads as brand, ink guarantees the 3:1 */
}
```
Never `outline: none` without a replacement. Use `:focus-visible`, not `:focus`, so mouse users don't see rings on click.

---

## 4. Layout system

### 4.1 Grid

- **12 columns** ≥1024px · **6 columns** 640–1023px · **4 columns** <640px.
- Container `max-width: 1440px`. Beyond that the page stops growing and margins absorb the excess — full-bleed sections still bleed.
- Gutter: `clamp(16px, 2vw, 32px)`. Page margin: `clamp(20px, 5vw, 80px)`.
- Use **CSS Grid with `subgrid`** for card internals so titles/specs/CTAs align across cards of unequal content length. ✅ Baseline **widely available since 2026-03-15** — safe to use unconditionally.
- Use **container queries** for the product card so the same component works in a 3-up grid, a 2-up related-products rail, and a full-width feature. ✅ Baseline **widely available since 2025-08-14**.

```css
.grid{ display:grid; grid-template-columns:repeat(12,1fr); gap:var(--gutter); }
@media (max-width:1023px){ .grid{ grid-template-columns:repeat(6,1fr); } }
@media (max-width:639px){  .grid{ grid-template-columns:repeat(4,1fr); } }
```

**Asymmetry is the whole game.** A templated site puts everything in a centred 8-column well. Do this instead:
- Section label (mono eyebrow) in columns **1–2**, content in **4–12**. This single move — a hanging left-margin label column — does more for "engineered" than any animation.
- Editorial text blocks at **max 68 characters** (`max-width: 68ch`), never full-width.
- Let images bleed to one edge while text stays gridded.

### 4.2 Whitespace scale

4px base, non-linear at the top (spacing should feel stepped, not continuous):

```css
--sp-1:4px;  --sp-2:8px;   --sp-3:12px;  --sp-4:16px;  --sp-5:24px;
--sp-6:32px; --sp-7:48px;  --sp-8:64px;  --sp-9:96px;  --sp-10:128px;
--sp-11:160px; --sp-12:200px;
```

Section padding: `padding-block: clamp(var(--sp-9), 12vh, var(--sp-12))` → 96px mobile, up to 200px desktop. **Generous section padding is the cheapest luxury signal there is.** Most cheap B2B sites use 48px and look cramped.

### 4.3 Section rhythm & light/dark alternation

Don't alternate every section — that produces a zebra. Use dark as **punctuation**, roughly 1 dark per 3–4 light, and always for the same *semantic* purposes:

| Section | Ground | Why |
|---|---|---|
| Hero | `--paper` | Confidence. Black type on white, huge. |
| Product categories | `--paper` | |
| **Technical / capability stats** | **`--ink`** | Dark = "specification mode". Accents finally readable (§3.2). Count-ups live here. |
| Applications / references | `--bone` | Warm shift, still light — avoids two identical white sections in a row. |
| Product detail split view | `--paper` | Machine must sit on white, like Durst. |
| **Closing CTA band** | **`--ink`** | Dark bookend; one accent CTA. |
| Footer | `--ink` | Continuous with the CTA band — no seam. |

Transitions between grounds should be **hard edges, never gradients**. A 1px `--rule` line at the boundary of two light sections; nothing at all at a light→dark boundary (the colour change is the edge).

---

## 5. Motion catalogue

### 5.1 Tokens

```css
:root{
  /* durations */
  --d-instant: 90ms;   --d-fast: 160ms;  --d-base: 240ms;
  --d-slow:   380ms;   --d-slower: 560ms; --d-page: 480ms;

  /* easings */
  --e-out:      cubic-bezier(0.16, 1, 0.30, 1);    /* signature — sharp out, long settle */
  --e-out-soft: cubic-bezier(0.25, 1, 0.50, 1);
  --e-in-out:   cubic-bezier(0.76, 0, 0.24, 1);    /* symmetrical, for page/overlay */
  --e-standard: cubic-bezier(0.20, 0, 0.00, 1);    /* Material 3 "emphasized"/"standard" */
  --e-accel:    cubic-bezier(0.30, 0, 0.80, 0.15); /* M3 emphasized-accelerate, for exits */
  --e-linear:   linear;                             /* marquee only */
}
```

Material 3's easing values (`emphasized` = `cubic-bezier(0.2, 0, 0, 1)`, `emphasized-accelerate` = `cubic-bezier(0.3, 0, 0.8, 0.15)`, `emphasized-decelerate` = `cubic-bezier(0.05, 0.7, 0.1, 1)`) are documented at [m3.material.io](https://m3.material.io/styles/motion/easing-and-duration/tokens-specs).

**No springs, no overshoot, no bounce anywhere on this site.** A machine that overshoots is a broken machine. `--e-out` is the house curve; it decelerates hard without ever exceeding its endpoint.

### 5.2 The catalogue

| # | Name | Trigger | Property animated | Duration | Easing | Reduced-motion fallback |
|---|---|---|---|---|---|---|
| 1 | **Sliding underline** (enter L → exit R) | `:hover` / `:focus-visible` on nav + inline links | `transform: scaleX()` + `transform-origin` swap | `320ms` | `--e-out` | Underline appears instantly at full width (`transition: none`); state still conveyed |
| 2 | **Button line sweep** (fill wipe) | `:hover` / `:focus-visible` on `.btn` | `transform: scaleX()` on `::before`, + `color` | `420ms` fill / `160ms` colour | `--e-out` | Instant background/colour swap, no wipe |
| 3 | **Button arrow shift** | `:hover` on CTA | `transform: translateX(0 → 4px)` on `::after` glyph | `240ms` | `--e-out` | No transform; arrow static |
| 4 | **Image clip reveal** | Enters viewport (once) | `clip-path: inset(0 0 100% 0 → 0 0 0 0)` + inner `scale(1.06 → 1)` | `900ms` mask / `1200ms` scale | `--e-out` | Element visible at rest, `opacity 0→1` in `200ms` only |
| 5 | **Staggered line reveal** | Heading enters viewport | per-line `transform: translateY(105% → 0)` inside `overflow:hidden` mask | `640ms`, stagger `70ms` | `--e-out` | All lines visible; single `opacity` fade `200ms`, no stagger, no translate |
| 6 | **Rule draw-in** | Section enters viewport | `transform: scaleX(0 → 1)`, `transform-origin: left` | `560ms` | `--e-out` | Rule rendered at full width immediately |
| 7 | **Number count-up** | Stat block enters viewport | JS-driven `textContent` via `rAF`, `Intl.NumberFormat('tr-TR')` | `1400ms` | ease-out (JS `1-(1-t)^3`) | Final value written immediately, no animation |
| 8 | **Marquee** (client logos / applications) | Always on (autoplay) | `transform: translateX(0 → -50%)` on a duplicated track | `36s` per loop | `--e-linear` | **Animation stopped**, track becomes a horizontally scrollable, scroll-snapped strip |
| 9 | **Sticky condensing header** | Scroll past 120px sentinel | `height` 88→60px, logo `scale(1 → 0.82)`, `border-bottom-color` transparent→`--rule` | `280ms` | `--e-standard` | Header switches to condensed state instantly (no transition) |
| 10 | **Header hide-on-scroll-down** | Scroll direction change | `transform: translateY(0 → -100%)` | `320ms` | `--e-in-out` | Disabled — header stays pinned |
| 11 | **Cursor-adaptive hover** (desktop only) | `pointer:fine` + hover on media/product card | custom cursor `transform: translate3d()` lerped; label `opacity`/`scale` | `lerp 0.15` / `200ms` | `--e-out` | Feature not mounted at all; native cursor + a static caption |
| 12 | **Card hover lift** | `:hover` on product card | `border-color`, thumbnail `scale(1 → 1.03)`, accent rule `scaleX(0 → 1)` | `300ms` | `--e-out` | `border-color` change only |
| 13 | **Page transition** | Same-origin navigation | `::view-transition-old/new` cross-fade + `translateY(12px)`; shared-element morph on product thumbnail | `480ms` | `--e-in-out` | `@media(prefers-reduced-motion)` → `navigation: none` (plain load) |
| 14 | **Gallery slide** | Carousel next/prev, drag, arrow keys | `transform: translate3d()` on track; CSS `scroll-snap` | `500ms` | `--e-out` | Snap-scroll retained, smooth-scroll off (`scroll-behavior: auto`) |
| 15 | **Accordion (spec panels)** | `<summary>` click | `grid-template-rows: 0fr → 1fr`, chevron `rotate(0 → 180deg)` | `340ms` | `--e-standard` | Instant open/close, no rotation |
| 16 | **Mega-menu open** | Nav hover/click (desktop) | `clip-path: inset(0 0 100% 0 → 0)` + item stagger `40ms` | `380ms` | `--e-out` | Instant show, no stagger |
| 17 | **3D model idle → engage** | Model loaded; user grabs | idle `rotation.y += 0.0015/frame`; on pointerdown → damped orbit | continuous | linear / damping `0.08` | **Idle auto-rotation off.** Model static until dragged. |
| 18 | **Section index tick** | Section enters viewport | mono index `01 → 02`, `opacity` + `translateY(6px)` | `240ms` | `--e-out` | Value swaps, no motion |

### 5.3 The signature interaction — sliding underline, exactly

The client asked for *"hover kayan buton çizgileri"*. The whole trick is that **`transform-origin` is swapped but never transitioned**, so the line grows from the left on enter and shrinks to the right on exit:

```css
.link{ position:relative; text-decoration:none; color:var(--ink); }
.link::after{
  content:""; position:absolute; left:0; right:0; bottom:-3px; height:1px;
  background:currentColor;
  transform:scaleX(0);
  transform-origin:right center;        /* ← governs the EXIT */
  transition:transform var(--d-base) var(--e-out);
}
.link:hover::after,
.link:focus-visible::after{
  transform:scaleX(1);
  transform-origin:left center;          /* ← governs the ENTER */
}
```

Enter: origin flips to `left`, scale 0→1 ⇒ sweeps in from the left.
Exit: rule reverts, origin is `right`, scale 1→0 ⇒ retracts off to the right.
It reads as one continuous line travelling left-to-right through the word. Do **not** animate `width` (layout thrash) and do **not** transition `transform-origin` (it would ruin the effect).

Accent variant — the underline in that section's process colour, 2px, sitting under a black word:

```css
.link--accent::after{ height:2px; bottom:-4px; background:var(--section-accent); }
```

Button sweep is the same mechanic scaled to a box:

```css
.btn{
  position:relative; isolation:isolate; overflow:hidden;
  border:1px solid var(--ink); background:transparent; color:var(--ink);
  padding:14px 28px; font:500 var(--step--1)/1 var(--font-sans); letter-spacing:.02em;
  transition:color var(--d-fast) var(--e-out);
}
.btn::before{
  content:""; position:absolute; inset:0; z-index:-1; background:var(--ink);
  transform:scaleX(0); transform-origin:right center;
  transition:transform 420ms var(--e-out);
}
.btn:hover, .btn:focus-visible{ color:var(--paper); }
.btn:hover::before, .btn:focus-visible::before{ transform:scaleX(1); transform-origin:left center; }
```

### 5.4 Scroll-driven reveals — technique + the honest support picture

✅ VERIFIED via the webstatus.dev Baseline API (2026-07-28):

| Feature | Baseline | Chrome | Safari | Firefox |
|---|---|---|---|---|
| **Scroll-driven animations** (`animation-timeline`) | ⚠️ **limited** | 115 (2023-07) | 26 (2025-09) | ❌ none |
| **Cross-document view transitions** | ⚠️ **limited** | 126 (2024-06) | 18.2 (2024-12) | ❌ none |
| Same-document view transitions | ✅ **newly** (2025-10-14) | 111 | 18 | 144 |
| `text-wrap: balance` | ✅ newly (2024-05-13) | 114 | 17.5 | 121 |
| `@starting-style` | ✅ newly (2024-08-06) | 117 | 17.5 | 129 |
| Subgrid | ✅ **widely** (since 2026-03-15) | 117 | 16 | 71 |
| Container queries | ✅ **widely** (since 2025-08-14) | 105 | 16 | 110 |
| `::details-content` | ✅ newly (2025-09-16) | 131 | 18.4 | 143 |
| `interpolate-size` / scroll-state queries | ⚠️ limited | 129 / 133 | ❌ | ❌ |
| `prefers-reduced-motion` | ✅ **widely** (since 2020) | 74 | 10.1 | 63 |

**Decision:** use CSS scroll-driven animations as a *progressive enhancement*, with an IntersectionObserver fallback. Firefox users get the reveal via JS; everyone else gets it off the compositor for free.

```css
@keyframes reveal-mask{
  from{ clip-path:inset(0 0 100% 0); }
  to  { clip-path:inset(0 0 0 0);    }
}
@supports (animation-timeline: view()){
  @media (prefers-reduced-motion: no-preference){
    .reveal{
      animation:reveal-mask linear both;
      animation-timeline:view();
      animation-range:entry 10% cover 35%;
    }
  }
}
```

```js
// Fallback for Firefox (and any engine without view() timelines)
if (!CSS.supports('animation-timeline: view()') &&
    !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) {
      e.target.classList.add('is-in');
      io.unobserve(e.target);           // reveal once, never re-run
    }
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}
```

**Never** drive reveals from a `scroll` event listener — that's the single biggest cause of janky "premium" sites.

### 5.5 Page transitions on a static multi-page site

Because we're static HTML on Vercel with no router, **cross-document view transitions are exactly the right tool** — they give SPA-grade transitions with zero JS and zero framework:

```css
@view-transition { navigation: auto; }   /* same-origin only */

::view-transition-old(root){ animation: vt-out var(--d-page) var(--e-in-out) both; }
::view-transition-new(root){ animation: vt-in  var(--d-page) var(--e-in-out) both; }
@keyframes vt-out{ to  { opacity:0; transform:translateY(-8px); } }
@keyframes vt-in { from{ opacity:0; transform:translateY(12px); } }

/* Shared-element morph: product thumbnail → product hero */
.product-thumb, .product-hero{ view-transition-name: var(--vt-product); }

@media (prefers-reduced-motion: reduce){
  @view-transition { navigation: none; }
}
```

Firefox simply performs an ordinary navigation. That is an acceptable, invisible degradation — no polyfill, no JS router, no risk. Requires same-origin (satisfied) and no cross-origin redirects.

### 5.6 Sticky condensing header

`scroll-state()` container queries would do this in pure CSS but are **Chrome-only (133+)**, so use a sentinel:

```js
const sentinel = document.querySelector('#header-sentinel'); // 1px div at page top
new IntersectionObserver(
  ([e]) => document.documentElement.classList.toggle('is-condensed', !e.isIntersecting),
  { threshold: 0 }
).observe(sentinel);
```
Zero scroll listeners. Animate `height`, logo `scale` and `border-bottom-color` — never `position` or `top`.

### 5.7 Desktop-only cursor behaviour

Gate on capability, not width — a Surface at 1400px is touch-capable, an iPad Pro reports large widths:

```css
@media (hover:hover) and (pointer:fine){ .cursor{ display:block; } }
```
```js
if (matchMedia('(hover:hover) and (pointer:fine)').matches &&
    !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  mountCustomCursor();     // never even loaded on touch
}
```
Keep it restrained: a small `mix-blend-mode: difference` disc that scales up over media and shows a mono label (`SÜRÜKLE`, `GÖRÜNTÜLE`). Lerp at `0.15` — a cursor that tracks 1:1 is pointless, one that lags too far feels broken.

### 5.8 Reduced motion — the correct implementation

The common `*{animation:none!important}` sledgehammer is wrong: it breaks loading spinners and any state conveyed *only* by motion. WCAG 2.3.3 (Animation from Interactions, AAA) asks that non-essential motion be removable; **opacity fades are not vestibular triggers** — movement, scaling, parallax and rotation are. So keep fades, kill travel.

```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:.01ms !important;
    animation-iteration-count:1 !important;
    transition-duration:.01ms !important;
    scroll-behavior:auto !important;
  }
  /* re-permit non-vestibular fades */
  .reveal,.stagger-line{
    animation:none !important; transform:none !important; clip-path:none !important;
    opacity:1 !important; transition:opacity 200ms linear !important;
  }
  .marquee__track{ animation:none !important; }
  .marquee{ overflow-x:auto; scroll-snap-type:x mandatory; }
}
```

Mirror it in JS for anything script-driven, and **respond to changes live** (users toggle it mid-session):

```js
const rm = matchMedia('(prefers-reduced-motion: reduce)');
rm.addEventListener('change', applyMotionPrefs);
```

⚠️ **WCAG 2.2.2 (Pause, Stop, Hide — Level A)** applies to the marquee: any automatic motion lasting more than 5 seconds needs a user-accessible pause control. `prefers-reduced-motion` alone does **not** satisfy this. Ship a visible pause/play toggle on the marquee, or don't autoplay it.

---

## 6. What makes B2B manufacturing sites look cheap — anti-patterns

Explicit ban list. Every one of these is a signal buyers read as "small, unserious, or outsourced".

**Imagery**
1. **Stock photos of people in hard hats / shaking hands / pointing at monitors.** The most reliable cheapness signal in the sector. Industrial buyers detect and discount stock photography, and it measurably lowers trust ([blendb2b.com](https://www.blendb2b.com/resources/best-manufacturing-website-designs), [lowcode.agency](https://www.lowcode.agency/blog/how-outdated-b2b-website-design-hurts-enterprise-deals)). Use real machines, real substrates, real print output, real service vans, real workshop.
2. Machines composited onto fake gradient backgrounds with drop shadows. Shoot or render on white; keep the shadow contact-only or absent.
3. Mixed image treatments — some cut-out, some photographed, some rendered — on the same grid.
4. Low-res vendor JPEGs upscaled. If the vendor asset is bad, render the machine ourselves (we're building a glTF anyway — render stills from it for perfect consistency).

**Typography**
5. Poppins / Montserrat / Raleway headings. Instant "template" tell.
6. Centred paragraphs of body copy.
7. `text-transform: uppercase` with default tracking (`0`). Caps *always* need positive tracking.
8. Three or more type families.
9. **Turkish text with fallback-font `ğ ş İ`** (§2.1-A) — looks like a broken machine translation.
10. **`ISTANBUL` instead of `İSTANBUL`** in caps labels (§2.1-B).

**Colour & surface**
11. Blue-to-cyan gradient hero. The default "tech" cliché.
12. Coloured drop shadows, glow, glassmorphism, neumorphism.
13. More than one accent colour in a viewport (§3.4).
14. Yellow text on white (1.17:1) or cyan body text on white (2.53:1).
15. Border-radius everywhere. Machines are extruded aluminium; keep radii at `0` (or `2px` maximum, applied consistently).

**Layout**
16. Everything centred in an 8-column well with 48px section padding.
17. **A 3-across "feature card" row with a circular icon, a two-word title, and a sentence of filler** — the single most template-coded pattern in B2B.
18. Full-width carousels of nothing (hero sliders auto-advancing through three near-identical images).
19. Cards with unequal internal alignment (fix with `subgrid`, §4.1).
20. No spec table. An industrial buyer's first question is "what are the numbers?" — burying specs in a PDF costs enquiries.

**Motion**
21. Bouncy/spring easing, `ease-in-out` on everything, or 800ms hover transitions.
22. Fade-up-on-scroll applied to *every* element, re-triggering each time it re-enters view.
23. Parallax hero backgrounds.
24. AOS/WOW.js-style libraries with default 1000ms delays.
25. Motion with no reduced-motion path.
26. Auto-rotating 3D model that never stops — it fights the user the moment they try to orbit (§5.2 #17).

**Content & trust**
27. "Leading provider of innovative solutions" boilerplate above the fold.
28. Fake/anonymous testimonials, or logo walls of clients who aren't clients.
29. Contact page with a form and nothing else — industrial buyers want a **phone number, a WhatsApp link, a physical address with a map, and a named person**.
30. No visible pricing *direction*, no lead times, no service-coverage statement. Ambiguity reads as evasion.
31. English-first with a machine-translated Turkish page. For this client TR is primary; EN is the translation.
32. Broken/absent favicon, no OG image, `title` tags reading "Home".

---

## 7. Implementation checklist for the build

- [ ] `<html lang="tr">` on TR pages, `lang="en"` on EN — **and** `lang="en"` on Latin brand/model strings inside TR pages (§2.1-B/C).
- [ ] Self-host `latin` + `latin-ext` subsets with `locl,case,tnum,kern,liga,calt`; preload 2 files max (§2.3).
- [ ] `font-variant-numeric: tabular-nums` on all spec tables and counters.
- [ ] Ship the Durst IA on product pages: `AÇIKLAMA / TEKNİK VERİLER / ÖZELLİKLER / UYGULAMALAR` + sticky 4-action bar (§1.1).
- [ ] `Mürekkepler` (Inks) as a top-level nav item (§1.2).
- [ ] One accent per section; rotate cyan → magenta → yellow down the page (§3.4).
- [ ] Two-tone focus ring; audit every interactive element (§3.5).
- [ ] Dark sections only for stats/spec and the closing CTA band (§4.3).
- [ ] `@view-transition { navigation: auto; }` + reduced-motion `none` (§5.5).
- [ ] Scroll reveals behind `@supports (animation-timeline: view())` with IO fallback; reveal **once** (§5.4).
- [ ] Marquee pause control for WCAG 2.2.2 (§5.8).
- [ ] Custom cursor mounted only under `(hover:hover) and (pointer:fine)` (§5.7).
- [ ] 3D model: no idle auto-rotation under reduced motion (§5.2 #17).
- [ ] Test every layout with the **longest Turkish string**, not the English one (§2.6).

---

## 8. Sources

Browsed live in this session:
- Durst Virtual Showroom — https://showroom.durst-group.com/en/P5-350-HS
- swissQprint — https://www.swissqprint.com/ch/en/
- Teenage Engineering — https://teenage.engineering/
- Awwwards, Minimal collection — https://www.awwwards.com/websites/minimal/
- Awwwards, "Industrial" collection (found to be keyword-matched, not curated) — https://www.awwwards.com/websites/industrial/
- Mount Street Printers — https://mountstreetprinters.com/

APIs / binaries inspected:
- Google Fonts CSS2 API (`unicode-range` per subset) — https://fonts.googleapis.com/css2
- Google Fonts family metadata — https://fonts.google.com/metadata/fonts/Inter
- Shipped `.woff2` `cmap` + `fvar` tables read with `fontTools` 4.63.0
- Web Platform Status (Baseline) API — https://api.webstatus.dev/v1/features
- caniuse feature JSON — https://github.com/Fyrd/caniuse

Documentation:
- MDN, `@view-transition` — https://developer.mozilla.org/en-US/docs/Web/CSS/@view-transition
- MDN, `animation-timeline` — https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline
- Material Design 3, easing & duration tokens — https://m3.material.io/styles/motion/easing-and-duration/tokens-specs

Trade commentary (secondary, treat as directional):
- https://www.blendb2b.com/resources/best-manufacturing-website-designs
- https://www.lowcode.agency/blog/how-outdated-b2b-website-design-hurts-enterprise-deals
- https://valmax.agency/insights/best-manufacturing-websites-of-2026/
- https://www.bartleyndick.com/blog/manufacturing-website-design-content-mistakes/
