# Contribution roadmap

Small, useful improvements are welcome. These are proposed contribution areas, not completed features or release promises. Before substantial work, open an issue to agree on scope.

| Area | Small starting task | Acceptance evidence |
| --- | --- | --- |
| Client examples | Add a JavaScript support-routing client | One authenticated request, clear error handling, no key logging |
| Installation | Validate the documented Windows Python 3.12 setup | OS/runtime versions, reproducible steps, sanitized result |
| Documentation | Explain a common setup failure | Reproduction and a verified fix; English and Chinese links stay valid |
| Evaluation | Add a small labeled support-routing dataset | Data source/license, expected labels, evaluation command |
| Deployment | Design a model-cache volume recipe | Fresh-container startup, no embedded keys, supported architecture stated |

For an approachable issue, maintainers should identify files, expected behavior, and verification steps before applying `good first issue`. A complete task description is more useful than an empty label.

Longer-term priorities: reproducible latency/memory/accuracy measurements, verified multi-architecture images, and real integration feedback. No performance or accuracy threshold is claimed yet.
