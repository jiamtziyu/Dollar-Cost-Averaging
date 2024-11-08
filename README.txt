# Dollar Cost Averaging Analysis

## Description
Dollar Cost Averaging Analysis is a tool designed to explore how the interval of dollar cost averaging (DCA) impacts investment returns. While conventional DCA strategies suggest monthly investing, this project investigates why this interval is recommended and examines the influence of trading fees on overall returns.

## Features
- Access historical datasets for specific stock tickers.
- Analyze the performance of a standard dollar-cost averaging (DCA) strategy.
- Compare relative performance of different DCA intervals (e.g., weekly, monthly, quarterly).
- Factor in brokerage fees to understand their impact on returns.

## Installation
1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/DollarCostAveragingAnalysis.git
   ```

2. **Navigate to the project directory**  
   ```bash
   cd DollarCostAveragingAnalysis
   ```

3. **Install required packages**  
   Use the following command to install dependencies from `requirements.txt`, which includes essential libraries like `yahoofinance`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
After installing the required packages, you can launch the tool by running the following command:

```bash
streamlit run main.py
```

This will start a Streamlit web app where you can:
- Select stock tickers for analysis,
- Set different DCA intervals for comparison,
- Adjust brokerage fees to see their impact on returns.

Navigate to the provided local URL in your browser to interact with the tool.

## Contributing
Contributions are welcome! If you'd like to improve this project or add new features, please follow these steps:

1. **Fork the repository** to your GitHub account.
2. **Create a new branch** for your feature or bug fix.
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes** with a clear and descriptive message.
   ```bash
   git commit -m "Add AmazingFeature to improve performance analysis"
   ```
4. **Push to the branch**.
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request** in the original repository, describing your changes and why they should be merged.

Feel free to open issues for any suggestions or bugs, and we’ll review them!

## Acknowledgments
- Design inspiration from [TipRanks' Dollar Cost Averaging Tool](https://www.tipranks.com/personal-finance/investing-and-retirement/dollar-cost-averaging?ticker=AAPL&startYear=2018&startMonth=12&endMonth=12&endYear=2024&monthlyInvestment=100&initialInvestment=1000&multipleRecurringInvestment=1&multipleRecurringInvestmentOnChange=0.01&period=month).
- Tutorial guidance from [Pixegami's YouTube video on Streamlit](https://www.youtube.com/watch?v=D0D4Pa22iG0&t=71s&ab_channel=pixegami), titled *"Streamlit: The Fastest Way To Build Python Apps?"*.
