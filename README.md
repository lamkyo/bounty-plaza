# DAXDA Recursive Bounty System

This package implements Bounty Plaza #645 as a deterministic, local-first catalog of five self-similar domain bounties:

| Domain | ID | Value |
|---|---|---:|
| Cl(16,4) | `DAXDA-CL164` | $7,500 |
| Containment | `DAXDA-CONTAINMENT` | $7,500 |
| DA13 | `DAXDA-DA13` | $7,500 |
| Chrono | `DAXDA-CHRONO` | $7,500 |
| MMPIBench | `DAXDA-MMPIBENCH` | $7,000 |

Run the machine-readable catalog with `python -m daxda_bounties`. Run tests with `python -m pytest`.
Each bounty exposes `create_sub_bounty(...)`; the child inherits the same contract and records its parent ID.

