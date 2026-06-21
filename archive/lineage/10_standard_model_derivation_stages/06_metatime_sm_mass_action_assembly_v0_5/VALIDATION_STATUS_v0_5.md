# Validation Status v0.5

- Package contains no nested archives.
- Generation seed assignment uses no mass input.
- Observed masses are used only as validation targets after assignment.
- Ordering validation passes for charged leptons, up-type quarks, and down-type quarks.
- Absolute mass prediction is not claimed.

## Summary JSON

```json
[
  {
    "family": "charged_leptons",
    "spearman_rank_match": 1.0,
    "model_rank_desc": "{\"e\": 1, \"mu\": 2, \"tau\": 3}",
    "target_rank_desc": "{\"e\": 1, \"mu\": 2, \"tau\": 3}",
    "status": "PASS_order_only"
  },
  {
    "family": "up_type_quarks",
    "spearman_rank_match": 1.0,
    "model_rank_desc": "{\"u\": 1, \"c\": 2, \"t\": 3}",
    "target_rank_desc": "{\"u\": 1, \"c\": 2, \"t\": 3}",
    "status": "PASS_order_only"
  },
  {
    "family": "down_type_quarks",
    "spearman_rank_match": 1.0,
    "model_rank_desc": "{\"d\": 1, \"s\": 2, \"b\": 3}",
    "target_rank_desc": "{\"d\": 1, \"s\": 2, \"b\": 3}",
    "status": "PASS_order_only"
  }
]
```
