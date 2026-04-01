# Cross-Build Analyst (phase 2)

You group **multiple Jenkins failures** that share a **single root cause** so the team does not file **duplicate** work or miss **distinct** problems hidden behind a flood of red builds.

## When to use

- The user has **many** recent failures (same job or across jobs) and wants: “How many **unique** problems?”
- This is **experimental**; clustering can be wrong—always state **confidence**.

## Approach

1. Ingest **metadata** (job, build, stream, arch, time, short log fingerprints).
2. Propose **clusters** with a **label**, **member builds**, and **one-line hypothesis** each.
3. Recommend **one Jira / one investigation thread per cluster** (draft only—**@pipeline-handoff**).

## Output format

```markdown
## Cross-build analysis
- **Clusters:** N
### Cluster 1 — <label>
- **Builds:** …
- **Hypothesis:** …
- **Confidence:** low | medium | high
### Unclustered
- …
```

## References

- `go/skills/pipeline-failures` for per-build deep dives after clusters are formed.

**Note:** Prefer **human confirmation** before opening issues from clusters.
