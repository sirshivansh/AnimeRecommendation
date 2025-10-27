import pandas as pd

# Load dataset
data = pd.read_csv("anime.csv")

print("="*60)
print("CHECKING IMAGE DATA IN DATASET")
print("="*60)

# Check if main_picture column exists
if 'main_picture' in data.columns:
    print("\n✓ 'main_picture' column found!")
    
    # Show sample data
    print("\n📸 Sample image data (first 5 entries):")
    print("-"*60)
    for i in range(min(5, len(data))):
        print(f"\n{i+1}. {data.iloc[i]['title']}")
        print(f"   Image data: {str(data.iloc[i]['main_picture'])[:100]}...")
    
    # Count how many have images
    non_null = data['main_picture'].notna().sum()
    total = len(data)
    print(f"\n📊 Statistics:")
    print(f"   Total anime: {total}")
    print(f"   With images: {non_null} ({non_null/total*100:.1f}%)")
    print(f"   Without images: {total - non_null} ({(total-non_null)/total*100:.1f}%)")
    
else:
    print("\n❌ 'main_picture' column NOT found!")
    print("\nAvailable columns:")
    for col in data.columns:
        print(f"   - {col}")

print("\n" + "="*60)