# Content Review of Structural Changes (2026-10-19)

## Review scope

Reviewed the four most recent commits (`HEAD~4..HEAD`) per `git log --oneline -4`:

| Commit | Content |
|---|---|
| `4f055f0` | Align site copy with notes voice (C: site wording) |
| `edee3bf` | Clarify overlapping note scopes (B: overlapping topic scopes) |
| `5e9bf06` | Clarify navigation source (A: navigation authority source and SUMMARY consolidation) |
| `a3125cc` | Add docs structure audit (structure audit record adjustments) |

These four commits touch 19 files together; `HEAD~4..HEAD` counts 82 insertions and 451 deletions; commit history was not rewritten. The working tree started clean, and `git fetch origin && git pull --rebase origin main` succeeded and reported already up to date.

## The four checks

### 1. Content loss — no body content lost

- `docs/SUMMARY.md:1-5`: the old 414-line table of contents was replaced with a maintenance note. The config at `docs/.vitepress/config.mts:18-20` explicitly excludes SUMMARY via `srcExclude`, and no body files were deleted. What this change removed was a second copy of the navigation, not content entries.
- Checking each of the 13 duplicate routes removed from the sidebar against their targets, every target page still has exactly one entry: for example the old `/start/Build` is at `docs/.vitepress/sidebar.json:74`, and the old `/concurrency/Select` is retained in its concurrency-related group. The old sidebar had 402 links and 389 unique targets; the new sidebar has 389 links and 389 unique targets, so the duplicate count went from 13 down to 0.
- The `docs/zh/alloc/GC.md` merged in B: the two explanations under the old `### Basic principles: concurrent mark-and-sweep` were compressed into a summary, and the new `docs/zh/alloc/GC.md:11` links to the authority page `docs/zh/gc/GC.md`; allocator-cooperation and tuning content is still retained. The content move's destination exists.
- Before/after: `docs/zh/alloc/GC.md` originally had full marking and sweeping explanations; it now has a paragraph overview plus "for the full marking, tricolor abstraction, and trigger mechanism see [How GC works notes](/gc/GC.md)". No allocator-specific content was deleted.

### 2. Misstatements, numbers, and technical meaning — numbers match; found and fixed a stale audit statement

- `docs/.vitepress/config.mts:38-40` declares 50 top-level groups; a manual count of the top-level objects in `sidebar.json` is 50. Sidebar targets checked out as 389 links, 389 unique targets, 0 duplicates, and 0 missing files.
- The two README edits are one line each (`README.md:22`, `README.zh.md:22`), with no page counts, file counts, or directory listings that need changing. The Chinese version changed from "Go knowledge site / covers…" to "personal study notes, insights, and development experience… not a course or learning tutorial"; it did not reverse a "not supported" Go support scope or capability into "supported". The English version was likewise rewritten toward personal development notes and a game-developer perspective, and the technical topics still list language details, concurrency, algorithms, libraries, and engineering practice.
- The positioning rewrites at `docs/zh/index.md:6-7` and `config.mts:8,30` are consistent with the README; the "development notes" navigation still points at the existing `start/Starter` page.
- Found that the audit page's old analysis paragraph still claimed SUMMARY had 403 current links, recommended SUMMARY as the authority source, and asked the user to choose — which conflicts with A's actual closeout decision. The evidence is lines 103, 113, 129, and 135 of `docs/zh/review/structure-audit-2026-10-19.md` before this review. The wording has been corrected: the old recommendation is marked as pre-change state, the sidebar JSON is stated as the sole source, and the build dead-link status is now listed as "unverified". Fix commit: `6a354f4`.

### 3. Links and navigation — no bad targets found

- The 5 new sets of scope-statement cross-links were checked one by one against the file topics and relative paths: array semantics ↔ array data structure, runtime interfaces ↔ interface concepts, plain switch ↔ type switch, assignment operator ↔ variable assignment patterns, official security ↔ IO/database security; every path exists and the topics match.
- All 389 existing sidebar link targets were mapped to files item by item, none missing. The 13 removed ones were duplicate routes, and the retained entry is still in the corresponding topic group (see check 1).
- The config top navigation `/start/Starter`, `/type/CompositeType`, `/concurrency/Concurrency`, `/dp/DesignPatterns`, `/db/Readme`, and `/gin/Gin` all have corresponding pages.
- **Unverified**: this pass did not install dependencies or run a full VitePress build, so the build-time dead-link check has no independent evidence. This is not the same as reporting that dead links were found.

### 4. Other clear conclusions

- After the trim, SUMMARY's only function is a maintenance note; its new content explains the sidebar authority source and `srcExclude` behavior, which matches the config.
- B's scope statements for the six cross-directory topic groups match the target pages' content: only the GC fundamentals in `gc/GC.md` and `alloc/GC.md` were treated as duplicates, and the other five groups keep their distinct angles; this diff did not delete any of those Markdown pages.
- No content merge-or-delete tradeoff requiring a user decision was found; what was actually merged this pass were duplicate navigation routes, not page bodies.

## Findings

| # | Severity | Issue and evidence | Fixed | Fix commit |
|---|---|---|---|---|
| 1 | Low (audit record consistency) | The structure audit's old recommendation still asks the user to choose between SUMMARY and the sidebar, contradicting the already-implemented single-source decision; the old build concern wording is also out of date. | Yes | `6a354f4` |

No lost body content, number errors, or misdirected links were found. Unverified item: VitePress full-build-level link checking (no build was run this pass).

## Conclusion

As a line-by-line manual review of this pass, the A/B/C structural changes showed no substantive issue that would cause content loss or broken navigation, and the stale recommendation in the audit record has been fixed. **This can be considered accepted at the content and navigation level; the build-level dead-link status remains unverified.**
