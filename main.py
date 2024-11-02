import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf
from functions import *

# Page title
st.title("Dollar Cost Averaging Tool")
st.divider()
# Input Parameters
st.write("### Input Parameters")

col1, col2, col3 = st.columns(3)

ticker = col1.text_input(
    label="Ticker",
    value="SPY",
    max_chars=5)

interval = col2.selectbox(
    label="Interval",
    options=("Weekly", "Monthly", "Quarterly", "Biannually")
)

investment = col3.number_input(
    label="Monthly Budget ($)",
    min_value=0,
    value=100,
    step=100
)

col1, col2 = st.columns(2)

month_start = col1.selectbox(
    label="Start Month",
    options=("January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"),
    index=0
)

# Get the current year
current_year = datetime.now().year

# Generate the list of years from 1990 to the current year
years = list(range(1990, current_year + 1))

# Create the selectbox with the list of years
year_start = col2.selectbox(
    label="Start Year",
    options=years,
    index=34
)

month_end = col1.selectbox(
    label="End Month",
    options=("January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"),
    index=11
)

# Create the selectbox with the list of years
year_end = col2.selectbox(
    label="End Year",
    options=years,
    index=34
)

st.divider()
# Input Parameters
st.write("### Brokerage Fee Structure")

col1, col2, col3 = st.columns(3)

comm_per_share = col1.number_input(
    label="Comm/Share ($)",
    min_value=0.000,
    value=0.005,
)

comm_min_per_order = col2.number_input(
    label="Min Comm/Order ($)",
    min_value=0.00,
    value=0.99
)

comm_max_per_order = col3.number_input(
    label="Max Comm/Order (%)",
    min_value=0.00,
    value=0.5,
    help="% Of Trade Value"
)

platform_fee_per_share = col1.number_input(
    label="Fee/Share ($)",
    min_value=0.000,
    value=0.005,
)

platform_fee_min_per_order = col2.number_input(
    label="Min Fee/Order ($)",
    min_value=0.00,
    value=1.00
)

platform_fee_max_per_order = col3.number_input(
    label="Max Fee/Order (%)",
    min_value=0.00,
    value=0.5,
    help="% Of Trade Value"
)

min_charges_per_trade = comm_min_per_order + comm_per_share + \
    platform_fee_min_per_order + platform_fee_per_share

st.markdown(
    f"The minimum fee for each trade is: **:blue[${min_charges_per_trade:,.2f}]**")
st.markdown(
    f"To breakeven for each trade, the take profit must be at least: **:red[${min_charges_per_trade*2:,.2f}]**")

st.write("##### Quick Calculation")

col1, col2 = st.columns(2)
test_num_share = col1.number_input(
    label="Num of Shares",
    min_value=0.00,
    value=1.00
)
test_share_value = col2.number_input(
    label="Price/Share",
    min_value=0.00,
    value=1.00
)
test_total_value = test_num_share * test_share_value
test_total_fee = min(max(test_num_share * (comm_per_share + platform_fee_per_share), comm_min_per_order + platform_fee_min_per_order), (test_total_value) * (comm_max_per_order/100 + platform_fee_max_per_order/100))

st.markdown(
    f"The total value for this trade is: **:blue[${test_total_value:,.2f}]**")
st.markdown(
    f"The total fee for this trade is: **:red[${test_total_fee:,.2f}]**")


st.divider()


# Chart
st.write(f"### Historical Price of ${ticker}")


start_date = str(year_start) + "-" + get_month_number(month_start) + "-01"
end_date = str(year_end) + "-" + get_month_number(month_end) + "-01"
historical_data = download_ticker_data(ticker, start_date, end_date)


close_price_data = historical_data[["Date", "Close"]]
close_price_data.set_index("Date", inplace=True)

st.line_chart(
    data=close_price_data,
    use_container_width=True
)
st.dataframe(
    data=historical_data,
    use_container_width=True,
    hide_index=True,
    height=150)

st.divider()

# Chart
st.write(f"### Visualization of {interval} DCA into ${ticker}")

dca_data = dollar_cost_average_strategy(historical_data, interval, investment, comm_per_share, comm_min_per_order,
                                        comm_max_per_order, platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order)

close_price_data = dca_data[["Date", "Original Cash", "Total"]]
close_price_data.set_index("Date", inplace=True)

st.line_chart(
    data=close_price_data,
    use_container_width=True,
    y=["Total", "Original Cash"]
)

st.divider()

# Chart
st.write(f"### Other Investment Data")

total_fees_paid = 5000

st.metric(
    label="Total Fees Paid",
    value=f"${total_fees_paid:,.2f}"
)

st.divider()

# TODO: compute dollar cost averaging strategy
# Chart
st.write(f"### ${ticker} DCA Table")

total_invested = 0
# for index, row in historical_data.iterrows():
#     pass

st.divider()

# Performance
st.write(f"### ${ticker} DCA Performance")

percentage_gain = 200
total_gain = 20000
final_portfolio_value = 40000

col1, col2 = st.columns(2)

col1.metric(
    label="Total Invested",
    value=f"${total_invested:,.0f}"
)
col2.metric(
    label="Percentage Gain",
    value=f"{percentage_gain:,.2f}%"
)
col1.metric(
    label="Total Gain",
    value=f"${total_gain:,.2f}"
)
col2.metric(
    label="Final Portfolio Value",
    value=f"${final_portfolio_value:,.2f}"
)

st.divider()
