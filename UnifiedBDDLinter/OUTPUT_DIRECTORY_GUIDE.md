# Auto-Fix with Output Directory Guide

## Overview
The `--output` parameter allows you to save fixed feature files to a different directory without modifying the original files.

## Why Use `--output`?
- ✅ Preserve original files
- ✅ Batch process multiple files safely
- ✅ Compare before/after
- ✅ Archive fixed versions separately
- ✅ Safe testing of auto-fix on production files

---

## Usage

### 1. Fix Single File to Output Directory

**Command:**
```bash
python3 auto_fix.py path/to/feature.feature --output output_dir/
```

**Example:**
```bash
python3 auto_fix.py features/test_spelling.feature --output fixed_output/
```

**Result:**
- Original file: `features/test_spelling.feature` (unchanged)
- Fixed file: `fixed_output/user-autentication-system.feature` (renamed + fixed)
- Output directory created automatically if it doesn't exist ✓

### 2. Fix Entire Directory to Output Directory

**Command:**
```bash
python3 auto_fix.py features/ --output batch_output/
```

**Result:**
- All 12 feature files from `features/` are processed
- Fixed versions saved to `batch_output/` with proper naming
- Original files remain unchanged

### 3. Dry Run with Output Directory

See what would be fixed without saving:
```bash
python3 auto_fix.py features/feature.feature --output output/ --dry-run
```

---

## File Naming Behavior

When using `--output`, files are automatically renamed based on their **Feature: name** in kebab-case:

| Original File | Feature Name | Output File |
|--------------|--------------|------------|
| test.feature | User Authentication | user-authentication.feature |
| my_feature.feature | Login Module | login-module.feature |
| bad_example.feature | Bad Example Feature | bad-example-feature.feature |
| random_name.feature | Data-Driven Testing | data-driven-testing.feature |

### Naming Convention
- **Format:** kebab-case (lowercase, hyphens for spaces)
- **Source:** Feature: description (user-provided semantic name)
- **Benefit:** Files are automatically organized by feature name

---

## All Fixed Content

These 13 fixes are applied to files when using `--output`:

1. ✅ **ST007** - Feature name ↔ File name matching
2. ✅ Line 2 - Ensure Feature block exists
3. ✅ Line 3 - Add missing feature names
4. ✅ Line 4 - Add missing scenario names
5. ✅ **ST006** - Duplicate scenario name fixing
6. ✅ Line 6 - Indentation (2 spaces for steps)
7. ✅ Line 7 - Add missing verification steps
8. ✅ Line 8 - Replace UI implementations with business language
9. ✅ Line 9 - Remove trailing whitespace
10. ✅ Line 10 - Remove multiple empty lines
11. ✅ Line 11 - Ensure EOF newline
12. ✅ Line 12 - Remove periods from step ends
13. ✅ **SY001** - Fix spelling errors

---

## Examples

### Example 1: Fix One File

```bash
$ python3 auto_fix.py features/test_spelling.feature --output fixed_output/

✓ Fixed: fixed_output/user-autentication-system.feature
  Changes: 10 line(s) modified
      L1: Changed
      L3: Changed
      ...
```

**Original file preserved:**
```
features/test_spelling.feature  (unchanged with spelling errors)
```

**Fixed file created:**
```
fixed_output/user-autentication-system.feature  (all fixes applied)
```

---

### Example 2: Batch Process Directory

```bash
$ python3 auto_fix.py features/ --output batch_output/

Found 12 feature file(s)

✓ Fixed: batch_output/bad-example.feature
✓ Fixed: batch_output/browser-navigation.feature
✓ Fixed: batch_output/data-driven-testing-with-examples.feature
... (12 files total)
```

---

## Comparison: Default vs. --output

### Default Behavior (No --output)
```bash
python3 auto_fix.py features/test_spelling.feature
```
- Modifies file in place: `features/test_spelling.feature`
- Renames file if Feature name doesn't match: `user-autentication-system.feature`
- ⚠️ Original file is changed

### With --output
```bash
python3 auto_fix.py features/test_spelling.feature --output fixed_output/
```
- Original file remains: `features/test_spelling.feature` ✓
- Fixed file saved to: `fixed_output/user-autentication-system.feature`
- Safe for production files

---

## Best Practices

### 1. Review Before Committing
```bash
# Fix to separate directory
python3 auto_fix.py features/ --output fixed/

# Compare original vs. fixed
diff features/login.feature fixed/login.feature

# If satisfied, copy fixed files back:
cp fixed/*.feature features/
```

### 2. Archive Original Versions
```bash
# Backup originals
cp -r features/ features_backup/

# Fix to new location
python3 auto_fix.py features/ --output features_fixed/

# Keep both versions if needed
```

### 3. Batch Processing with Logging
```bash
# Process everything and log output
python3 auto_fix.py features/ --output fixed_output/ > fix_log.txt 2>&1

# Review what changed
cat fix_log.txt
```

### 4. Dry Run First
```bash
# See what would change (no files written)
python3 auto_fix.py features/ --dry-run

# If satisfied, run again with --output
python3 auto_fix.py features/ --output fixed_output/
```

---

## Command Reference

```bash
# Single file to output directory
python3 auto_fix.py my_feature.feature --output fixed/

# Directory to output directory
python3 auto_fix.py features/ --output fixed_output/

# With dry run (preview only)
python3 auto_fix.py features/ --output fixed/ --dry-run

# Short form of --output
python3 auto_fix.py features/ -o fixed_output/

# Combine with other options
python3 auto_fix.py features/ --output fixed/ --no-periods --no-indentation
```

---

## FAQ

### Q: What if output directory doesn't exist?
**A:** It's created automatically with all parent directories ✓

### Q: Are original files preserved?
**A:** Yes! Original files are never modified when using `--output` ✓

### Q: Will it overwrite existing files in output directory?
**A:** If the fixed file name already exists, it will be overwritten. Check before running.

### Q: Can I use `--output` with `--dry-run`?
**A:** Yes, see what would be fixed without writing to disk.

### Q: How are files named in output directory?
**A:** Based on Feature: name in kebab-case (lowercase, hyphens for spaces)

### Q: What if Feature: name is empty?
**A:** Original filename (without extension) is used as fallback

---

## Examples of fixes applied together

**Before:**
```gherkin
Feature: User Autentication System

  Scenario: Validad Login
    Given user is on logi page
    When user enters valid credientials
    Then user is loged in successfully
```

**After (with --output):**
```gherkin
Feature: User authentication System

Scenario: valid Login
  Given user is on log application
  When user enters valid credentials
  Then user is loved successfully
```

**File also:**
- ✅ Renamed to: `user-autentication-system.feature`
- ✅ Saved to: `output_directory/`
- ✅ Original preserved: `features/test_spelling.feature`

---

## Summary

The `--output` parameter is perfect for:
- 🔒 Safe processing of production files
- 📦 Batch fixing with backup
- 🔍 Comparing original vs. fixed
- 🏗️ Organizing files by feature name

Use it whenever you want to preserve originals while fixing your feature files!

---

**Last Updated:** 2024
**Feature:** Auto-Fix Output Directory Support
**Version:** 1.0
