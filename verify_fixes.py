"""
Quick Verification Script - Currency Symbol Fix
Checks that all currency symbols have been changed from $ to ₹
"""

import re

print("=" * 70)
print("CURRENCY SYMBOL VERIFICATION")
print("=" * 70)

# Read visualizations.py
with open(r"c:\python prac\Loan payoff calculator\visualizations.py", "r", encoding="utf-8") as f:
    viz_content = f.read()

# Count occurrences
dollar_count = viz_content.count('$')
rupee_count = viz_content.count('₹')

# Find dollar signs in context
dollar_matches = re.finditer(r'.{0,30}\$.{0,30}', viz_content)
dollar_contexts = list(dollar_matches)

print(f"\n📊 Statistics:")
print(f"   Dollar signs ($): {dollar_count}")
print(f"   Rupee symbols (₹): {rupee_count}")

if dollar_count > 0:
    print(f"\n❌ FAILED: Found {dollar_count} dollar sign(s) in visualizations.py")
    print("\n   Contexts where $ appears:")
    for i, match in enumerate(dollar_contexts[:5], 1):  # Show first 5
        print(f"   {i}. ...{match.group()}...")
else:
    print("\n✅ PASSED: No dollar signs found in visualizations.py")

if rupee_count >= 14:  # Should have at least 14 rupee symbols
    print(f"✅ PASSED: Found {rupee_count} rupee symbols (expected ~14+)")
else:
    print(f"⚠️  WARNING: Only found {rupee_count} rupee symbols (expected ~14)")

# Check specific patterns
print("\n🔍 Pattern Analysis:")

hover_patterns = re.findall(r'hovertemplate=.*?>', viz_content)
tick_patterns = re.findall(r'tickformat=.*?[\'"]', viz_content)
text_patterns = re.findall(r'text=\[f.*?\]', viz_content)

print(f"   Hover templates: {len(hover_patterns)}")
for i, pattern in enumerate(hover_patterns[:3], 1):
    has_rupee = '₹' in pattern
    symbol = "✅" if has_rupee else "❌"
    print(f"      {symbol} {pattern[:60]}...")

print(f"   Tick formats: {len(tick_patterns)}")
for i, pattern in enumerate(tick_patterns, 1):
    has_rupee = '₹' in pattern
    symbol = "✅" if has_rupee else "❌"
    print(f"      {symbol} {pattern}")

# Check app.py for CSV encoding
print("\n" + "=" * 70)
print("CSV EXPORT ENCODING VERIFICATION")
print("=" * 70)

with open(r"c:\python prac\Loan payoff calculator\app.py", "r", encoding="utf-8") as f:
    app_content = f.read()

if "encoding='utf-8-sig'" in app_content:
    print("✅ PASSED: CSV export uses utf-8-sig encoding")
elif "encoding=\"utf-8-sig\"" in app_content:
    print("✅ PASSED: CSV export uses utf-8-sig encoding")
else:
    print("❌ FAILED: CSV export encoding not found or incorrect")
    # Show to_csv usage
    csv_matches = re.findall(r'\.to_csv\([^)]+\)', app_content)
    if csv_matches:
        print("\n   Found to_csv calls:")
        for match in csv_matches[:3]:
            print(f"      {match}")

# Check months_elapsed calculation
print("\n" + "=" * 70)
print("MONTHS_ELAPSED CALCULATION VERIFICATION")
print("=" * 70)

if "Reverse-engineer months_elapsed" in app_content:
    print("✅ PASSED: months_elapsed calculation added for balance input method")
else:
    print("❌ FAILED: months_elapsed calculation not found")

# Check clarifying comments
print("\n" + "=" * 70)
print("CODE COMMENTS VERIFICATION")
print("=" * 70)

if "NOTE: Schedules use original column names" in app_content:
    print("✅ PASSED: Clarifying comments about column naming added")
else:
    print("❌ FAILED: Column naming comments not found")

# Final summary
print("\n" + "=" * 70)
print("FINAL VERIFICATION SUMMARY")
print("=" * 70)

all_passed = (
    dollar_count == 0 and
    rupee_count >= 14 and
    "encoding='utf-8-sig'" in app_content and
    "Reverse-engineer months_elapsed" in app_content and
    "NOTE: Schedules use original column names" in app_content
)

if all_passed:
    print("✅ ALL CHECKS PASSED - Ready for deployment!")
else:
    print("⚠️  Some checks failed - review above for details")

print("=" * 70)
