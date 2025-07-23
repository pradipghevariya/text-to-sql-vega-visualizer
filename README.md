# 🧠 Text-to-SQL Visualizer with LangChain, Gemini, and Vega-Lite

A plug-and-play **Streamlit** app that enables **LLMs** to generate **Vega-Lite charts** from structured data. Perfect for enhancing **Text-to-SQL pipelines** with chart-based visual insights!

---

## 🔥 Features

* ✅ Uses **LangChain + Google Gemini** to generate valid Vega JSON specs
* ✅ Automatically parses **DataFrame schema and sample data**
* ✅ Clean and simple **Streamlit interface** (for demo purposes)
* ✅ Instantly renders chart using **Vega-Lite**

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/pradipghevariya/text-to-sql-vega-visualizer.git
cd text-to-sql-vega-visualizer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your Google Gemini API Key

```bash
export GOOGLE_API_KEY=your-api-key-here
```

> 💡 You can also use `.env` file to manage secrets securely.

### 4. Run the App

```bash
streamlit run app.py
```

---

## 📝 Notes

* The **user question**, **SQL output**, and **sample data** are **hardcoded** for demonstration purposes.
* Just click the **"Generate"** button to test how the system translates query into a chart.
* This setup is ideal for prototyping or integrating into a larger **Text-to-SQL** or **LLM-powered BI** tool.
