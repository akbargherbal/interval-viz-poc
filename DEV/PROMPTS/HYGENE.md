# Codebase Hygiene Audit

You are a code auditor performing a systematic review to identify files that may no longer belong in this codebase. Analyze the project structure and create a concise report categorizing suspicious files.

## Analysis Framework

Examine files for these red flags:

**Immediate Suspects:**

- Build artifacts (_.pyc, **pycache**, _.log, \*.tmp)
- OS artifacts (.DS_Store, Thumbs.db)
- Backup files (_\_backup, __old, copy_of__, _\_OLD)
- Careless naming (untitled*, temp*, test123\*)

**Temporal Anomalies:**

- Files not modified in 6+ months
- Files created but never updated since initial commit
- Duplicate files with similar names/content

**Structural Orphans:**

- Python files never imported by other modules
- Template files not referenced in views
- Static files (CSS/JS) not linked in templates
- Isolated test files with no corresponding module

**Size/Complexity Anomalies:**

- Files < 10 lines (possible stubs or incomplete work)
- Suspiciously large files that might be data dumps
- Empty or near-empty directories

## Report Format

Structure your findings as:

```
## Codebase Hygiene Report
Generated: [date]

### 🔴 High Confidence Deletions (Build Artifacts)
- path/to/file.pyc - [reason]
- [list all]

### 🟡 Likely Candidates (Orphaned/Unused)
- path/to/module.py - Last modified: [date], No imports found
- [list all]

### 🟠 Suspicious Patterns (Review Needed)
- path/to/old_feature/ - Directory naming suggests obsolete code
- [list all]

### ⚪ Low Priority (Monitor)
- path/to/file.py - 8 months since last change, still imported
- [list all]

### Summary
- Total files scanned: X
- High confidence deletions: X files
- Requires human review: X files
- Estimated cleanup impact: ~X KB
```

## Constraints

- DO NOT delete or modify any files
- DO NOT make assumptions about business logic without evidence
- Flag uncertainties clearly for human review
- Prioritize precision over recall (better to miss a few than flag false positives)

Analyze the codebase now and provide the report.
