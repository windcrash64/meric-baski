#!/usr/bin/env bash
# Download and subset the two webfonts.
#
# Turkish is the reason this script exists: 'İ' (U+0130), 'ğ/Ğ' (U+011F/011E)
# and 'ş/Ş' (U+015F/015E) live in latin-ext, NOT latin. Only 'ı' (U+0131) is in
# latin — which is why a site can look fine in review and still be misspelling
# every other Turkish capital.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/tools/.venv/Scripts/python.exe"
SRC="$ROOT/tools/.fontsrc"
OUT="$ROOT/public/fonts"

mkdir -p "$SRC" "$OUT"

# uv-created venvs deliberately ship without pip, so install through uv.
uv pip install --quiet --python "$PY" "fonttools[woff]>=4.55" brotli

fetch() {
  local url="$1" dest="$2"
  [ -s "$dest" ] && return 0
  echo "  fetch $(basename "$dest")"
  curl -fsSL --retry 3 -o "$dest" "$url" || return 1
}

# google/fonts is the canonical upstream for both families and carries the OFL
# alongside each. The per-family repos have moved their paths more than once.
GF="https://raw.githubusercontent.com/google/fonts/main/ofl"

echo "downloading sources"
fetch "$GF/archivo/Archivo%5Bwdth%2Cwght%5D.ttf" "$SRC/archivo-var.ttf"
fetch "$GF/archivo/OFL.txt" "$SRC/archivo-OFL.txt"

for w in Regular Medium; do
  fetch "$GF/ibmplexmono/IBMPlexMono-$w.ttf" "$SRC/plexmono-$w.ttf"
done
fetch "$GF/ibmplexmono/OFL.txt" "$SRC/ibmplexmono-OFL.txt"

# Ship the licences with the fonts — SIL OFL requires the notice to travel.
mkdir -p "$OUT/licenses"
cp "$SRC/archivo-OFL.txt" "$OUT/licenses/Archivo-OFL.txt"
cp "$SRC/ibmplexmono-OFL.txt" "$OUT/licenses/IBMPlexMono-OFL.txt"

# latin + latin-ext + the punctuation/currency/maths a spec sheet actually uses.
# Deliberately NOT included: U+1E00-1EFF (Vietnamese) and U+0370-03FF (Greek) —
# together they were ~40% of the Archivo subset and this site ships neither.
UNICODES="U+0000-00FF,U+0100-024F,U+0259,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+2080-2089,U+20A0-20BF,U+2113,U+2122,U+2126,U+212E,U+2190-2193,U+2202,U+2205-2206,U+220F,U+2211-2212,U+2215,U+221A,U+221E,U+2229,U+222B,U+2248,U+2260-2265,U+25A0-25CF,U+2713,U+2717,U+FEFF,U+FFFD"

# locl carries the Turkish i/ı forms; case fixes punctuation inside all-caps
# labels; tnum gives the tabular figures every spec table depends on.
FEATURES="kern,liga,calt,locl,case,tnum,frac,ccmp,mark,mkmk"

subset() {
  local src="$1" out="$2"; shift 2
  "$PY" -m fontTools.subset "$src" \
    --output-file="$out" --flavor=woff2 \
    --layout-features="$FEATURES" \
    --unicodes="$UNICODES" \
    --no-hinting --desubroutinize --drop-tables+=DSIG "$@"
}

# Clip the variable axes to the range the design actually uses before subsetting.
# Archivo ships wdth 62-125 / wght 100-900; the type scale uses wdth 82-100 and
# wght 400-700, and every delta outside that is weight we would ship for nothing.
echo "instancing axes (wdth 80:100, wght 400:600)"
"$PY" -m fontTools.varLib.instancer "$SRC/archivo-var.ttf" \
  "wdth=80:100" "wght=400:600" \
  --output "$SRC/archivo-clipped.ttf" >/dev/null

echo "subsetting"
subset "$SRC/archivo-clipped.ttf"  "$OUT/archivo-var.woff2"
subset "$SRC/plexmono-Regular.ttf" "$OUT/ibm-plex-mono-400.woff2"
subset "$SRC/plexmono-Medium.ttf"  "$OUT/ibm-plex-mono-500.woff2"

echo
echo "result:"
total=0
for f in "$OUT"/*.woff2; do
  size=$(stat -c%s "$f")
  total=$((total + size))
  printf "  %-28s %6.1f KB\n" "$(basename "$f")" "$(echo "$size" | awk '{print $1/1024}')"
done
printf "  %-28s %6.1f KB  (budget 85 KB, hard fail 110 KB)\n" "TOTAL" "$(echo "$total" | awk '{print $1/1024}')"

echo
echo "Turkish glyph check:"
"$PY" - "$OUT/archivo-var.woff2" "$OUT/ibm-plex-mono-400.woff2" "$OUT/ibm-plex-mono-500.woff2" <<'PYEOF'
import sys
from fontTools.ttLib import TTFont

NEEDED = "ıİğĞşŞçÇöÖüÜâîû₺"
missing_any = False
for path in sys.argv[1:]:
    font = TTFont(path)
    cmap = set()
    for table in font["cmap"].tables:
        cmap |= set(table.cmap)
    missing = [c for c in NEEDED if ord(c) not in cmap]
    status = "OK" if not missing else f"MISSING {''.join(missing)}"
    if missing:
        missing_any = True
    print(f"  {path.split('/')[-1]:<28} {status}")
sys.exit(1 if missing_any else 0)
PYEOF
