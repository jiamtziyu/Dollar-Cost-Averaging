import yfinance as yf
import pandas as pd


def download_ticker_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)

    # Flatten MultiIndex columns (if applicable)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [f'{col[0]}' for col in data.columns.values]

    # Reset the index to move 'Date' from index to a column
    data = data.reset_index()

    # Convert the 'Date' column to just the date part
    data['Date'] = data['Date'].dt.date

    return data


def get_month_number(month_name):

    month_mapping = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    return month_mapping.get(month_name, "Invalid month name")


def get_interval_mapping(interval):

    interval_mapping = {
        "weekly": 5,
        "monthly": 20,
        "quarterly": 60,
        "biannually": 120
    }

    return interval_mapping.get(interval.lower(), "Invalid frequency")


def dollar_cost_average_strategy(data, interval, investment, comm_per_share, comm_min_per_order, comm_max_per_order, platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order):

    invested_amount = 0.0
    cash_balance = 0.0
    num_shares = 0.0
    original_cash = 0.0
    performance_data = []

    for index, data in data[0:].iterrows():
        date = data['Date']
        price = data['Close']
        price_bought_at = 0
        num_shares_bought = 0
        investing_amount = 0

        # Increasing cash balance from pay check
        if index % 20 == 0 and index != 0:
            cash_balance += investment
            original_cash += investment

        # Decrease cash balance to invest
        if index % get_interval_mapping(interval) == 0 and cash_balance != 0:
            investing_amount = investment / \
                (20 / get_interval_mapping(interval))
            fees_incurred = 0
            cash_balance -= investing_amount
            invested_amount += investing_amount - fees_incurred
            investing_amount -= fees_incurred
            num_shares += investing_amount / price
            price_bought_at = price
            num_shares_bought = investing_amount / price

        total = cash_balance + num_shares * price

        try:
            t_c = total / original_cash
        except ZeroDivisionError:
            t_c = 1

        performance_data.append((date, price_bought_at, original_cash, cash_balance, invested_amount, num_shares * price, total,
                                t_c, investing_amount, num_shares_bought))

    performance_data = pd.DataFrame(performance_data, columns=['Date', 'Price Bought At', 'Total Invested', 'Cash Balance', 'Capital',
                                                               'Investment', 'Total', 'Total/Cash', 'Investing Amount',
                                                               'Num Shares Bought'])

    performance_data['Performance'] = performance_data['Total/Cash'] - 1

    print("Basic DCA Strategy completed.")

    return performance_data
