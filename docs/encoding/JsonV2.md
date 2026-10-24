# `encoding/json/v2`: Whether to migrate — the official answer

`encoding/json/v2` is the new JSON package introduced with Go 1.27 alongside the new struct tags, and the official team wrote a dedicated migration guide. This repo's `docs/zh/encoding/JSON.md` covers v1; v2 had no page before. The content comes from the official migration guide and package documentation, fetched on 2026-10-08.

## One, the conclusion first: no need to migrate

The migration guide answers right off the bat: "First things first: you don't have to!":

- `encoding/json` will never go away; it is protected by the Go 1 compatibility promise, and code written against v1 will keep running.
- v1 and v2 are mutually compatible. If a type implements `encoding/json/v2.MarshalerTo`, calling it through `encoding/json.Marshal` also uses that custom marshal.
- The new struct tags introduced in Go 1.27 are also supported by `encoding/json`.

So this is a "migrate when you want better defaults and a better API" situation, not version pressure.

## Two, what v2 changed

| Aspect | v1 | v2 |
| --- | --- | --- |
| Writing to a writer | Requires `encoding/json.Encoder` | `encoding/json/v2.MarshalWrite` writes directly to an `io.Writer` |
| Overriding serialization behavior for a specific type | Can only change the type itself | `encoding/json/v2.Marshalers` can override types you do not own |
| Case matching of field names | Fixed behavior | `encoding/json/v2.MatchCaseInsenstiveNames` controls whether case is ignored |
| Invalid UTF-8 in strings | Silently replaced with the replacement character | Reports an error directly |
| Default-value stance | Lenient | Stricter, better interoperability |

The last row is the heaviest of the migration reasons the official docs give: v2 chose stricter, more interoperable defaults. The invalid-UTF-8 row is the first comparison example the docs give.

## Three, what this means for this repo

| Scenario | What to do |
| --- | --- |
| Existing service, v1 runs fine | Leave it alone; compatibility is backed by the official promise |
| A new API that needs strict input validation | Use v2 for new code; invalid UTF-8 will error at encode/decode time instead of being silently rewritten |
| Need to match field names ignoring case | Use v2's switch for what v1 cannot do |
| Mixing v1 and v2 | Works; custom marshal and the new struct tags are honored by both sides |

Related pages: `docs/zh/encoding/JSON.md` (v1 syntax and usage), `docs/zh/type/Json.md` (struct tags), `docs/zh/gin/Request.md` (request body binding).

## Four, reading the package docs

The v2 package docs live under the `encoding/json/v2` group in the standard library; both `golang.google.cn/pkg/` and pkg.go.dev open them. The migration guide is at `/doc/jsonv2-migration`. Both are pages actually fetched during this investigation.

## Sources

1. https://golang.google.cn/doc/jsonv2-migration — Migration guide: the three reasons not to migrate, v1/v2 compatibility, four API and default-value differences, and Go 1.27's new tags being supported by both (fetched 2026-10-08)
2. https://golang.google.cn/pkg/encoding/json/v2 — Package documentation entry point
3. https://golang.google.cn/doc/ — The json/v2 migration guide entry listed in the References section of the documentation overview

## References

- [encoding standard library series (json as an example)](https://pkg.go.dev/encoding/json)
- [Official · json/v2 migration guide](https://go.dev/doc/jsonv2-migration)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [CSV](/encoding/CSV.md)
- [Encoding](/encoding/Encoding.md)
- [Formats](/encoding/Formats.md)
- [Gob](/encoding/Gob.md)
- [Hex](/encoding/Hex.md)
- [Ini](/encoding/Ini.md)
- [JSON](/encoding/JSON.md)
- [TOML](/encoding/TOML.md)
- [Text](/encoding/Text.md)
- [Voice](/encoding/Voice.md)
- [XML](/encoding/XML.md)
- [knowledge](/zh/knowledge.md)
