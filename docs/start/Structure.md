This page compares the directory layouts of a regular application project and a library project, side by side.

### Regular project directory layout

A regular project is usually a complete application, containing several executables and the resources that go with them.

```
myproject/
├── cmd/
│   └── myapp/
│       └── main.go
├── pkg/
│   └── mypackage/
│       ├── mypackage.go
│       └── mypackage_test.go
├── internal/
│   └── myinternalpackage/
│       ├── myinternalpackage.go
│       └── myinternalpackage_test.go
├── api/
│   ├── api.go
│   └── api_test.go
├── web/
│   ├── static/
│   └── templates/
├── configs/
│   └── config.yaml
├── scripts/
│   └── build.sh
├── deployments/
│   └── docker/
│       └── Dockerfile
├── test/
│   └── e2e/
│       └── e2e_test.go
├── docs/
│   └── README.md
├── tools/
│   └── tools.go
├── examples/
│   └── example.go
└── go.mod
└── go.sum
```

#### Folders and what they do

##### `cmd/`
Holds the application's entry-point files. Each subdirectory stands for one standalone executable.

- **`main.go`**: contains the `main` function, the program's entry point.

##### `pkg/`
Public library code, visible to the outside and usable by other projects.

- **`mypackage/`**: package and test code that this project and external ones can use.

##### `internal/`
Private library code, visible only inside this project. It keeps other projects from depending on this code by accident.

- **`myinternalpackage/`**: private package and test code.

##### `api/`
API-related code: protocol definitions, API handling logic, and so on.

- **`api.go`**: the API implementation.
- **`api_test.go`**: API tests.

##### `web/`
Web-related resource files.

- **`static/`**: static assets such as JavaScript, CSS, and images.
- **`templates/`**: HTML templates.

##### `configs/`
Config files, holding the project's various settings, such as YAML and JSON files.

- **`config.yaml`**: a sample config file.

##### `scripts/`
Build, deployment, and automation scripts of all kinds.

- **`build.sh`**: a sample build script.

##### `deployments/`
Deployment-related files and configuration, such as Docker config files, Kubernetes config files, and so on.

- **`docker/`**: Docker-related config files.
  - **`Dockerfile`**: the Docker build file.

##### `test/`
Test-related code and resources, especially end-to-end (E2E) tests.

- **`e2e/`**: end-to-end test code.
  - **`e2e_test.go`**: a sample end-to-end test.

##### `docs/`
Project documentation, possibly including a README, API docs, and so on.

- **`README.md`**: the project's main documentation.

##### `tools/`
Tool code and scripts, possibly including development and build tools.

- **`tools.go`**: tool-related code.

##### `examples/`
Example code showing how to use the project's packages and functions.

- **`example.go`**: example code demonstrating the project's features.

##### `go.mod` and `go.sum`
Go module management files.

- **`go.mod`**: defines the module path, dependency versions, and so on.
- **`go.sum`**: records the exact versions and checksums of module dependencies.

### Library project directory layout

A library project mainly provides library code that other projects can depend on and use, so its layout differs somewhat, with the emphasis on code reuse and documentation.

```
mylibrary/
├── pkg/
│   └── mylibrary/
│       ├── mylibrary.go
│       └── mylibrary_test.go
├── internal/
│   └── myinternal/
│       ├── myinternal.go
│       └── myinternal_test.go
├── examples/
│   └── example.go
├── docs/
│   └── README.md
├── test/
│   └── e2e/
│       └── e2e_test.go
├── tools/
│   └── tools.go
└── go.mod
└── go.sum
```

#### Folders and what they do

##### `pkg/`
Public library code, visible to the outside and usable by other projects.

- **`mylibrary/`**: library and test code that this project and external ones can use.

##### `internal/`
Private library code, visible only inside this project. It keeps other projects from depending on this code by accident.

- **`myinternal/`**: private library and test code.

##### `examples/`
Example code showing how to use the library's packages and functions.

- **`example.go`**: example code demonstrating the library's features.

##### `docs/`
Project documentation, possibly including a README, API docs, and so on.

- **`README.md`**: the project's main documentation.

##### `test/`
Test-related code and resources, especially end-to-end (E2E) tests.

- **`e2e/`**: end-to-end test code.
  - **`e2e_test.go`**: a sample end-to-end test.

##### `tools/`
Tool code and scripts, possibly including development and build tools.

- **`tools.go`**: tool-related code.

##### `go.mod` and `go.sum`
Go module management files.

- **`go.mod`**: defines the module path, dependency versions, and so on.
- **`go.sum`**: records the exact versions and checksums of module dependencies.

### Notes

Two things actually make this layout work. One is visibility: code under `pkg/` can be imported by other projects, code under `internal/` only by this one, and the Go toolchain enforces that line directly. The other is finding things fast: entry points in `cmd/`, scripts in `scripts/`, deployment manifests in `deployments/` — the directory name alone gets you there. On top of that it's the common community layout, so other people can read your repo without much effort.

This layout is a recommended starting point; adjust it to fit your project's actual needs.

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)


## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Build](/start/Build.md)
- [Embed](/start/Embed.md)
- [Starter](/start/Starter.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Starter](/start/Starter.md)
