# hello-golang Documentation Structure Audit (2026-10-19)

Scope: read-only inspection of the repo's documentation organization, VitePress sidebar, the repo root directory, and local links. The report was added at `docs/zh/review/structure-audit-2026-10-19.md`; no other documentation or configuration was changed. Line counts are counted by LF line breaks and include blank lines.

## Quantified facts

### Markdown count and line count under top-level `docs/` directories

| Top-level directory | .md count | Total lines |
|---|---:|---:|
| algo | 49 | 6,906 |
| alloc | 3 | 476 |
| applications | 5 | 292 |
| asm | 2 | 385 |
| cgo | 2 | 435 |
| cmd | 6 | 1,416 |
| compress | 6 | 1,583 |
| concurrency | 11 | 1,925 |
| const | 5 | 478 |
| db | 19 | 3,817 |
| debug | 7 | 1,014 |
| distribution | 1 | 199 |
| dp | 29 | 3,822 |
| encoding | 14 | 2,311 |
| env | 9 | 1,184 |
| error | 4 | 923 |
| func | 10 | 1,741 |
| gc | 2 | 208 |
| generics | 7 | 1,154 |
| gin | 13 | 2,674 |
| idioms | 8 | 979 |
| introduction | 4 | 357 |
| io | 14 | 3,922 |
| log | 4 | 939 |
| math | 8 | 1,707 |
| middleware | 3 | 209 |
| mod | 9 | 1,240 |
| naming | 3 | 537 |
| net | 7 | 1,617 |
| oop | 8 | 1,460 |
| operator | 11 | 1,603 |
| redis | 11 | 1,820 |
| reflection | 2 | 370 |
| regex | 6 | 1,052 |
| research | 5 | 449 |
| security | 1 | 58 |
| start | 7 | 1,016 |
| sync | 11 | 1,741 |
| syntax | 10 | 1,670 |
| sys | 4 | 296 |
| test | 9 | 1,286 |
| time | 7 | 982 |
| type | 26 | 4,677 |
| var | 5 | 831 |
| **Total (content directories)** | **391** | **64,701** |

Directory statistics are computed recursively. `docs/.vitepress` is the config/build directory (0 md files), `docs/public` is the static assets directory (0 md files); neither counts toward the content directory total. Under the `docs/` root there are additionally `SUMMARY.md` (414 lines), `glossary.md` (379 lines), `index.md` (25 lines), `knowledge.md` (122 lines) — 4 files, 940 lines in total.

### Organization-axis inventory

| Organization axis / mechanism | Entries | Naming pattern | Numbering | Continuity |
|---|---:|---|---|---|
| Topic directories (primary storage axis) | 44 content directories, 391 pages | Mostly short English topic directory names, with English topic file names inside; e.g. `docs/zh/concurrency/Chan.md` | None | N/A |
| Navigation section order (`SUMMARY.md` → `sidebar.json`) | SUMMARY has 403 links; sidebar has 389 unique page references | Organized by Chinese section names, links land in topic directories; sidebar imported by `config.mts` | No explicit numeric numbering | N/A; not a numbering system |
| Guide/getting-started path (embedded in topic navigation) | No standalone `guide` directory; 7 getting-started pages, 9 environment pages | `docs/zh/start/` and `docs/zh/env/`, serving as topic directory and navigation group respectively | None | N/A |
| API directory axis | 0 top-level directories named API; API content is scattered across topic directories (entries not counted as a dedicated API list) | Filed by language/library topic | None | N/A |
| history axis | 1 file name containing History: `docs/zh/func/History.md` | File-level topic/history tag, not a standalone directory or stable system | None | N/A |
| Numeric-prefix section axis | 0 file basenames with a numeric prefix | No files with numeric prefixes such as `01-` or `1.` found | No entries | No gaps/skips/duplicates to report; the full numeric-prefix sort result is empty |

Conclusion: **3 organization mechanisms actually in effect** (topic directories, navigation section order, embedded guide path). API and history are content-type/single-file phenomena, not independent organization axes; the numeric section-numbering axis does not exist. `SUMMARY.md` and the sidebar are the draft and runtime config of the same navigation structure, not counted twice.

### Sidebar reconciliation

Read `docs/.vitepress/config.mts` and the imported `docs/.vitepress/sidebar.json`. 389 unique configured page link values:

| Group | Count | First 10 entries |
|---|---:|---|
| Configured but target file does not exist | 0 | None |
| File exists but not in sidebar | 2 | `docs/zh/index.md`, `docs/SUMMARY.md` |

