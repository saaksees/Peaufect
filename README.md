# ✨ PEAUFECT: From Questions to Glow

**Peaufect knows!!** Your AI-powered skincare companion for personalized beauty solutions.

## 🌟 Features

- **Personalized Skincare Advice**: Get tailored recommendations based on your skin type, concerns, and budget
- **Budget-Friendly Options**: Filter recommendations by Indian Rupee budget ranges (₹0-₹1,500, ₹1,500-₹4,000, ₹4,000+)
- **Dynamic Brand Selection**: Brands automatically filter based on your budget preference
- **Interactive UI**: Beautiful, modern interface with animations and visual elements
- **Smart Validation**: Only accepts skincare-related queries
- **Bullet Point Responses**: Clear, actionable advice in easy-to-read format

## 🎯 Skin Types Supported

- **Oily Skin**: Oil-control and pore-minimizing solutions
- **Dry Skin**: Hydrating and nourishing recommendations  
- **Combination Skin**: Balanced approach for mixed skin needs

## 💰 Budget Categories

- **Low Budget**: ₹0-₹1,500 (Himalaya, Biotique, Garnier, etc.)
- **Mid Budget**: ₹1,500-₹4,000 (Minimalist, Dot&Key, The Ordinary, etc.)
- **High Budget**: ₹4,000+ (Clinique, Forest Essentials, SK-II, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/peaufect-skincare-ai.git
   cd peaufect-skincare-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv skinenv
   source skinenv/bin/activate  # On Windows: skinenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
peaufect-skincare-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/                 # Skincare knowledge base (CSV files)
├── utils/
│   ├── loader.py         # Data loading utilities
│   └── vectorstore.py    # Vector database setup
├── models/
│   └── llm.py           # Language model configuration
└── README.md            # Project documentation
```

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: LLM orchestration and RAG implementation
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings
- **Groq**: Fast LLM inference

## 🌈 Key Features

### Smart Skincare Validation
- Only processes skincare-related queries
- Politely redirects off-topic questions
- Comprehensive keyword detection

### Personalized Recommendations
- Considers skin type, age, budget, and concerns
- Dynamic brand filtering based on budget
- Contextual product suggestions

### Beautiful UI/UX
- Gradient animations and modern design
- Interactive skin concern selection
- Quick tips for each skin type
- Categorized suggestion tabs

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

PEAUFECT provides general skincare guidance only. Always consult with a dermatologist for serious skin concerns or before starting new skincare treatments.

## 🌟 Live Demo

Try PEAUFECT live: [Streamlit Cloud Link](https://your-app-link.streamlit.app)

---

**Made with ❤️ for healthier, happier skin**

*Personalized • Science-Based • Budget-Friendly • Natural*