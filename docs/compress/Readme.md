# Compression and Archiving
### 1. Overview

**Compression** and **archiving** do two different things. Compression uses algorithms to strip redundancy from data and shrink files — the common ones are `gzip`, `zlib`, and `bzip2`, used for things like moving large files and saving disk space. Archiving bundles multiple files along with their metadata into a single file so they are easier to manage and distribute — the representative formats are `tar` and `zip`, relied on for backups, bulk transfer, and shipping software packages.

The two are often chained: `tar` packs without compressing, while `tar.gz` runs `gzip` on top of a `tar` archive, so archiving and compressing happen in one pass.

#### 1.2 Common compression algorithms and archive formats

All of these formats have ready-made packages in the Go standard library — just pick one that fits:

**Compression algorithms**:

- **gzip**: high compression ratio, fast decompression, and by far the most used. Go package: `compress/gzip`
- **zlib**: a lossless compression library based on DEFLATE. Go package: `compress/zlib`
- **bzip2**: a higher compression ratio than `gzip`, at the cost of slower compression. Go package: `compress/bzip2`

**Archive formats**:

- **tar**: common on Unix, bundles multiple files and directories into a single file. Go package: `archive/tar`
- **zip**: packs and compresses in one operation. Go package: `archive/zip`

## References

- [compress/gzip standard library](https://pkg.go.dev/compress/gzip)
- [compress/flate standard library](https://pkg.go.dev/compress/flate)


## Sibling pages

- [Advanced](/compress/Advanced.md)
- [Archive](/compress/Archive.md)
- [Composite](/compress/Composite.md)
- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ErrHandleAndTest](/compress/ErrHandleAndTest.md)