`SUMMARY.md` is explicitly excluded via `srcExclude: ['**/SUMMARY.md']` in `config.mts`; `index.md` is the site root page, normally served by the VitePress home route, so leaving it out of the sidebar is reasonable configuration. The sidebar check does not double-count directory pages or aliases.

### Numbering, naming, distribution, and repo root

- **Numeric prefixes**: A full extraction of basenames from the 391 content Markdown files matched against `number + optional separator + name` yields 0. There are no gaps, skips, or duplicate numbers to list; these should not be artificially back-filled.
- **Same/similar topics across multiple places** (identical basenames are checkable proxy evidence, not proof that content is necessarily duplicated): `Array` at `docs/zh/type/Array.md` and `docs/zh/algo/array/Array.md`; `GC` at `docs/zh/gc/GC.md` and `docs/zh/alloc/GC.md`; `Interface` at `docs/zh/type/Interface.md` and `docs/zh/oop/Interface.md`; `Security` at `docs/zh/security/Security.md`, `docs/zh/io/Security.md`, `docs/zh/db/Security.md`; `Switch` at `docs/zh/syntax/Switch.md` and `docs/zh/type/Switch.md`; `Assignment` at `docs/zh/operator/Assignment.md` and `docs/zh/var/Assignment.md`. Each may reasonably represent a different context; whether they are duplicates can only be judged after reading the bodies.
- **Naming style**: topic directories use lowercase English (e.g. `docs/zh/redis/`), and file names mix PascalCase (`docs/zh/env/Goland.md`), lowercase (`docs/zh/env/ide.md`, `docs/zh/gin/advanced.md`), and acronym/word-boundary styles (`docs/zh/encoding/JSON.md`, `docs/zh/io/ModOS.md`); `Readme.md` and `README.md` coexist, with 8 README variants whose basenames have inconsistent casing: `docs/zh/cmd/Readme.md`, `docs/zh/db/Readme.md`, `docs/zh/distribution/Readme.md`, `docs/zh/middleware/Readme.md`, `docs/zh/redis/Readme.md`, `docs/zh/regex/Readme.md`, `docs/zh/research/README.md`, `docs/zh/compress/Readme.md`. Casing differences affect case-sensitive links and search consistency.
- **Cross entry points**: the "Idioms" section of `docs/SUMMARY.md` links to the same topic pages repeatedly — `func/MultipleReturnValues.md`, `func/Defer.md`, `syntax/Switch.md`, `concurrency/Select.md`, and so on. This is multi-entry navigation and does not by itself prove body duplication.
- **Navigation mapping draft discrepancy**: `docs/SUMMARY.md` has 403 Markdown links, all currently existing files; the VitePress sidebar has 389 unique references. Duplicate links in SUMMARY explain part of the difference. A comment in `docs/.vitepress/config.mts` states that the sidebar is generated from SUMMARY by mapping; the two appear in sync, but the mapping script was not executed in this check (`unverified`).
- **Stray files at repo root**: the repo root contains `BUGS.md`, `README.md`, `README.zh.md`, `LICENSE`, `package.json`, `package-lock.json`; no temporary files found at the root. `BUGS.md` is a maintenance log; the bilingual README is an intentional distinction, not a duplicate README. `docs/` has the 4 entry/auxiliary Markdown files listed above, which are docs-site content and not repo-root stray files.

### Link/build check

- `npm run docs:build` **could not run**: `sh: 1: vitepress: not found`; `package.json` has a build script, but the current environment has no installed local VitePress executable. The full build-level dead-link check is therefore **unverified**.
- Sidebar page references were mapped to files: 0 missing.
- A simple scan of Markdown inline links was done, but the scanner misreads parentheses inside code fences/inline code as links, producing 18 false positives (e.g. the code argument at `docs/zh/generics/Constraints.md:14`). It cannot be claimed that there are 18 dead links on that basis. Comparing `docs/SUMMARY.md:396` with `docs/zh/gin/advanced.md`, the current SUMMARY casing references are consistent; `docs/zh/research/Coverage.md:100` is merely an old issue record preserved in the audit table, not a link, so it cannot be reported as a current dead link.

## Issue list and severity

