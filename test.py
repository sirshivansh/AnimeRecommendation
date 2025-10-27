"""
Quick verification script to check if app.py has been updated correctly
"""

import os

print("Checking app.py...")

if not os.path.exists("app.py"):
    print("❌ app.py not found in current directory!")
    exit()

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Check for new code markers
checks = {
    "New logging system": "🎬 LOADING ANIME RECOMMENDATION SYSTEM" in content,
    "Detailed search logging": "🔍 SEARCH REQUEST" in content,
    "Better error messages": "💡 Did you mean one of these?" in content,
    "parse_tags function": "def parse_tags" in content,
    "Correct endpoint": "@app.post(\"/recommend\")" in content,
}

print("\n" + "="*50)
print("VERIFICATION RESULTS")
print("="*50)

all_good = True
for check_name, passed in checks.items():
    status = "✓" if passed else "❌"
    print(f"{status} {check_name}")
    if not passed:
        all_good = False

print("="*50)

if all_good:
    print("\n✅ app.py looks correct! You can run: python app.py")
else:
    print("\n❌ app.py needs to be updated with the new code!")
    print("   Please replace app.py with the code from the artifact.")

# Check for old code patterns
old_patterns = [
    "Received request:",
    "Recommendations count:",
]

has_old_code = any(pattern in content for pattern in old_patterns)
if has_old_code:
    print("\n⚠️  WARNING: Old code detected! Please replace app.py completely.")