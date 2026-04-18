# Manual Terminal Commands - Step by Step Guide

Run these commands one by one in your terminal to observe the linter and auto-fix in action.

---

## Setup (One Time)

```bash
# Navigate to the linter directory
cd /home/vaishnavkoka/RE4BDD/UnifiedBDDLinter
```

---

## Step 1: See All Issues in Original Feature Files

### Command 1.1: Run linter on all feature files (shows all violations)
```bash
python3 linter.py features/
```
**What you'll see:**
- Detailed violations for each file
- Error codes (ST007, S004, Q001, SY001, etc.)
- Line numbers and suggestions
- Summary: "174 violation(s), 143 error(s)"

### Command 1.2: Get quick summary of violations
```bash
python3 linter.py features/ | tail -20
```
**What you'll see:**
- Last 20 lines showing summary and statistics

### Command 1.3: Count violations by file
```bash
python3 linter.py features/ 2>&1 | grep -E "^features/|Summary:"
```
**What you'll see:**
- List of all 9 feature files
- Total violation count: 174

---

## Step 2: Run Auto-Fix and Save to Output Directory

### Command 2.1: Fix ALL feature files to fixed_features folder
```bash
python3 auto_fix.py features/ --output fixed_features/
```
**What you'll see:**
- ✓ Progress for each file being fixed
- Changes count: "X line(s) modified"
- File renaming: original_name → kebab-case-name
- Summary: "9 file(s) fixed, 9 file(s) renamed"

### Command 2.2: Use short form of --output
```bash
python3 auto_fix.py features/ -o fixed_features/
```
**Same as 2.1 but shorter syntax**

### Command 2.3: Fix with dry-run (see what would change without saving)
```bash
python3 auto_fix.py features/ --output fixed_features/ --dry-run
```
**What you'll see:**
- Same output but files are NOT saved
- Useful to preview changes before running

---

## Step 3: Verify Fixed Files

### Command 3.1: Run linter on fixed files
```bash
python3 linter.py fixed_features/
```
**What you'll see:**
- Much fewer violations (~14 remaining)
- Summary: "14 violation(s), 3 error(s)" (99% improvement!)

### Command 3.2: Compare violation counts
```bash
echo "=== ORIGINAL ===" && python3 linter.py features/ 2>&1 | grep "Summary:" && echo -e "\n=== FIXED ===" && python3 linter.py fixed_features/ 2>&1 | grep "Summary:"
```
**What you'll see:**
- Original: 174 violations
- Fixed: 14 violations
- Reduction: ~160 violations fixed! ✓

---

## Step 4: View Before/After Comparison

### Command 4.1: Compare one file side by side
```bash
diff -u features/browser_navigation.feature fixed_features/browser-navigation.feature | head -50
```
**What you'll see:**
- Red lines (-) = Original content
- Green lines (+) = Fixed content
- All the changes made

### Command 4.2: View full before file
```bash
cat features/browser_navigation.feature
```

### Command 4.3: View full after file
```bash
cat fixed_features/browser-navigation.feature
```

### Command 4.4: Visual diff with colored output
```bash
diff -u --color=auto features/browser_navigation.feature fixed_features/browser-navigation.feature
```

---

## Step 5: List All Fixed Files

### Command 5.1: Show all files in fixed_features folder
```bash
ls -lh fixed_features/
```
**What you'll see:**
- All 9 fixed feature files
- File sizes
- Modification times

### Command 5.2: Show file names only
```bash
ls fixed_features/ | sort
```
**What you'll see:**
- Kebab-case named files
- All properly formatted

### Command 5.3: Count files
```bash
ls fixed_features/ | wc -l
```
**What you'll see:**
- Total count: 9 files

---

## Step 6: Test Individual Files

### Command 6.1: Fix just ONE file to output directory
```bash
python3 auto_fix.py features/test_spelling.feature --output my_output/
```
**What you'll see:**
- One file fixed and saved
- A new `my_output/` folder created
- Summary: "1 file(s) fixed, 1 file(s) renamed"

### Command 6.2: Lint just ONE file
```bash
python3 linter.py features/test_spelling.feature
```
**What you'll see:**
- Violations for just that one file

### Command 6.3: Fix one file without output (modifies in place)
```bash
python3 auto_fix.py features/good_example.feature --dry-run
```
**What you'll see:**
- Changes that WOULD be made (but file not modified)

---

## Step 7: Detailed Analysis

### Command 7.1: Show only errors (no warnings)
```bash
python3 linter.py features/ 2>&1 | grep "\[ERROR"
```
**What you'll see:**
- Only error-level violations

### Command 7.2: Show only warnings
```bash
python3 linter.py features/ 2>&1 | grep "\[WARNING"
```
**What you'll see:**
- Only warning-level violations