| # | Issue / judgment | Severity | Evidence and rationale |
|---|---|---|---|
| 1 | Build-level dead-link status unknown | Unverified | This closeout record has local link-scan results, but the initial VitePress build was still not run. The earlier casing suspicion was confirmed to be an old issue record, not a current link. |
| 2 | SUMMARY and sidebar are dual maintenance data and can drift | Resolved | The closeout record selected `docs/.vitepress/sidebar.json` as the sole authority source; `docs/SUMMARY.md` is now a maintenance note and is excluded via `srcExclude`. The old 403/389 reconciliation only describes the pre-change state, not current data. |
| 3 | File naming casing/word-boundary inconsistency, README variants especially obvious | Low | The 8 `Readme.md`/`README.md` paths above; `docs/zh/env/ide.md` alongside `docs/zh/env/Goland.md`, `docs/zh/gin/advanced.md`. Mainly affects search, cross-platform links, and maintenance consistency; not an organizational failure. |
| 4 | Same-basename topic pages distributed across multiple places, easy to misjudge as duplicates or cause search ambiguity | Low | `docs/zh/type/Array.md` and `docs/zh/algo/array/Array.md`; `docs/zh/gc/GC.md` and `docs/zh/alloc/GC.md`; more in "Same/similar topics across multiple places". Contexts may be intentionally distinct; merging based on file names alone is not recommended. |
| 5 | Numbering gaps/duplicates | No issue | Numeric-prefix count across all content files is 0; the current system is not a numbered-section scheme and should not be treated as a defect. |
| 6 | Sidebar orphans / pages not in sidebar | Low / no blocker | 0 configured files missing; 2 not in sidebar, of which SUMMARY is explicitly excluded and index is the root homepage. No navigation dead links to fix. |

## Judgment and recommendations

The current main skeleton is **topic directories + one set of section navigation**; the structure itself is understandable, and the directory names broadly cover the Go language, standard library, engineering practice, algorithms, and ecosystem topics. The pre-change risk of dual-maintained navigation drafts was addressed at closeout; file naming details and whether adjacent concept pages have clear context cues still need attention; "too messy" does not apply to all parts.

The pre-change structural recommendation favored SUMMARY as the navigation source; that recommendation has been superseded by the "Closeout execution record" below. The current actual approach is `docs/.vitepress/sidebar.json` as the sole authority source, with SUMMARY retaining only the maintenance note, and no 403/389 link difference remaining to be handled.

**Parts that are actually not messy and need no change**

- Topic directories as the primary filing method is reasonable; topic boundaries like `db/`, `redis/`, `gin/` are clear, and a large count by itself is not evidence of disorder.
- All 389 VitePress sidebar references currently resolve to files; no configured dead links.
- `docs/SUMMARY.md` being explicitly excluded and `docs/zh/index.md` not being in the sidebar matches common site routing design.
- `README.md` and `README.zh.md` are language versions, not duplicate files; `BUGS.md` is a repo-level maintenance log.
- Same names like `Array`, `Interface`, `Security` may serve different teaching goals in different domains; keep them and improve cross-links first, no merging without evidence.
- There is no numeric section numbering currently, and no numbering-skip issue, so no back-filling or reordering is needed.

## Three-phase closeout plan

| Phase | Action list | Scope of impact | Risk (links/search/external) | User decision |
|---|---|---|---|---|
| Phase 1: mechanical tidy-up, target within 1 hour | A candidate list for unifying obvious spelling/casing naming (first do repo-wide link replacement and casing verification); add a one-line scope statement/cross-link for same-named cross-topic pages; confirm the suspected `Advanced.md` path. Only rename after every on-site reference has been updated one by one and the build passes. | A small number of file names and links, README variants as candidates; no directory architecture change. | In-place casing renames may break case-sensitive paths, external links, and search indexes; purely adding scope statements is low risk. Renames must update on-site links in sync. | **Decide** the unified target name for README; whether renaming public URLs is acceptable; whether cross-topic pages keep their current names. |
| Phase 2: navigation authority source and redirects | **Navigation authority source selection complete**: sidebar JSON as the sole source; check whether pages like `docs/zh/knowledge.md` have reasonable entry points; if paths migrate in the future, evaluate old-URL redirects and run build link checks. | Sidebar JSON, a small amount of navigation, and possible redirect config. | Changing navigation order affects discoverability; page path migration may affect external links and search indexing. Keeping old-address redirects reduces risk but requires maintenance. | Authority source decided; future path migration and redirect strategy to be evaluated per change. |
| Phase 3: deep restructuring with section merge/delete | Compare bodies for same-basename/duplicate topics, define audience and boundaries; decide to merge, split, or keep; maintain aliases/redirects, update on-site links and search; verify by build and manual sampling. | Multiple topic docs, potentially touching dozens of bodies, navigation, and historical URLs. | Highest: deleting/merging affects deep links, search ranking, citations, and reader bookmarks; redirects only mitigate, and semantic merges may also lose differentiating content. | **Must decide item by item**: content deletion/merge target, keep-or-drop old URLs, navigation hierarchy, and external-link compatibility strategy. |

## The three things to do first

