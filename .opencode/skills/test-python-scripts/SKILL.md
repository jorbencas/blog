---
name: test-python-scripts
description: Generate/update pytest tests for modified Python scripts under scripts/
---

# test-python-scripts

Generate or update pytest tests for Python scripts that have been modified in the current session. Run this skill once after ALL changes are complete, not after each individual file edit.

## When to use

- One or more files under `scripts/` have been modified
- No new Python scripts have been added (those are handled separately)
- All functional changes to the scripts are finished and the build passes

## Process

### Step 1 — Identify changed scripts

Run `git diff --name-only HEAD` to find which files under `scripts/` were modified.

For each modified file `scripts/<name>.py` (excluding `__pycache__`), determine the corresponding test file path:

- `scripts/fix_images.py` → `tests/python/test_fix_images.py`
- `scripts/solutions_db.py` → `tests/python/test_solutions_db.py`
- etc.

If no test file exists yet for a given script, it needs to be created.

### Step 2 — Read existing test patterns

Before writing tests, read at least one existing test file (e.g., `tests/python/test_solutions_db.py`) to understand:

- Import style: `from scripts.<module> import <symbol>`
- Test class structure: `class Test<Feature>:` with `test_<desc>` methods
- Assertion style: plain `assert` statements
- No fixtures, no `unittest.TestCase`, no `__init__.py`
- Helper functions defined at module level (not as fixtures)

### Step 3 — Read the changed script

Read the full content of each changed `scripts/<name>.py` to identify:

- Public functions and their signatures
- Edge cases the functions might encounter
- Which functions are pure (no I/O, no side effects) — prefer these for testing
- Functions that call external APIs or read files — those should NOT be tested (mark them as out of scope in a comment)

### Step 4 — Generate/update the test file

For each changed script:

**If the test file already exists:**
- Add new test classes/methods for any new functions added to the script
- Do NOT remove existing tests unless a function was removed
- Keep the existing structure and style

**If the test file is new:**
- Create `tests/python/test_<name>.py`
- Use the same import pattern as existing tests
- Group tests by function in `Test*` classes
- Test pure functions only
- Include edge cases: empty inputs, boundary values, type mismatches, special characters

**Complexity comment:** If the tested function contains non-trivial logic (loops, recursion, branching beyond simple conditionals, or external state handling), add a comment at the top of the test class explaining what the function does, for example:
```python
# TestNormalizeKey: tests key normalization for DB lookups —
# handles Unicode folding, whitespace stripping, stop-word removal
```

### Step 5 — Verify the tests pass

Run the newly created or modified tests:

```bash
python3 -m pytest tests/python/test_<name>.py -v
```

If any test fails:
1. Read the error message and traceback
2. Fix the test (or the source code if the test revealed a bug)
3. Re-run until all tests pass

Do NOT skip this step. Tests that don't pass are worse than no tests.

## Convention reference

- Test directory: `tests/python/` (no `__init__.py`)
- Framework: pytest, class-based (no `unittest.TestCase`)
- Imports: `from scripts.<module> import <symbol>`
- Assertions: plain `assert`
- Commands: `python3 -m pytest tests/python/ -v` (or for a single file: `python3 -m pytest tests/python/test_<name>.py -v`)
- Config: `pyproject.toml` sets `testpaths = ["tests/python"]`