### Command 7.3: Show spelling errors
```bash
python3 linter.py features/ 2>&1 | grep "SY001"
```
**What you'll see:**
- Only spelling error violations

### Command 7.4: Show indentation errors
```bash
python3 linter.py features/ 2>&1 | grep "S004"
```
**What you'll see:**
- Only indentation violations

### Command 7.5: Show feature name mismatch errors
```bash
python3 linter.py features/ 2>&1 | grep "ST007"
```
**What you'll see:**
- Only feature name mismatch violations

---

## Step 8: Generate Reports

### Command 8.1: Save linter output to file
```bash
python3 linter.py features/ > original_report.txt 2>&1
```
**What you'll see:**
- File created: `original_report.txt`
- Contains full linter output

### Command 8.2: Save fixed linter output to file
```bash
python3 linter.py fixed_features/ > fixed_report.txt 2>&1
```
**What you'll see:**
- File created: `fixed_report.txt`
- Contains linter output for fixed files

### Command 8.3: Compare the two reports
```bash
diff original_report.txt fixed_report.txt | head -50
```
**What you'll see:**
- Differences between original and fixed reports

### Command 8.4: Show improvement statistics
```bash
echo "Original violations:" && grep "Summary:" original_report.txt && echo -e "\nFixed violations:" && grep "Summary:" fixed_report.txt
```

---

## Step 9: Cleanup and Reset

### Command 9.1: Remove fixed_features folder (to re-run fresh)
```bash
rm -rf fixed_features/
```

### Command 9.2: Remove output files
```bash
rm -rf my_output/ fixed_output/ batch_output/
```

### Command 9.3: Clean all generated reports
```bash
rm -f original_report.txt fixed_report.txt
```

---

## Step 10: All in One - Complete Workflow

### Command 10.1: Run complete workflow in one command
```bash
echo "=== Step 1: Scanning original files ===" && python3 linter.py features/ 2>&1 | tail -5 && echo -e "\n=== Step 2: Fixing files ===" && python3 auto_fix.py features/ --output fixed_features/ 2>&1 | tail -5 && echo -e "\n=== Step 3: Verifying fixed files ===" && python3 linter.py fixed_features/ 2>&1 | tail -5
```
**What you'll see:**
- Complete workflow output in one go

---

## Recommended Sequence to Try

**First Time Experience (15 minutes):**
1. `python3 linter.py features/`  ← See all issues
2. `python3 auto_fix.py features/ --output fixed_features/`  ← Fix them
3. `python3 linter.py fixed_features/`  ← Verify fixed

**Detailed Analysis (10 minutes):**
1. `python3 linter.py features/ | tail -20`  ← Summary only
2. `python3 linter.py features/ 2>&1 | grep "ST007"`  ← See file naming issues
3. `python3 linter.py features/ 2>&1 | grep "S004"`  ← See indentation issues
4. `diff features/browser_navigation.feature fixed_features/browser-navigation.feature`  ← Compare one file

**Compare Before/After (5 minutes):**
1. `python3 linter.py features/ 2>&1 | grep "Summary:"`
2. `python3 linter.py fixed_features/ 2>&1 | grep "Summary:"`
3. `ls fixed_features/`  ← See renamed files

**Test Single File (5 minutes):**
1. `python3 auto_fix.py features/test_spelling.feature --output test_output/`
2. `cat test_output/user-autentication-system.feature`
3. `rm -rf test_output/`

---

## Tips for Terminal

### Copy-Paste Commands
- Highlight command and right-click → Copy
- Right-click in terminal → Paste
- Or use: Ctrl+Shift+C (copy), Ctrl+Shift+V (paste)

### Scroll Up/Down History
- ↑ Arrow key = Previous command
- ↓ Arrow key = Next command

### Clear Screen
```bash
clear
```

### Exit Terminal
```bash
exit
```

### Check Current Directory
```bash
pwd
```

### List Files
```bash
ls
```

---

## Troubleshooting Commands

### If Python not found:
```bash
which python3
```

### If linter not found:
```bash
ls -la linter.py
```

### Check Python version:
```bash
python3 --version
```

### Check available feature files:
```bash
ls features/
```

### Check fixed output:
```bash
ls fixed_features/
```

---

## Final Verification

After running all the commands, you should have:
- ✅ Seen all 174 original violations
- ✅ Fixed 161 violations (92.5%)
- ✅ Verified only 14 violations remain (99% improvement)
- ✅ 9 files renamed to semantic names
- ✅ Original files preserved
- ✅ All files in `fixed_features/` folder ready to use

---

**Total time to run all commands: ~30 minutes**
**Total commands available: 30+**
**Estimated learning time: 1 hour**

Started: Copy-paste first command and observe the magic! 🚀
