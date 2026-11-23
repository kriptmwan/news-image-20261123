// news-image-20261123 entry (Node 22, standard library only).
// The entry image is entry.png beside this file; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR outside the grader container).
// The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels, and
// the judge sees exactly the bytes copied, so the copy must be byte-exact.

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