1. Run `npm ci && npm run docs:build` in an environment with dependencies installed; resolve and record the real build/dead-link results; record build output and handle the dead links the build actually reports.
2. The navigation authority source has been consolidated to sidebar JSON; going forward maintain only that file and confirm target Markdown files exist.
3. First mark scope and cross-entry points for same/similar topic pages, then discuss renaming or merging; do not touch numbering or large-scale migration for now.

## Closeout execution record (2026-10-19)

### A. Single source of navigation truth

- The authority source is set to `docs/.vitepress/sidebar.json`: `docs/.vitepress/config.mts:2,40` imports and configures that file directly.
- `docs/SUMMARY.md:1-5` is retained as a maintenance note: it states that the sidebar is the sole editable source, that SUMMARY is a leftover mdbook draft excluded by `srcExclude`, and that manual edits to SUMMARY do not take effect.
- The sidebar tree originally had 13 duplicate routes (402 link values, 389 unique values). Duplicates were collapsed to the first entry; duplicate parents that contain standalone child pages keep their group but lose the duplicate parent link, avoiding loss of child-page entry. Now 389 link values, 389 unique values, 0 duplicates. Page reuse across different groups is navigation-entry reuse and was not deleted across the sidebar.

### B. Per-group judgment on cross-axis duplicates

| Page group | Judgment | Body comparison evidence | Handling |
|---|---|---|---|
| `type/Array.md` / `algo/array/Array.md` | Different angles | The first opens with "arrays have fixed length and the same element type, while slices can grow", and covers Go arrays/slices and pass-by-value; the second opens with "linear data structure... contiguous memory", focusing on O(1) random access, contiguous storage, and complexity. | Kept, cross-linked and marked as language-semantics / data-structure perspective. |
| `gc/GC.md` / `alloc/GC.md` | True duplicate (GC basic principles) | The first says "Go's garbage collector is a concurrent mark-and-sweep collector", the second says "Go's GC is a concurrent tricolor mark-and-sweep collector"; both explain marking from roots and sweeping unreachable objects. | `gc/GC.md` is the authority page on principles; `alloc/GC.md:11-13` changed to a summary with a full link, while allocator cooperation, observation, and tuning remain on that page. |
| `type/Interface.md` / `oop/Interface.md` | Different angles | `type/Interface.md` opens with emphasis on `iface`, `itab`, and reflection relationships; `oop/Interface.md` develops type/interface definition and implementation from "types describe what data looks like, interfaces describe what an object can do". | Kept, cross-linked and marked as runtime / conceptual-implementation perspective. |
| `syntax/Switch.md` / `type/Switch.md` | Different angles | The first opens with default-exit, `fallthrough`, and ordinary switch; the second's first paragraph is clearly a type switch branching on the dynamic type of an interface value. | Kept, cross-linked and marked as control-flow / dynamic-type-dispatch perspective. |
| `operator/Assignment.md` / `var/Assignment.md` | Different angles | The first opens with `=` and compound assignment operators; the second's first paragraph says "there are ten common patterns", covering short declarations, multiple assignment, blank identifiers, pointers, structs, and similar patterns. | Kept, cross-linked and marked as operator / variable-usage-pattern perspective. |
| `security/Security.md` / `io/Security.md` / `db/Security.md` | Different angles | The official page covers the Go vulnerability database, fix scope, fuzzing, and crypto; the IO page is titled "Security of files and IO"; the DB page develops from database security and SQL injection. | All three pages kept and cross-linked, marked as official-position, file-IO, and database-security perspectives. |

Merged true duplicates: **1 group**; kept different angles: **5 groups**. No Markdown was deleted, and different perspectives were not forced together.

### C. Positioning and dead items

- `README.md:22` and `README.zh.md:22` changed to a personal-notes and game-developer-sharing positioning; neither README has hard-coded page counts or directory listings, so no count/listing change was needed.
- Site copy at `docs/zh/index.md:6-7` and `docs/.vitepress/config.mts:6,24` changed to a personal development-notes positioning.
- The "50 top-level groups" at `docs/.vitepress/config.mts:38-40` matches the sidebar's actual 50 items, retained; no sidebar page entries with non-existent target files were found.
- `docs/zh/knowledge.md` is already in the "Research" sidebar group; the important overview page is in the sidebar.

### Acceptance snapshot

- `pnpm docs:build` passed (VitePress 1.6.4; pages built). Output includes assembly/gdb highlight fallback and large-chunk warnings, which do not affect the build.
- Recomputable equivalent check: the Markdown local-link scan skips code fences and inline code, and resolves `/...` routes against the docs root; **2782** local Markdown links checked, **0** missing. All 389 sidebar link targets exist, **0** missing; sidebar duplicate routes **0**.
- Markdown files deleted: **0** (no `.md` was deleted during the closeout commits).
