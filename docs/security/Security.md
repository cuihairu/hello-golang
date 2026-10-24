# Official security guidance and the `crypto` standard library


> Perspective: this page rounds up Go's official security guidance and the entry points into crypto; for file/IO and database scenarios see [IO security notes](/io/Security.md) and [database security notes](/db/Security.md).
The officials list security as its own section under Why Go, titled How Go can help keep you secure by default. This repo previously had no `crypto/`-related content; this page copies down the official guidance and gives entry points for further reading. Fetched on 2026-10-08.

## 1. The four things the officials list

1. **Vulnerability database**: the Go Vulnerability Database, where you can browse reports, look up documentation, and submit vulnerabilities publicly. The Security Policy page spells out how the security team tracks issues and discloses them to the public, and points to the security-fix records in the release history.
2. **Fix coverage**: per the release policy, security fixes are shipped to the **last two major versions**. This is the same rule as the support policy in `docs/zh/introduction/ReleaseNotes.md`.
3. **fuzzing**: finding bugs by continuously varying inputs in automated tests. Since **1.18**, Go ships native fuzzing built into the standard toolchain, and native fuzz tests are supported by OSS-Fuzz.
4. **Crypto libraries**: the officials say the goal of Go's crypto libraries is to help developers build secure applications; the entry points are the standard library's `crypto` package and `golang.org/x/crypto/`; Go's crypto libraries can also be used in **FIPS 140-3 compliance mode**, aimed at environments with compliance requirements.

## 2. How to find the application-relevant `crypto` packages

The standard library package documentation is the crypto group on pkg.go.dev; `golang.google.cn/pkg/` also opens directly. Grouped by purpose:

| Purpose | Package |
| --- | --- |
| Transport encryption | `crypto/tls` (what HTTPS sits on), `crypto/x509` (certificates) |
| Digests | `crypto/sha256`, `crypto/sha512`, `crypto/md5` (only for checking legacy data, not for security purposes) |
| Message authentication and symmetric encryption | `crypto/hmac`, `crypto/aes`, `crypto/chacha20poly1305` |
| Asymmetric and signatures | `crypto/rsa`, `crypto/ecdsa`, `crypto/ed25519`, `crypto/rand` |
| Random numbers | `crypto/rand` (keys and tokens must use this one, not `math/rand`) |

The `math/rand` covered in `docs/zh/math/MathRand.md` is reproducible pseudo-randomness, good for shuffling and simulation; keys, nonces, and tokens always go through `crypto/rand` — do not mix the two.

## 3. Related pages already in this repo

| Page | What it covers |
| --- | --- |
| `docs/zh/io/Security.md` | security practices on the file and I/O side |
| `docs/zh/db/Security.md` | the database side, including SQL injection prevention |
| `docs/zh/net/Socket.md` | the underlying socket, with TLS layered on top |
| `docs/zh/encoding/Base64.md`, `docs/zh/encoding/Hex.md` | encoding, not encryption |

The gap is server-side `crypto/tls` configuration, certificates, and the handshake — this page only gives the entry points without expanding on them: expanding would need the official `crypto/tls` package documentation as backing, and this round of research did not pull enough original text.

## 4. Notes on the dependency side

The official vulnerability database covers the Go standard library and indexed modules. The third-party libraries that appear in this repo's pages (Gin, gORM, Kafka clients, and so on) are outside the standard library's scope; before upgrading, run a tool like `govulncheck` against your own dependency graph and let the tool's output be the verdict.

## Sources

1. https://golang.google.cn/security/ — the official security page: vulnerability database, security policy, fix coverage for the last two major versions, fuzzing, crypto libraries and FIPS 140-3 (fetched 2026-10-08)
2. https://golang.google.cn/doc/fuzz/ — native fuzzing started in Go 1.18, OSS-Fuzz support
3. https://golang.google.cn/doc/devel/release — security-fix coverage in the release policy
4. https://golang.google.cn/pkg/ — entry point for standard library package documentation

## References

- [Official · Go Security](https://go.dev/security/)
- [Official blog · Vulnerability Management for Go](https://go.dev/blog/vuln)
- [Official blog · Govulncheck v1.0.0](https://go.dev/blog/govulncheck)

<!-- BACKLINKS-AUTO -->
## Related pages

- [knowledge](/knowledge.md)
- [Plugin](/sys/Plugin.md)
