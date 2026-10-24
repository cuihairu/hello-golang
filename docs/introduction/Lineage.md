### The genealogy chart of the Go language

This chart shows where Go came from and the languages it influenced.

```mermaid
graph TB
  A[BCPL] --> B[B]
  B --> C[C]
  C --> D[Unix]
  C --> E[Pascal]
  D --> F[C++]
  E --> G[Modula]
  F --> H[AWK]
  G --> I[Oberon]
  H --> J[Perl]
  I --> K[Limbo]
  J --> L[Python]
  K --> M[Newsqueak]
  M --> N[Alef]
  N --> O[Plan 9]
  O --> P[Go]
  L --> Q[Java]
  Q --> R[C#]
  R --> S[Scala]
  S --> P
  H --> P
  I --> P
  J --> P
  K --> P

  style A fill:#f9f,stroke:#333,stroke-width:4px
  style B fill:#f9f,stroke:#333,stroke-width:4px
  style C fill:#f9f,stroke:#333,stroke-width:4px
  style D fill:#f9f,stroke:#333,stroke-width:4px
  style E fill:#f9f,stroke:#333,stroke-width:4px
  style F fill:#f9f,stroke:#333,stroke-width:4px
  style G fill:#f9f,stroke:#333,stroke-width:4px
  style H fill:#f9f,stroke:#333,stroke-width:4px
  style I fill:#f9f,stroke:#333,stroke-width:4px
  style J fill:#f9f,stroke:#333,stroke-width:4px
  style K fill:#f9f,stroke:#333,stroke-width:4px
  style L fill:#f9f,stroke:#333,stroke-width:4px
  style M fill:#f9f,stroke:#333,stroke-width:4px
  style N fill:#f9f,stroke:#333,stroke-width:4px
  style O fill:#f9f,stroke:#333,stroke-width:4px
  style P fill:#0f0,stroke:#333,stroke-width:4px
  style Q fill:#0ff,stroke:#333,stroke-width:4px
  style R fill:#0ff,stroke:#333,stroke-width:4px
  style S fill:#0ff,stroke:#333,stroke-width:4px
```


You can read this chart in four blocks: origin, evolution, birth, and influence.

- **Origin**:
  - BCPL, B, and C are Go's ancestor languages, representing the early evolution of programming languages.
  - Systems and languages such as Unix and Pascal had an important influence on the development of C and C++.

- **Evolution**:
  - Languages such as C++, AWK, and Modula grew out of C.
  - Scripting languages such as Perl and Python simplified programming and improved development efficiency.
  - Java and C# introduced object-oriented programming and garbage collection.
  - Squeak and Newsqueak provided the basis for concurrent programming.

- **The birth of Go**:
  - Go absorbed the lessons of these languages — C-family syntax, the ease of scripting languages, the concurrency model, garbage collection — and made them into a language with concise syntax and built-in concurrency support.

- **Influence**:
  - Go is widely used in cloud computing, containerization, and microservices: projects such as Docker, Kubernetes, gRPC, etcd, and Prometheus are all written in Go.

## References

- [Official documentation overview](https://go.dev/doc/)
- [Release history and support policy](https://go.dev/doc/devel/release)
- [Official FAQ](https://go.dev/doc/faq)

## Sibling pages

- [ReleaseNotes](/introduction/ReleaseNotes.md)
- [Feature](/introduction/Feature.md)
- [Introduction](/introduction/Introduction.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Feature](/introduction/Feature.md)
- [Introduction](/introduction/Introduction.md)
