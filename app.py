from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from nltk.stem.porter import PorterStemmer
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize stemmer
ps = PorterStemmer()

def stem(text):
    """Apply stemming to text"""
    y = []
    for i in str(text).split():
        y.append(ps.stem(i))
    return " ".join(y)

def parse_tags(tag_string):
    """Parse tags from list format and apply stemming"""
    if pd.isna(tag_string) or tag_string == '' or tag_string == '[]':
        return ''
    
    tag_string = str(tag_string)
    words = re.findall(r"'([^']*)'", tag_string)
    if not words:
        words = re.findall(r'"([^"]*)"', tag_string)
    
    stemmed_words = [ps.stem(word) for word in words if word.strip()]
    return " ".join(stemmed_words)

print("\n" + "="*60)
print("🎬 LOADING ANIME RECOMMENDATION SYSTEM")
print("="*60)

# Load dataset
try:
    print("📂 Loading anime.csv...")
    data = pd.read_csv("anime.csv")
    print(f"✓ Loaded {len(data)} anime entries")
except FileNotFoundError:
    print("❌ ERROR: anime.csv not found!")
    exit()

# Prepare data
required_cols = ['anime_id', 'title', 'genres', 'themes', 'studios', 'producers', 'main_picture']
animes = data[required_cols].copy()

# Fill NaN values - keep main_picture as is for URLs
for col in ['genres', 'themes', 'studios', 'producers']:
    animes[col] = animes[col].fillna('[]')

# For main_picture, fill with empty string instead of '[]'
animes['main_picture'] = animes['main_picture'].fillna('')

print("🔧 Processing tags...")
animes['tags'] = (
    animes['genres'].astype(str) + ' ' +
    animes['themes'].astype(str) + ' ' +
    animes['studios'].astype(str) + ' ' +
    animes['producers'].astype(str)
)

animes['tags'] = animes['tags'].apply(parse_tags)
animes = animes[animes['tags'].str.strip() != ''].reset_index(drop=True)
print(f"✓ {len(animes)} anime with valid tags")

# Show sample titles
print("\n📺 Sample anime titles in database:")
for i, title in enumerate(animes['title'].head(10), 1):
    print(f"   {i}. {title}")

# Create vectors
print("\n🧠 Building recommendation model...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(animes['tags']).toarray()
similarity = cosine_similarity(vectors)
print(f"✓ Model ready! Similarity matrix: {similarity.shape}")

print("="*60 + "\n")

# Request model
class UserInput(BaseModel):
    animeName: str
    genre: str

def get_recommendations(anime_name, genre_input):
    """Get anime recommendations"""
    
    print("\n" + "="*60)
    print(f"🔍 SEARCH REQUEST")
    print("="*60)
    print(f"Anime Name: '{anime_name}'")
    print(f"Genre Filter: '{genre_input}'")
    print("-"*60)
    
    # Prepare genre list
    genre_list = [g.strip().lower() for g in genre_input.split(",")] if genre_input else []
    
    # Search for anime (case-insensitive)
    print(f"Searching in {len(animes)} anime...")
    matching_animes = animes[animes['title'].str.lower() == anime_name.lower()]
    
    if matching_animes.empty:
        print("❌ No exact match found")
        print("🔍 Trying partial match...")
        matching_animes = animes[animes['title'].str.lower().str.contains(anime_name.lower(), na=False)]
        
        if matching_animes.empty:
            print(f"❌ No matches found for '{anime_name}'")
            print("\n💡 Did you mean one of these?")
            # Try first word
            first_word = anime_name.split()[0].lower()
            suggestions = animes[animes['title'].str.lower().str.contains(first_word, na=False)]
            for i, title in enumerate(suggestions['title'].head(10), 1):
                print(f"   {i}. {title}")
            print("="*60)
            return []
        else:
            print(f"✓ Found {len(matching_animes)} partial matches")
            for i, title in enumerate(matching_animes['title'].head(5), 1):
                print(f"   {i}. {title}")
            selected_anime = matching_animes.iloc[0]['title']
            print(f"\n✓ Using: '{selected_anime}'")
            index = matching_animes.index[0]
    else:
        selected_anime = matching_animes.iloc[0]['title']
        index = matching_animes.index[0]
        print(f"✓ Exact match found: '{selected_anime}'")
        print(f"   Index: {index}")
        print(f"   ID: {matching_animes.iloc[0]['anime_id']}")
    
    # Get similarity scores
    print(f"\n🎯 Finding similar anime...")
    similarity_scores = list(enumerate(similarity[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = [score for score in similarity_scores if score[0] != index]
    
    print(f"✓ Found {len(similarity_scores)} similar anime")
    
    # Get top candidates
    top_indices = [i[0] for i in similarity_scores[:50]]
    recommended = animes.iloc[top_indices][['anime_id', 'title', 'genres', 'main_picture']].copy()
    
    # Filter by genre
    if genre_list:
        print(f"\n🎭 Filtering by genre(s): {genre_list}")
        recommended = recommended[recommended['genres'].str.lower().apply(
            lambda g: any(genre in str(g).lower() for genre in genre_list)
        )]
        print(f"✓ {len(recommended)} anime match the genre")
    
    # Get final recommendations
    result = recommended.head(10).to_dict('records')
    
    print(f"\n✅ Returning {len(result)} recommendations")
    if result:
        print("\nTop 3 recommendations:")
        for i, rec in enumerate(result[:3], 1):
            print(f"   {i}. {rec['title']}")
    
    print("="*60 + "\n")
    return result

@app.post("/recommend")
def recommend(user: UserInput):
    """Recommendation endpoint"""
    try:
        recommendations = get_recommendations(user.animeName, user.genre)
        
        if not recommendations:
            return {
                "success": False,
                "message": f"No anime found matching '{user.animeName}'. Please check spelling or try another anime.",
                "recommendations": []
            }
        
        return {
            "success": True,
            "message": f"Found {len(recommendations)} recommendations!",
            "recommendations": recommendations
        }
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "recommendations": []
        }

@app.get("/test/images")
def test_images():
    """Test endpoint to check image data"""
    sample = animes.head(5)[['anime_id', 'title', 'main_picture']].to_dict('records')
    return {"sample_data": sample}

@app.get("/search/{query}")
def search_anime(query: str):
    """Search endpoint"""
    matches = animes[animes['title'].str.lower().str.contains(query.lower(), na=False)]
    results = matches.head(20)[['anime_id', 'title']].to_dict('records')
    return {"results": results}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve HTML"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found</h1>")

@app.get("/health")
def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "anime_count": len(animes),
        "model_ready": True
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting server...")
    print("🌐 Open: http://127.0.0.1:8000/")
    print("📝 Press CTRL+C to stop\n")
    uvicorn.run(app, host="127.0.0.1", port=8000)