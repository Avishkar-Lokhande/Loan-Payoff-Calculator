# 💰 Loan Payoff Calculator

A comprehensive Streamlit web application for analyzing loan amortization schedules and exploring prepayment strategies.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Features

- **Loan Amortization Calculator** - Generate detailed month-by-month payment schedules
- **Prepayment Analysis** - See how extra payments affect your loan
- **Interactive Visualizations** - Beautiful Plotly charts for better understanding
- **What-If Scenarios** - Compare multiple prepayment strategies
- **CSV Export** - Download your amortization schedule
- **Target Payoff Calculator** - Find out how much extra to pay to reach your goal

## 📸 Screenshots

*Coming soon!*

## 🚀 Installation

1. Clone or download this project:
```bash
git clone https://github.com/yourusername/loan-payoff-calculator.git
cd loan-payoff-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
loan_payoff_calculator/
├── app.py              # Main Streamlit application
├── calculations.py     # Loan calculation functions
├── visualizations.py   # Plotly chart functions
├── utils.py           # Helper utilities
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🧮 How It Works

### Monthly Payment Formula

The app uses the standard amortization formula:

```
PMT = P × [r(1+r)^n] / [(1+r)^n - 1]
```

Where:
- P = Principal (loan amount)
- r = Monthly interest rate
- n = Number of payments

### Interest Calculation

For each month:
- Interest = Remaining Balance × (Annual Rate / 12)
- Principal Payment = Monthly Payment - Interest
- New Balance = Previous Balance - Principal Payment

### Prepayment Benefits

Extra payments go directly toward principal, which:
- Reduces total interest paid
- Shortens your loan term
- Builds equity faster

## 🛠️ Tech Stack

- **Python 3.9+** - Programming language
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **NumPy Financial** - Financial calculations
- **Plotly** - Interactive charts

## 📊 App Tabs

1. **Summary** - Quick comparison of base vs prepayment scenarios
2. **Amortization Schedule** - Full month-by-month breakdown
3. **Visualizations** - Charts showing balance, interest, and savings
4. **What-If Scenarios** - Explore different extra payment amounts
5. **Methodology** - Learn about the formulas used

## 💡 Tips for Users

- Even $50-$100 extra per month can save thousands in interest
- Making one extra payment per year (13 payments) can cut years off your loan
- The earlier you start making extra payments, the more you save

## 🔮 Future Enhancements

- [ ] Bi-weekly payment options
- [ ] Multiple loan comparison
- [ ] PDF report generation
- [ ] Loan refinancing calculator
- [ ] Historical interest rate data
- [ ] Mobile-responsive design improvements

## ⚠️ Disclaimer

This calculator provides estimates for educational purposes only. Actual loan terms may vary. Always consult with your lender or a financial advisor for exact figures.

## 📄 License

MIT License - feel free to use this project for learning or building your own tools!

---

Made with ❤️ using Streamlit
