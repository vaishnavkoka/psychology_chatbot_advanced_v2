# Quick Copy-Paste Commands (Cheat Sheet)

## Start Here - Copy & Paste These in Terminal

```bash
cd /home/vaishnavkoka/RE4BDD/UnifiedBDDLinter
```

---

## Main Workflow (Copy-Paste Each Line)

### See All Issues
```bash
python3 linter.py features/
```

### Fix Everything to fixed_features folder
```bash
python3 auto_fix.py features/ --output fixed_features/
```

### Verify Fixed Files
```bash
python3 linter.py fixed_features/
```

### Compare Results
```bash
echo "Original:" && python3 linter.py features/ 2>&1 | grep "Summary:" && echo -e "\nFixed:" && python3 linter.py fixed_features/ 2>&1 | grep "Summary:"
```

---

## See Specific Issues

### File Naming Mismatches
```bash
python3 linter.py features/ 2>&1 | grep "ST007"
```

### Indentation Problems
```bash
python3 linter.py features/ 2>&1 | grep "S004"
```

### Spelling Errors
```bash
python3 linter.py features/ 2>&1 | grep "SY001"
```

### Implementation Details
```bash
python3 linter.py features/ 2>&1 | grep "Q001"
```

---

## Compare Files

### Show differences for one file
```bash
diff features/browser_navigation.feature fixed_features/browser-navigation.feature
```

### Show original file
```bash
cat features/browser_navigation.feature
```

### Show fixed file
```bash
cat fixed_features/browser-navigation.feature
```

### List all fixed files
```bash
ls -lh fixed_features/
```

---

## Fix Single Files

### Fix one file to output folder
```bash
python3 auto_fix.py features/test_spelling.feature --output my_output/
```

### See what would change (don't save)
```bash
python3 auto_fix.py features/test_spelling.feature --dry-run
```

---

## Save Reports

### Save original violations to file
```bash
python3 linter.py features/ > original_violations.txt 2>&1
```

### Save fixed violations to file
```bash
python3 linter.py fixed_features/ > fixed_violations.txt 2>&1
```

### View the reports
```bash
cat original_violations.txt
cat fixed_violations.txt
```

---

## Cleanup

### Remove fixed_features folder
```bash
rm -rf fixed_features/
```

### Remove all output folders
```bash
rm -rf my_output/ fixed_output/ batch_output/
```

### Clear reports
```bash
rm -f original_violations.txt fixed_violations.txt
```

---

## One-Command Complete Workflow

```bash
echo "=== BEFORE ===" && python3 linter.py features/ 2>&1 | tail -3 && echo -e "\n=== FIXING ===" && python3 auto_fix.py features/ --output fixed_features/ 2>&1 | tail -3 && echo -e "\n=== AFTER ===" && python3 linter.py fixed_features/ 2>&1 | tail -3
```

---

## Pro Tips

**See last 10 lines only:**
```bash
python3 linter.py features/ | tail -10
```

**Count violations by type:**
```bash
python3 linter.py features/ 2>&1 | grep -o "\[ERROR\]" | wc -l
```

**See only the summary:**
```bash
python3 linter.py features/ 2>&1 | grep "Summary:"
```

**Show file names being processed:**
```bash
python3 auto_fix.py features/ --output fixed_features/ 2>&1 | grep "✓"
```

---

**Print this page or keep terminal open while following commands!**
