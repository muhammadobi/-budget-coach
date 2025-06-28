# 💰 Budget Coach - Personal Financial Literacy App

A simple, educational budgeting application built with Streamlit that helps users track their finances, visualize spending patterns, and learn fundamental financial concepts.

## 🎯 Features

### Core Functionality
- **Transaction Logging**: Easy income and expense tracking with categorization
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Financial Advice**: Personalized budgeting recommendations based on the 50/30/20 rule
- **Educational Content**: Rotating financial tips and micro-lessons
- **Data Management**: CSV import/export for data backup and migration

### Educational Focus
- 50/30/20 budgeting rule analysis
- Emergency fund guidance
- Compound interest education
- Net worth tracking concepts
- Smart spending habits

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd budget-coach
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   Open your browser and go to `http://localhost:8501`

## 📱 How to Use

### 1. Dashboard
- View your monthly income, expenses, and net savings
- See spending breakdown by category
- Track monthly trends
- Review recent transactions

### 2. Add Transactions
- Log income and expenses with detailed categorization
- Use quick-add buttons for common transactions
- Specify dates, amounts, and descriptions

### 3. Analytics
- Get personalized financial advice
- Analyze spending against the 50/30/20 rule
- View detailed spending patterns
- Track daily spending trends

### 4. Financial Tips
- Learn about budgeting concepts
- Understand compound interest
- Build an emergency fund
- Develop healthy financial habits

### 5. Settings
- Export your data to CSV
- Import transactions from CSV files
- Manage and delete transactions
- View app information

## 🏗️ Project Structure

```
budget-coach/
├── app.py                 # Main Streamlit application
├── database.py           # SQLite database operations
├── financial_advisor.py  # Financial advice and education logic
├── visualizations.py     # Plotly chart creation
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── budget_coach.db      # SQLite database (created on first run)
```

## 🧱 Technical Stack

- **Backend**: Python 3.11+, SQLite, Pandas
- **Frontend**: Streamlit with custom CSS styling
- **Visualizations**: Plotly Express and Plotly Graph Objects
- **Data Storage**: SQLite for lightweight, local storage
- **File Handling**: CSV import/export capabilities

## 💡 Key Features Explained

### 50/30/20 Rule Analysis
The app automatically categorizes your spending and provides visual feedback on how well you're following the 50/30/20 budgeting rule:
- 50% for needs (housing, utilities, groceries)
- 30% for wants (entertainment, dining out)
- 20% for savings and debt payment

### Educational Components
- Rotating financial tips with actionable advice
- Interactive gauges showing budget compliance
- Clear explanations of financial concepts
- Goal-setting guidance for emergency funds and retirement

### Data Management
- Automatic SQLite database creation and management
- CSV export for data backup
- CSV import for migrating existing financial data
- Transaction editing and deletion capabilities

## 🎨 Customization

### Adding New Categories
The app comes with predefined income and expense categories, but you can modify them in the `database.py` file by updating the default categories lists.

### Styling
Custom CSS is included in `app.py` for enhanced visual appeal. You can modify the styling by updating the CSS in the `st.markdown()` section.

### Educational Content
Add new financial tips and educational content by modifying the `financial_tips` list in `financial_advisor.py`.

## 🔒 Privacy & Security

- All data is stored locally in an SQLite database
- No personal information is transmitted over the internet
- Data export capabilities ensure you maintain control of your financial information
- The app runs entirely on your local machine

## 🤝 Contributing

This project is designed to be educational and easily extensible. Feel free to:
- Add new visualization types
- Enhance the financial advice algorithms
- Improve the user interface
- Add new educational content

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check that all dependencies are properly installed
2. Ensure you're using Python 3.11 or higher
3. Verify that the SQLite database has proper permissions
4. Check the terminal for any error messages

## 🎓 Educational Goals

Budget Coach is designed to help users:
- Develop consistent money tracking habits
- Understand fundamental budgeting principles
- Learn about long-term financial planning
- Build confidence in personal finance management
- Make informed financial decisions

---

**Happy Budgeting! 💰** 