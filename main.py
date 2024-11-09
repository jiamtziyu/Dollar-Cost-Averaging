import streamlit as st
import pandas as pd
from datetime import datetime
import yfinance as yf
from functions import *


with st.sidebar:
    st.write("#### Input Parameters")

    ticker = st.text_input(
        label="Ticker",
        value="SPY",
        max_chars=5)
    interval = st.selectbox(
        label="Interval",
        options=("Weekly", "Monthly", "Quarterly", "Biannually"))
    investment = st.number_input(
        label="Monthly Budget ($)",
        min_value=0,
        value=100,
        step=100)
    month_start = st.selectbox(
        label="Start Month",
        options=("January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"),
        index=0)
    # Get the current year
    current_year = datetime.now().year

    # Generate the list of years from 1990 to the current year
    years = list(range(1990, current_year + 1))

    # Create the selectbox with the list of years
    year_start = st.selectbox(
        label="Start Year",
        options=years,
        index=34)

    month_end = st.selectbox(
        label="End Month",
        options=("January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"),
        index=11)

    # Create the selectbox with the list of years
    year_end = st.selectbox(
        label="End Year",
        options=years,
        index=34)

    st.divider()
    st.write("#### Brokerage Fee Structure")

    comm_per_share = st.number_input(
        label="Comm/Share ($)",
        min_value=0.000,
        value=0.005,
    )

    comm_min_per_order = st.number_input(
        label="Min Comm/Order ($)",
        min_value=0.00,
        value=0.99
    )

    comm_max_per_order = st.number_input(
        label="Max Comm/Order (%)",
        min_value=0.00,
        value=0.5,
        help="% Of Trade Value"
    )

    platform_fee_per_share = st.number_input(
        label="Fee/Share ($)",
        min_value=0.000,
        value=0.005,
    )

    platform_fee_min_per_order = st.number_input(
        label="Min Fee/Order ($)",
        min_value=0.00,
        value=1.00
    )

    platform_fee_max_per_order = st.number_input(
        label="Max Fee/Order (%)",
        min_value=0.00,
        value=0.5,
        help="% Of Trade Value"
    )

    min_charges_per_trade = comm_min_per_order + comm_per_share + \
        platform_fee_min_per_order + platform_fee_per_share

    st.markdown(
        f"The minimum fee for each trade is: **:blue[${min_charges_per_trade:,.2f}]**. To breakeven, the take profit must be at least: **:red[${min_charges_per_trade*2:,.2f}]**")


# Page title
st.title("Dollar Cost Averaging Tool")

# Chart
start_date = str(year_start) + "-" + str(get_month_number(month_start)) + "-01"
end_date = str(year_end) + "-" + str(get_month_number(month_end)) + "-01"
historical_data = download_ticker_data(ticker, start_date, end_date)
dca_data = dollar_cost_average_strategy(historical_data, interval, investment, comm_per_share, comm_min_per_order,
                                        comm_max_per_order, platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order)

total_invested = dca_data['Total Invested'].iloc[-1]
percentage_gain = dca_data['Portfolio/Cash'].iloc[-1] - 1
final_portfolio_value = dca_data['Portfolio Value'].iloc[-1]
total_gain = final_portfolio_value - dca_data['Total Cash'].iloc[-1]
total_period = (year_end - year_start) * 12 + \
    (get_month_number(month_end) - get_month_number(month_start))
annualized_gain = (1+percentage_gain)**(1/(total_period/12))-1
loss_frequency = (dca_data['Performance'] < 0).mean()


col1, col2, col3 = st.columns(3)

col1.metric(
    label="Total Invested",
    value=f"${total_invested:,.0f}",
)
col2.metric(
    label="Total Gain",
    value=f"${total_gain:,.2f}",
)
col3.metric(
    label="Final Portfolio Value",
    value=f"${final_portfolio_value:,.2f}",
)

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Percentage Gain",
    value=f"{percentage_gain*100:,.2f}%",
)
col2.metric(
    label="Annualized Gain",
    value=f"{annualized_gain*100:,.2f}%",
)
col3.metric(
    label="Loss Frequency",
    value=f"{loss_frequency*100:.2f}%",
    help="Percentage of days the portfolio value falls below the original cash investment"
)

close_price_data = dca_data[["Date", "Portfolio Value", "Total Cash"]]
close_price_data.set_index("Date", inplace=True)

st.line_chart(
    data=close_price_data,
    use_container_width=True,
    y=["Portfolio Value", "Total Cash"],
    height=400
)

dca_data = dca_data[dca_data["Price Bought"] != 0]


st.dataframe(
    data=dca_data,
    use_container_width=True,
    hide_index=True,
    height=150)

st.divider()


# Performance
# st.write(f"### ${ticker} DCA Performance")


# col1, col2 = st.columns(2)

# col1.metric(
#     label="Total Invested",
#     value=f"${total_invested:,.0f}",
# )
# col1.metric(
#     label="Percentage Gain",
#     value=f"{percentage_gain*100:,.2f}%",
# )

# col2.metric(
#     label="Final Portfolio Value",
#     value=f"${final_portfolio_value:,.2f}",
# )
# col2.metric(
#     label="Annualized Gain",
#     value=f"{annualized_gain*100:,.2f}%",
# )


st.write(f"### Relative Performance Across Other Intervals")

intervals = ["Weekly", "Monthly", "Quarterly", "Biannually"]


compare_data = compare_interval(intervals, historical_data, investment, comm_per_share, comm_min_per_order,
                                comm_max_per_order, platform_fee_per_share, platform_fee_min_per_order, platform_fee_max_per_order)
compare_data.set_index("Date", inplace=True)

adjusted_data = compare_data.subtract(compare_data[f"{interval}"], axis=0)

st.line_chart(
    data=adjusted_data,
    use_container_width=True,
)

st.dataframe(
    data=compare_data,
    use_container_width=True,
    height=150)

# Chart
st.write(f"### Historical Price of ${ticker}")

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
st.write(f"### Other Investment Data")

total_fees_paid = dca_data["Fees Paid"].sum()

col1, col2 = st.columns(2)

col1.metric(
    label="Total Fees",
    value=f"${total_fees_paid:,.2f}"
)

col1.metric(
    label="Proportion To Cash",
    value=f"{total_fees_paid/total_invested*100:.2f}%"
)


col2.write("##### Fees Quick Calculation")

col3, col4 = col2.columns(2)
test_num_share = col3.number_input(
    label="Num of Shares",
    min_value=0.00,
    value=1.00
)
test_share_value = col4.number_input(
    label="Price/Share",
    min_value=0.00,
    value=1.00
)
test_total_value = test_num_share * test_share_value
test_total_fee = max(comm_min_per_order + platform_fee_min_per_order, min(max(test_num_share * (comm_per_share + platform_fee_per_share), comm_min_per_order +
                     platform_fee_min_per_order), (test_total_value) * (comm_max_per_order/100 + platform_fee_max_per_order/100)))

col2.markdown(
    f"The total value for this trade is: **:blue[${test_total_value:,.2f}]**")
col2.markdown(
    f"The total fee for this trade is: **:red[${test_total_fee:,.2f}]**")

