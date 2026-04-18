# Simple Commands - Easy to Copy & Paste

## Just 3 Simple Commands

### Command 1: See Issues
```bash
python3 linter.py features/
```

### Command 2: Fix Everything
```bash
python3 auto_fix.py features/ --output fixed_features/
```

### Command 3: Check Fixed Files
```bash
python3 linter.py fixed_features/
```

---

That's it! Just run these 3 commands one by one in terminal.

---

## What Each Command Does

| Command | What It Does |
|---------|------------|
| `python3 linter.py features/` | Shows all problems in feature files |
| `python3 auto_fix.py features/ --output fixed_features/` | Fixes all problems and saves to `fixed_features/` folder |
| `python3 linter.py fixed_features/` | Shows remaining problems (should be much less) |

---

## Optional Simple Commands (If you want to explore)

### See fixed files list
```bash
ls fixed_features/
```

### Compare one file before/after
```bash
diff features/browser_navigation.feature fixed_features/browser-navigation.feature
```

### Show one fixed file content
```bash
cat fixed_features/browser-navigation.feature
```

---

**That's all you need!** 🎉
