# 🌱 Soil Quality Analysis System

A comprehensive AI-powered soil quality analysis application that provides real-time soil health assessment, expert recommendations, and multilingual support for farmers and agricultural professionals.

## 🚀 Features

### 🔬 **Advanced Soil Analysis**
- **Machine Learning Classification**: Uses XGBoost model to classify soil fertility into three categories:
  - Less Fertile
  - Fertile  
  - Highly Fertile
- **12 Key Soil Parameters**: Analyzes essential soil health indicators including:
  - Nitrogen (N), Phosphorous (P), Potassium (K)
  - pH levels and electrical conductivity
  - Organic carbon content
  - Micronutrients (Sulfur, Zinc, Iron, Copper, Manganese, Boron)

### 🤖 **AI-Powered Expert Chat**
- **Intelligent Recommendations**: Get personalized advice based on your soil analysis
- **Interactive Q&A**: Ask specific questions about nutrient levels, pH balance, and fertilizer recommendations
- **Context-Aware Responses**: Chat maintains conversation history for better assistance
- **Quick Action Buttons**: One-click access to common questions about nutrient improvement and fertilizer guidance

### 🌍 **Multilingual Support**
- **English & Japanese**: Full application support in both languages
- **Dynamic Language Switching**: Change language on-the-fly without losing data
- **Localized Expert Advice**: AI responses adapt to selected language

### 📊 **Real-Time Data Visualization**
- **Live Sensor Data**: Simulated real-time soil sensor readings
- **Multiple Sample Analysis**: Compare different soil samples simultaneously
- **Interactive Dashboard**: Clean, modern interface with responsive design
- **Visual Status Indicators**: Color-coded fertility status with clear visual feedback

### 🎨 **Modern User Interface**
- **Streamlit-Powered**: Fast, responsive web application
- **Dark Theme**: Professional dark background with white content containers
- **Mobile-Friendly**: Responsive design that works on all devices
- **Intuitive Navigation**: Easy-to-use interface with clear visual hierarchy

## 🛠️ Technology Stack

### **Backend**
- **Python 3.10+**: Core programming language
- **XGBoost**: Machine learning model for soil classification
- **LangChain**: AI framework for natural language processing
- **Groq API**: High-performance LLM inference

### **Frontend**
- **Streamlit**: Web application framework
- **Custom CSS**: Modern styling and responsive design
- **Real-time Updates**: Dynamic content updates without page refresh

### **Data Processing**
- **Pandas & NumPy**: Data manipulation and numerical computing
- **JSON**: Sensor data storage and processing
- **Scikit-learn**: Additional ML utilities

## 📋 Prerequisites

- Python 3.10 or higher
- Groq API key (for AI chat functionality)
- Git (for cloning the repository)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/soil-quality-analysis.git
   cd soil-quality-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r require.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### **Getting Started**
1. **Load Sensor Data**: Click "Load New Samples" to get fresh soil sensor readings
2. **Analyze Soil**: Select a soil sample and click "Analyze" to get AI-powered assessment
3. **Review Results**: View the fertility classification and detailed analysis
4. **Get Expert Advice**: Use the chat interface to ask specific questions about your soil

### **Understanding Results**
- **🔴 Less Fertile**: Soil needs significant improvement
- **🟡 Fertile**: Good soil with room for optimization  
- **🟢 Highly Fertile**: Excellent soil condition

### **Chat Features**
- **Quick Questions**: Use preset buttons for common inquiries
- **Custom Questions**: Type specific questions about your soil analysis
- **Language Support**: Switch between English and Japanese anytime

## 📁 Project Structure

```
soil-quality-analysis/
├── app.py                 # Main Streamlit application
├── soil.py               # ML model and LangChain setup
├── infer.py              # Data processing and inference
├── xgb_soil_analysis.bin # Trained XGBoost model
├── require.txt           # Python dependencies
├── assets/
│   └── sensor_data.json  # Sample sensor data
├── dataset1.csv          # Training dataset
└── Soil_Analysis_ML.ipynb # Model training notebook
```

## 🔧 Configuration

### **Environment Variables**
- `GROQ_API_KEY`: Required for AI chat functionality

### **Model Files**
- `xgb_soil_analysis.bin`: Pre-trained XGBoost model for soil classification
- `assets/sensor_data.json`: Sample sensor data for testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- XGBoost team for the excellent machine learning framework
- Streamlit team for the amazing web app framework
- LangChain community for AI integration tools
- Groq for high-performance LLM inference

## 📞 Support

For support, email your-email@example.com or create an issue in this repository.

---

**Made with ❤️ for sustainable agriculture**
