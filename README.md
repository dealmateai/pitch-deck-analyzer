# 🚀 Pitch Deck Analyzer


# 🚀 Pitch Deck Analyzer API

An AI tool that reads your startup pitch deck and gives you two scores:
- **Company Fit Score** (0-100%)
- **Founder Fit Score** (0-100%)


## 🎯 What It Does

Upload a PDF pitch deck → Get fit scores


Input: Your pitch deck PDF
↓
Analyzes company details (problem, solution, market, traction)
↓
Analyzes founder details (names, experience, education)
↓
Output: Two percentage scores + recommendations


## 🚀 Quick Start (5 Minutes)

### 1. Install
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
.\venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Prepare Data + Train Models
```bash
python train.py
```

This command now:
- Builds `data/datasets/training_dataset.csv`
- Trains company and founder models
- Saves artifacts in `models/`:
   - `company_fit_model.pkl`
   - `founder_fit_model.pkl`
   - `scaler_company.pkl`
   - `scaler_founder.pkl`
   - `feature_names.pkl`

### 3. Start API
```bash
python api_server.py
```

Then open: **http://localhost:8000/docs**

---

## 📮 How to Use

### Option 1: Postman (Easiest)

1. Create test PDF:
```bash
python create_test_pdf.py
```

2. In Postman:
   - Method: **POST**
   - URL: `http://localhost:8000/analyze`
   - Body: Select "form-data"
   - Key: "file" (Type: File)
   - Value: Select `test_pitch_deck.pdf`
   - Click **Send**

### Option 2: Python
```python
import requests

with open("pitch_deck.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/analyze", files=files)
    result = response.json()
    
print(f"Company Fit: {result['company_fit']}%")
print(f"Founder Fit: {result['founder_fit']}%")
```

---

## 📊 Sample Response

```json
{
    "company_fit": 82.5,
    "founder_fit": 88.3,
    "overall_score": 84.1,
    "company_extracted": {
        "name": "TechAI Analytics",
        "industry": "AI/ML",
        "problem": "Analytics tools are expensive...",
        "market_size": "$50 billion",
        "traction": "50K users, $500K revenue"
    },
    "founder_extracted": {
        "names": ["Sarah Chen", "John Smith"],
        "count": 2,
        "experience_level": "Highly Experienced",
        "education": "Stanford PhD"
    },
    "recommendations": [
        "🎯 Strong pitch! Ready for investors",
        "📈 Include growth metrics"
    ]
}
```

---

## 📁 Folder Structure

```
pitch-deck-analyzer/
├── api/               # FastAPI application
├── nlp/               # Text analysis
├── data/datasets/     # Training data
├── models/            # Trained AI models
├── config.py          # Settings
├── requirements.txt   # Dependencies
├── train.py          # Build dataset + train/save models
└── api_server.py     # Start the API
```

---

## 🔧 What You Need

- Python 3.8+
- pip
- Postman (optional, for testing)

---

## ⚙️ Step by Step Installation

### Step 1: Setup
```bash
git clone <your-repo>
cd pitch-deck-analyzer
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### Step 2: Install Libraries
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 3: Create Training Data + Model Artifacts
```bash
python train.py
# Builds dataset and saves all model files under models/
```

### Step 4: Start API
```bash
python api_server.py
# API runs on http://localhost:8000
```

### Step 6: Test It
```bash
python create_test_pdf.py
python test_api.py
```



## 📝 What the Scores Mean

### Company Fit Score
| Score | Meaning |
|-------|---------|
| 0-30% | Needs work |
| 31-60% | Average |
| 61-80% | Good |
| 81-100% | Excellent |

### Founder Fit Score
| Score | Meaning |
|-------|---------|
| 0-30% | Weak team |
| 31-60% | Average team |
| 61-80% | Strong team |
| 81-100% | Excellent team |



## 🚨 Troubleshooting

### API won't start?
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall everything
pip install -r requirements.txt --upgrade
```

### Getting "Failed to analyze" error?
```bash
# Create test PDF first
python create_test_pdf.py

# Run diagnostic
python -c "from nlp.pdf_extractor import PDFExtractor; print('OK')"
```

### Slow response?
- First request takes 15-20 seconds (loading AI models)
- Next requests are 8-12 seconds


## 📊 Training Data

The system comes with **100 example companies**:
- **50 Positive**: Real Y Combinator companies (Airbnb, Stripe, etc.)
- **50 Negative**: Typical non-funded startups

To use your own data, edit `scraper/synthetic_data_generator.py`



## 🔑 Key Files

| File | Purpose |
|------|---------|
| `api_server.py` | Start the API |
| `train.py` | Build dataset, train models, and save artifacts |
| `config.py` | Settings |
| `create_test_pdf.py` | Make test PDF |
| `test_api.py` | Test the API |



## 📦 What It Uses

- **FastAPI** - Web server
- **pdfplumber** - Read PDFs
- **spaCy** - Understand text
- **XGBoost** - AI predictions
- **pandas** - Data handling


## 🎯 How It Works

```
1. You upload PDF
   ↓
2. Extract text from PDF
   ↓
3. Find company info (name, industry, market size, etc.)
   ↓
4. Find founder info (names, experience, education)
   ↓
5. AI model rates both
   ↓
6. Return two scores + feedback
```



## 💡 Example Usage

### Upload a pitch deck
```bash
curl -F "file=@pitch_deck.pdf" http://localhost:8000/analyze


### Check if API is running
```bash
curl http://localhost:8000/health
```

### View documentation
Open in browser: `http://localhost:8000/docs`


## ⚡ Performance

| Metric | Time |
|--------|------|
| First request | 20-25 sec |
| Later requests | 8-12 sec |
| Max file size | 50 MB |
| Max pages | 100 |



## 📝 API Endpoints

| Endpoint | What It Does |
|----------|-------------|
| `POST /analyze` | Upload PDF & get scores |
| `GET /health` | Check if API is running |
| `GET /docs` | See all endpoints |



## 🐛 Common Issues

**Q: PDF won't upload?**
A: Make sure it's a .pdf file, not .docx or .txt

**Q: Getting error in terminal?**
A: Scroll up to see the actual error message

**Q: API too slow?**
A: First run loads AI models (slow), others are faster

**Q: Can I use with my own data?**
A: Yes! Edit `scraper/synthetic_data_generator.py` and retrain



## 📞 Need Help?

1. Check the troubleshooting section above
2. Look at API terminal for error messages
3. Run `python test_api.py` to test everything



## 📄 License

MIT - Use freely, modify as needed



## 🎉 You're Ready!

```bash
python api_server.py
# Open http://localhost:8000/docs
# Upload your pitch deck
# Get your scores!
```

**That's it! Happy analyzing! 🚀**
```
