# 🎬 Anime Recommendation System

A beautiful, modern web application that recommends anime based on user preferences using machine learning.

## ✨ Features

- 🎯 **Smart Recommendations** - Content-based filtering using TF-IDF and cosine similarity
- 🖼️ **Anime Images** - Beautiful card layout with anime posters
- 🎨 **Modern UI** - Dark cyberpunk theme with smooth animations
- 🔍 **Intelligent Search** - Partial matching and suggestions
- 📱 **Responsive Design** - Works on all devices
- ⚡ **Fast Performance** - Optimized similarity computations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning (TF-IDF, Cosine Similarity)
- **NLTK** - Natural language processing (stemming)

### Frontend
- **HTML5/CSS3** - Modern web standards
- **JavaScript (ES6)** - Interactive functionality
- **Fetch API** - Asynchronous data fetching

## 📁 Project Structure

```
anime-recommendation-system/
├── app.py              # FastAPI backend server
├── index.html          # Frontend interface
├── anime.csv           # Dataset (24,985 anime entries)
├── check_images.py     # Image data verification script
├── verify_app.py       # Code verification script
└── README.md           # This file
```

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pandas scikit-learn nltk
```

### 2. Download NLTK Data

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 💻 Usage

### Start the Server

```bash
python app.py
```

The server will start at: `http://127.0.0.1:8000/`

### Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

### Make a Search

1. Enter an anime name (e.g., "Steins;Gate", "Death Note")
2. Select a preferred genre
3. Click "Get Recommendations"
4. View your personalized recommendations!

## 📊 Dataset Information

- **Total Anime:** 24,985 entries
- **With Images:** 24,831 (99.4%)
- **Columns Used:**
  - `anime_id` - Unique identifier
  - `title` - Anime name
  - `genres` - Genre tags
  - `themes` - Theme tags
  - `studios` - Production studios
  - `producers` - Producers
  - `main_picture` - Image URL

## 🔧 API Endpoints

### GET `/`
Serves the main HTML interface

### POST `/recommend`
Returns anime recommendations

**Request Body:**
```json
{
  "animeName": "Steins;Gate",
  "genre": "Sci-Fi"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Found 10 recommendations!",
  "recommendations": [
    {
      "anime_id": 9253,
      "title": "Steins;Gate",
      "genres": "['Sci-Fi', 'Thriller']",
      "main_picture": "https://cdn.myanimelist.net/..."
    }
  ]
}
```

### GET `/search/{query}`
Search anime by name (partial matching)

### GET `/test/images`
Test endpoint to verify image data

### GET `/health`
Health check endpoint

## 🧠 How It Works

1. **Data Preprocessing**
   - Combines genres, themes, studios, and producers into tags
   - Applies stemming using Porter Stemmer
   - Removes entries with empty tags

2. **Feature Extraction**
   - Uses CountVectorizer with 5000 max features
   - Creates TF-IDF vectors for each anime

3. **Similarity Computation**
   - Computes cosine similarity matrix (24,500 × 24,500)
   - Finds most similar anime based on content

4. **Recommendation Generation**
   - Searches for user's favorite anime
   - Retrieves top 50 similar anime
   - Filters by selected genre
   - Returns top 10 recommendations

## 🎨 UI Features

- **Dark Theme** - Cyberpunk-inspired gradient background
- **Glassmorphism** - Frosted glass effect on containers
- **Smooth Animations** - Fade-in, slide, and hover effects
- **Responsive Grid** - Auto-adjusting card layout
- **Image Fallback** - Shows emoji if image fails to load
- **Status Messages** - Success/error/info notifications

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### No Recommendations Found
- Check exact spelling of anime name
- Try the suggestions shown in terminal
- Verify anime exists in dataset using `check_images.py`

### Images Not Loading
- Run `check_images.py` to verify image URLs
- Check browser console for CORS errors
- Ensure `main_picture` column exists in dataset

## 📝 Sample Anime to Try

- Fullmetal Alchemist: Brotherhood
- Steins;Gate
- Hunter x Hunter (2011)
- Death Note
- Attack on Titan (Shingeki no Kyojin)
- One Punch Man
- Cowboy Bebop
- Code Geass
- Demon Slayer (Kimetsu no Yaiba)
- My Hero Academia

## 🔮 Future Enhancements

- [ ] User authentication and profiles
- [ ] Save favorite anime
- [ ] Rating system
- [ ] Advanced filters (year, studio, rating)
- [ ] Collaborative filtering
- [ ] Anime details modal
- [ ] Watch list functionality
- [ ] Social sharing features

## 📄 License

This project is for educational purposes.

## 🙏 Credits

- Dataset: MyAnimeList
- Images: MyAnimeList CDN
- Framework: FastAPI
- ML Library: Scikit-learn

---

**Made with ❤️ for anime lovers**