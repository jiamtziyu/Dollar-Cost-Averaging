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
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
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

    for index, row in data.iterrows():
        date = row['Date']
        price = row['Close']
        price_bought_at = 0
        num_shares_bought = 0
        investing_amount = 0
        fees_incurred = 0

        # Increasing cash balance from pay check
        if index % 20 == 0 and index != 0:
            cash_balance += investment
            original_cash += investment

        # Decrease cash balance to invest
        if index % get_interval_mapping(interval) == 0 and cash_balance != 0:
            investing_amount = investment / \
                (20 / get_interval_mapping(interval))
            num_shares_rough = investing_amount / price
            fees_incurred = max(comm_min_per_order + platform_fee_min_per_order, min(max(num_shares_rough * (comm_per_share + platform_fee_per_share), comm_min_per_order +
                                                                                         platform_fee_min_per_order), (investing_amount) * (comm_max_per_order/100 + platform_fee_max_per_order/100)))
            cash_balance -= investing_amount
            invested_amount += investing_amount
            investing_amount -= fees_incurred
            num_shares += investing_amount / price
            price_bought_at = price
            num_shares_bought = investing_amount / price

        total = cash_balance + num_shares * price

        try:
            t_c = total / original_cash
        except ZeroDivisionError:
            t_c = 1

        performance_data.append((date, price_bought_at, num_shares_bought, fees_incurred, original_cash, cash_balance, invested_amount, num_shares * price, total,
                                t_c))

    performance_data = pd.DataFrame(performance_data, columns=['Date', 'Price Bought', 'Shares Bought', 'Fees Paid', 'Total Cash', 'Cash Balance', 'Total Invested',
                                                               'Investment Value', 'Portfolio Value', 'Portfolio/Cash'])

    performance_data['Performance'] = performance_data['Portfolio/Cash'] - 1

    return performance_data


def compare_interval(intervals, input_data, investment, comm_per_share, comm_min_per_order, comm_max_per_order, platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order):

    # Initialize an empty DataFrame to store the merged results
    result_df = pd.DataFrame()

    for interval in intervals:
        data = dollar_cost_average_strategy(input_data, interval, investment, comm_per_share, comm_min_per_order, comm_max_per_order,
                                            platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order)
        filtered_data = data[["Date", "Performance"]]

        # Rename columns to avoid overwriting during merges
        filtered_data = filtered_data.rename(columns={
            "Performance": f"{interval}"
        })

        # Merge `filtered_data` with `result_df` on "Date" column
        if result_df.empty:
            # First interval, initialize `result_df` with `filtered_data`
            result_df = filtered_data
        else:
            # Merge with existing data on "Date"
            result_df = pd.merge(result_df, filtered_data,
                                 on="Date", how="outer")

    # Sort the final result by Date, if necessary
    result_df = result_df.sort_values(by="Date").reset_index(drop=True)

    return result_df
