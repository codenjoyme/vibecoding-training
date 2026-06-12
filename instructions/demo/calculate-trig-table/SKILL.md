# Skill: Calculate Trig Table

**Version:** 1.0.0

## Description

Generate a deterministic trigonometric table for a degree range using Python stdlib `math` only.

## Usage

```bash
python instructions/calculate-trig-table/scripts/calculate.py --start 0 --end 90 --step 15 --format md
python instructions/calculate-trig-table/scripts/calculate.py --start 0 --end 90 --step 15 --format json --output output/trig.json
python instructions/calculate-trig-table/scripts/calculate.py --start 0 --end 90 --step 15 --format csv --output output/trig.csv
```

## Notes

- Deterministic: same arguments always produce identical values.
- Runtime computation is script-based (no model calls inside the script).
- Use as a reference for script + `SKILL.md` packaging and verification flow.
