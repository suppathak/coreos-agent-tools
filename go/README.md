# Go CLI (`coreos-tools`)

This directory holds the **Go** implementation of Jenkins / pipeline helpers (`cmd/coreos-tools`).

**Skills for Claude/OpenCode** live at repo root **`../skills/`** (not under `go/`), so contributors do not confuse markdown playbooks with Go packages.

- Build (from `go/`): `go build -o bin/coreos-tools ./cmd/coreos-tools`
- OpenCode/agent container (from repo root): `podman build -f go/Dockerfile.agent -t coreos-agent .` — see comments in **`Dockerfile.agent`**; it **`COPY skills/`** from the parent directory.
