# Where the numbers on the site come from

Checked on 23 October 2026. Every figure on `index.html` and `portfolio-dossier.html` comes from this list. Re-run the commands to check or refresh them.

| Project | Repository commit | Figure on the site | How it was counted |
| --- | --- | --- | --- |
| ICT Flux | `ict-trader` @ `e1fb268` (private) | 68 engine modules | `git ls-files 'ict_trader/*.py' \| wc -l` |
| | | about 17,000 lines of Python | `git ls-files 'ict_trader/*.py' 'api/*.py' \| xargs cat \| wc -l` gives 17,090 |
| | | over 690 automated tests | `grep -hcE '^\s+def test_' tests/*.py` summed gives 692 |
| | | no reliable edge on 19 markets of real candles | `docs/BASELINE.md` in the repo (real Deriv candles, 19 markets, three timeframes) |
| Video Splitter & Assembler | `video-assembler-saas` @ `0798a64` (public) | about 16,700 lines | `.ts` and `.tsx` files under version control, `xargs cat \| wc -l` gives 16,699 |
| | | 197 tests, all passing | `npm ci --ignore-scripts && npx vitest run`: 23 files, 197 tests passed |
| ToonForge | `toonforge` @ `ce004e1` (private) | about 5,300 lines TypeScript, about 600 Python | same method: 5,341 and 603 |
| | | 38 tests, all passing | `npm ci --ignore-scripts && npx vitest run`: 6 files, 38 tests passed |
| | | voices and GPU worker tested in mock mode only | `HANDOVER.md` in the repo. Update this line when they are tried on real hardware |
| Chopos | `chopos` @ `930ed8e` (private) | about 7,300 lines, 12 models, 13 API routes | `.ts`, `.tsx` and `.js` files: 7,299; `grep -c '^model ' prisma/schema.prisma`; `git ls-files \| grep -c 'route\.ts'` |
| | | stock row locks | `db/schema.sql`, function `atomic_decrement_stock` uses `SELECT ... FOR UPDATE` |
| | | no automated tests | no test files in the repository |
| Motion | `motion-oau` @ `9e1f739` (public) | about 4,000 lines | `.ts` and `.tsx` files: 4,001 |
| | | no automated tests | no test files in the repository |

Notes

- `showcase.html` (the 3D tour) uses only the figures above. Its walkthroughs describe how each project works; they are illustrations with no live data.

- A count of lines is a size, not a measure of quality.
- "Over 690 automated tests" counts test functions. It does not say they all pass at every commit.
- The site makes no claim that ICT Flux is profitable, because the measured result does not support one.
