import pkgutil
import importlib
import os
import sys

ROOT = os.path.dirname(__file__)
TARGET = os.path.join(ROOT, "nba_safe_bets")

print("🔍 Verifying imports...\n")

failures = []

for loader, module_name, is_pkg in pkgutil.walk_packages([TARGET], prefix="nba_safe_bets."):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
    except Exception as e:
        print(f"❌ {module_name} — {e}")
        failures.append((module_name, str(e)))

print("\n───────────────────────────────")
if failures:
    print("❌ Some imports FAILED:")
    for mod, error in failures:
        print(f" - {mod}: {error}")
else:
    print("🎉 ALL IMPORTS LOADED SUCCESSFULLY!")
