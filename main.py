import streamlit as st
import pandas as pd


def budget_app():
    # --- Configuration and Styling ---
    st.set_page_config(
        page_title="Personal Budget Projection Tool",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("💰 Personal Budget Projection Tool")
    st.markdown("""
    Use the checkboxes to select which expenses are active this month, and enter the corresponding amounts.
    """)

    # --- Data Structure for Expenses ---
    # Dictionary of expense categories and their default values
    EXPENSE_CATEGORIES = {
        "Core - Mortgage": 1200,
        "Core - Utilities": 90,
        "Core - Council Tax": 200,
        "Core - Car": 300,
        "Living - Groceries": 500,
        "Living - Travel": 300,
        "Living - Wellbeing": 200,
        "Living - Clothes": 300,
        "Living - Bills": 50,
        "Living - Homeware": 200,
        "Disposable - Eating Out": 400,
        "Disposable - Drinks and Cafe": 60,
        "Disposable - Events": 100,
        "Investment & Pension": 600,
        "Miscellaneous": 50
    }

    # --- Monthly Income Section ---
    st.header("1. Monthly Income")
    col_inc1, col_inc2 = st.columns(2)

    with col_inc1:
        income1_amount = st.number_input(
            "Income 1 (after tax)",
            min_value=0,
            value=2500,
            step=100,
            key="inc1"
        )
    with col_inc2:
        income2_amount = st.number_input(
            "Income 2 (After Tax)",
            min_value=0,
            value=2500,
            step=100,
            key="inc2"
        )

    total_income = income1_amount + income2_amount
    st.info(f"**Total Monthly Income:** £{total_income:,}")
    st.markdown("---")

    # --- Monthly Expenditure Section ---
    st.header("2. Monthly Expenditure")

    # Store expense results
    expenses = {}
    total_expenditure = 0

    # Layout for Expense Inputs (3 columns: Checkbox, Name, Amount)
    cols_header = st.columns([1, 3, 2])
    cols_header[1].markdown("**Category**")
    cols_header[2].markdown("**Amount ($)**")

    st.markdown("---")

    # Generate interactive rows for each expense category
    for i, (name, default_value) in enumerate(EXPENSE_CATEGORIES.items()):

        # Use a list comprehension to create columns with specific ratios
        col_check, col_name, col_amount = st.columns([1, 3, 2])

        # Checkbox
        is_active = col_check.checkbox("", value=True, key=f"check_{i}")
        col_name.markdown(f"**{name}**")

        # Numeric Input
        if is_active:
            amount = col_amount.number_input(
                "Amount",
                min_value=0,
                value=default_value,
                step=10,
                label_visibility="collapsed",
                key=f"input_{i}"
            )
        else:
            # If checkbox is unticked, set amount to 0
            amount = 0
            # Display a disabled placeholder input
            col_amount.number_input(
                "Amount",
                min_value=0,
                value=0,
                disabled=True,
                label_visibility="collapsed",
                key=f"input_disabled_{i}"
            )

        expenses[name] = amount
        total_expenditure += amount

    # Final Monthly Expenditure Summary
    st.markdown("---")
    st.success(f"**Total Monthly Expenditure:** ${total_expenditure:,.2f}")
    st.markdown("---")

    # --- Projection and Net Calculation ---
    st.header("3. Financial Summary & Projection")

    # Input for number of months
    months = st.number_input(
        "Project over how many months?",
        min_value=1,
        value=6,
        step=1,
        format="%d",
        key="months_input"
    )

    # Calculations
    net_monthly_cashflow = total_income - total_expenditure
    projected_expense = total_expenditure * months
    projected_income = total_income * months
    projected_cashflow = net_monthly_cashflow * months

    # Display Results

    col_net, col_proj = st.columns(2)

    with col_net:
        st.subheader("Monthly Cash Flow")
        if net_monthly_cashflow >= 0:
            st.metric(
                label="Net Monthly Savings",
                value=f"${net_monthly_cashflow:,.2f}",
                delta="You are saving this much per month!"
            )
        else:
            st.metric(
                label="Net Monthly Deficit",
                value=f"${net_monthly_cashflow:,.2f}",
                delta="This is your deficit per month!",
                delta_color="inverse"
            )

    with col_proj:
        st.subheader(f"Projection over {months} Months")
        st.metric(
            label="Total Projected Expenditure",
            value=f"${projected_expense:,.2f}"
        )
        st.metric(
            label="Total Projected Cash Flow (Net)",
            value=f"${projected_cashflow:,.2f}",
        )


# Run the app function
if __name__ == "__main__":
    budget_app()