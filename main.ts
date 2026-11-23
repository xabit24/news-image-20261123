// News image entry for make.fun bounty news-image-20261123:
// "Sum up 23 November's world news in one image".
//
// The program writes one image to /output/entry.png. The image itself is
// the newspaper front page in assets/news.png, rendered ahead of time by
// render.py (Pillow, Noto/DejaVu fonts) from the verified stories of
// Monday 23 November 2026 — COP31 collapsing in Antalya as the lead,
// plus Ukraine sinking the Russian corvette Merkury off Libya, the
// Russian strike on Kyiv flats, NATO's missile meeting on Poland, Iran's
// blockade warning, and the Delta outage. The bounty itself says the
// simplest program copies an image the repository holds; this file does
// exactly that, and nothing else.
//
// Determinism: the copy is byte-for-byte, no timestamps, no randomness,
// no network. Running it twice writes identical bytes, which is what the
// bounty requires. Before writing, it checks the image against the
// bounty's own limits (whole PNG, at most 1 MiB, at most 1024x1024)
// by reading the PNG header, so a bad asset fails loudly instead of
// submitting a rejected entry.
//
// Usage (Node 22, standard library only):
//   node main.ts [--output <dir>]
// The output directory is --output, else $MAKEFUN_OUTPUT_DIR, else
// /output. The file is always named entry.png.

import * as crypto from 'node:crypto';
import * as fs from 'node:fs';
import * as path from 'node:path';
import * as url from 'node:url';

const repoRoot = url.fileURLToPath(new URL('./', import.meta.url));
const ASSET = path.join(repoRoot, 'assets', 'news.png');

/** Bounty limits: whole PNG or JPEG, at most 1 MiB, at most 1024x1024. */
const MAX_BYTES = 1024 * 1024;
const MAX_DIMENSION = 1024;

/** Stop the run with a message on stderr and a non-zero exit. */
function die(message: string): never {
  process.stderr.write(`news image: ${message}\n`);
  process.exit(1);
}

/** The value after `--name <value>` or `--name=<value>`, else undefined. */
function flagValue(flag: string): string | undefined {
  const argv = process.argv;
  const bare = argv.indexOf(`--${flag}`);
  if (bare >= 0 && bare + 1 < argv.length) return argv[bare + 1];
  const joined = argv.find((a) => a.startsWith(`--${flag}=`));
  if (joined !== undefined) return joined.slice(flag.length + 3);
  return undefined;
}

/** Width and height from a PNG's IHDR chunk (big-endian u32s at 16/20). */
function pngDimensions(buf: Buffer): { width: number; height: number } {
  if (buf.length < 24 || buf.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
    die('assets/news.png is not a PNG file');
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

const outDir = flagValue('output') ?? process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outPath = path.join(outDir, 'entry.png');

const buf = fs.readFileSync(ASSET);
if (buf.length > MAX_BYTES) {
  die(`assets/news.png is ${buf.length} bytes, over the 1 MiB limit`);
}
const { width, height } = pngDimensions(buf);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  die(`assets/news.png is ${width}x${height}, over the 1024x1024 limit`);
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, buf);

const sha = crypto.createHash('sha256').update(buf).digest('hex');
console.log(
  `news image: wrote ${outPath} (${width}x${height}, ${buf.length} bytes, sha256 ${sha.slice(0, 16)}...)`,
);
