# The World Today — 23 November 2026 in one image

Entry for make.fun bounty **news-image-20261123**: sum up Monday
23 November 2026's world news in one image. An AI judge compares
entries pairwise and ranks them by how often it picks them; the 50
highest-ranked entries share $100 (1st $20, 2nd $12, 3rd $6, 4th–10th
$2, 11th–50th $1.20). Deadline 2026-11-25T00:00:00Z.

## The image

A newspaper front page, 1024×1024 PNG (162,120 bytes), six stories:

1. **COP31 COLLAPSES** (lead) — world climate talks fail in Antalya
   after two weeks; the first COP breakdown since 2009. Nations reject
   the Antalya Pact over fossil fuels; 90+ nations still sign an
   electrification pledge.
2. **Ukraine sinks Russian warship off Libya** — sea drones hit the
   corvette Merkury at Benghazi naval base; cargo ship Angara also hit.
3. **Russian strike on Kyiv flats kills 11+** — rescuers dig through
   rubble in Dymer after an overnight strike on an apartment block.
4. **NATO meets on Russian missiles in Poland** — the alliance's top
   body convenes after Kh-101 debris was found.
5. **Tehran vows 'every means' against US blockade** — Iran answers
   Trump's warning that tankers breaking the blockade will be sunk.
6. **Delta outage delays 1,600 flights** — a weight-and-balance
   system failure snarls the Atlanta hub as Thanksgiving travel begins.

Sources: CNN, Reuters, Le Monde, Bloomberg, The Guardian — all
reporting dated 23 November 2026.

## How it is built

- `render.py` — renders `assets/news.png` with Pillow (Noto Sans /
  DejaVu fonts). Run it to rebuild the image; it is deterministic.
- `main.ts` — the entry program (Node 22, standard library only).
  It copies `assets/news.png` to `/output/entry.png` and checks the
  bounty's limits first (PNG, ≤ 1 MiB, ≤ 1024×1024) by reading the
  PNG header. No network, no randomness, no timestamps: two runs
  write byte-identical output (verified: same SHA-256 across runs).

## Run it

```sh
node main.ts [--output <dir>]   # default: $MAKEFUN_OUTPUT_DIR or /output
```
