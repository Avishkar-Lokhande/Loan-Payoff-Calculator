"""
Loan Calculation Functions
==========================
Core financial calculations for loan amortization and prepayment analysis.
"""

import pandas as pd
import numpy_financial as npf
from typing import Dict, Optional
import streamlit as st


@st.cache_data(show_spinner=False)
def calculate_monthly_payment(principal: float, annual_rate: float, term_months: int) -> float:
    """
    Calculate the monthly payment for a loan using standard amortization formula.
    
    Args:
        principal: Loan amount in dollars
        annual_rate: Annual interest rate as decimal (e.g., 0.065 for 6.5%)
        term_months: Total number of months for the loan
    
    Returns:
        Monthly payment amount (positive value)
    """
    # Handle zero interest rate edge case
    if annual_rate == 0:
        return principal / term_months
    
    monthly_rate = annual_rate / 12
    
    # Using numpy-financial's pmt function
    # Returns negative value (cash outflow), so we take absolute
    payment = npf.pmt(monthly_rate, term_months, -principal)
    
    return abs(payment)


@st.cache_data(show_spinner=False)
def generate_base_amortization_schedule(
    principal: float,
    annual_rate: float,
    monthly_payment: float,
    term_months: int
) -> pd.DataFrame:
    """
    Generate a complete amortization schedule without any extra payments.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as decimal
        monthly_payment: Fixed monthly payment amount
        term_months: Total loan term in months
    
    Returns:
        DataFrame with month-by-month breakdown of payments
    """
    monthly_rate = annual_rate / 12
    
    # Initialize lists to store schedule data
    schedule_data = []
    balance = principal
    cumulative_interest = 0
    
    for month in range(1, term_months + 1):
        beginning_balance = balance
        
        # Calculate interest for this month
        interest_payment = beginning_balance * monthly_rate
        
        # Principal is whatever's left after interest
        principal_payment = monthly_payment - interest_payment
        
        # Handle final month - might need adjustment
        if principal_payment > beginning_balance:
            principal_payment = beginning_balance
            actual_payment = principal_payment + interest_payment
        else:
            actual_payment = monthly_payment
        
        ending_balance = beginning_balance - principal_payment
        cumulative_interest += interest_payment
        
        # Add this month's data
        schedule_data.append({
            'Month': month,
            'Beginning_Balance': round(beginning_balance, 2),
            'Monthly_Payment': round(actual_payment, 2),
            'Principal_Payment': round(principal_payment, 2),
            'Interest_Payment': round(interest_payment, 2),
            'Ending_Balance': round(max(ending_balance, 0), 2),
            'Cumulative_Interest': round(cumulative_interest, 2)
        })
        
        balance = ending_balance
        
        # Stop if loan is paid off
        if balance <= 0:
            break
    
    return pd.DataFrame(schedule_data)


@st.cache_data(show_spinner=False)
def generate_prepayment_schedule(
    principal: float,
    annual_rate: float,
    monthly_payment: float,
    extra_monthly: float = 0,
    lump_sum_amount: float = 0,
    lump_sum_month: int = 1
) -> pd.DataFrame:
    """
    Generate amortization schedule with extra payments factored in.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as decimal
        monthly_payment: Base monthly payment amount
        extra_monthly: Additional amount paid every month
        lump_sum_amount: One-time extra payment amount
        lump_sum_month: Month number when lump sum is applied
    
    Returns:
        DataFrame with prepayment schedule including extra payment columns
    """
    monthly_rate = annual_rate / 12
    
    schedule_data = []
    balance = principal
    cumulative_interest = 0
    month = 0
    
    while balance > 0:
        month += 1
        beginning_balance = balance
        
        # Calculate interest
        interest_payment = beginning_balance * monthly_rate
        
        # Determine extra payment for this month
        extra_this_month = extra_monthly
        if month == lump_sum_month:
            extra_this_month += lump_sum_amount
        
        # Calculate principal portion
        base_principal = monthly_payment - interest_payment
        total_principal = base_principal + extra_this_month
        
        # Don't overpay - cap at remaining balance
        if total_principal > beginning_balance:
            total_principal = beginning_balance
            extra_this_month = total_principal - base_principal
            if extra_this_month < 0:
                extra_this_month = 0
                total_principal = beginning_balance
        
        ending_balance = beginning_balance - total_principal
        cumulative_interest += interest_payment
        
        # Calculate total payment this month
        total_payment = interest_payment + total_principal
        
        schedule_data.append({
            'Month': month,
            'Beginning_Balance': round(beginning_balance, 2),
            'Monthly_Payment': round(monthly_payment, 2),
            'Extra_Payment': round(extra_this_month, 2),
            'Total_Payment': round(total_payment, 2),
            'Principal_Payment': round(total_principal, 2),
            'Interest_Payment': round(interest_payment, 2),
            'Ending_Balance': round(max(ending_balance, 0), 2),
            'Cumulative_Interest': round(cumulative_interest, 2)
        })
        
        balance = ending_balance
        
        # Safety check - don't go beyond 50 years
        if month > 600:
            break
    
    return pd.DataFrame(schedule_data)


def calculate_scenario_comparison(
    base_schedule: pd.DataFrame,
    prepay_schedule: pd.DataFrame,
    principal: float
) -> Dict:
    """
    Compare base scenario with prepayment scenario and calculate savings.
    
    Args:
        base_schedule: DataFrame from generate_base_amortization_schedule
        prepay_schedule: DataFrame from generate_prepayment_schedule
        principal: Original loan amount
    
    Returns:
        Dictionary containing comparison metrics
    """
    # Calculate totals from base schedule
    base_total_interest = base_schedule['Interest_Payment'].sum()
    base_months = len(base_schedule)
    base_total_paid = base_schedule['Monthly_Payment'].sum()
    
    # Calculate totals from prepayment schedule
    prepay_total_interest = prepay_schedule['Interest_Payment'].sum()
    prepay_months = len(prepay_schedule)
    prepay_total_paid = prepay_schedule['Total_Payment'].sum()
    
    # Calculate savings
    interest_saved = base_total_interest - prepay_total_interest
    months_saved = base_months - prepay_months
    total_extra_payments = prepay_schedule['Extra_Payment'].sum()
    
    return {
        'base_total_interest': round(base_total_interest, 2),
        'prepay_total_interest': round(prepay_total_interest, 2),
        'interest_saved': round(interest_saved, 2),
        'base_months': base_months,
        'prepay_months': prepay_months,
        'months_saved': months_saved,
        'base_total_paid': round(base_total_paid, 2),
        'prepay_total_paid': round(prepay_total_paid, 2),
        'total_extra_payments': round(total_extra_payments, 2),
        'savings_percentage': round((interest_saved / base_total_interest) * 100, 2) if base_total_interest > 0 else 0
    }


@st.cache_data(show_spinner=False)
def calculate_target_extra_payment(
    principal: float,
    annual_rate: float,
    monthly_payment: float,
    target_months: int
) -> float:
    """
    Calculate the extra monthly payment needed to pay off loan in target months.
    Uses binary search to find the required extra payment.
    
    Args:
        principal: Original loan amount
        annual_rate: Annual interest rate as decimal
        monthly_payment: Base monthly payment
        target_months: Desired payoff timeline in months
    
    Returns:
        Extra monthly payment required to meet target
    """
    # If target is longer than natural payoff, no extra needed
    base_schedule = generate_base_amortization_schedule(
        principal, annual_rate, monthly_payment, target_months + 120
    )
    if len(base_schedule) <= target_months:
        return 0.0
    
    # Binary search for the right extra payment
    low = 0
    high = principal / target_months  # Max would be paying it all equally
    tolerance = 0.01
    
    for _ in range(100):  # Max iterations
        mid = (low + high) / 2
        
        # Generate schedule with this extra payment
        test_schedule = generate_prepayment_schedule(
            principal, annual_rate, monthly_payment,
            extra_monthly=mid, lump_sum_amount=0, lump_sum_month=1
        )
        
        actual_months = len(test_schedule)
        
        if abs(actual_months - target_months) <= 1:
            # Close enough, but verify we're at or below target
            if actual_months <= target_months:
                return round(mid, 2)
            else:
                low = mid
        elif actual_months > target_months:
            # Need more extra payment
            low = mid
        else:
            # Paying too fast, reduce extra
            high = mid
        
        # Check if we've converged
        if high - low < tolerance:
            break
    
    return round(mid, 2)


def get_payoff_summary(schedule: pd.DataFrame) -> Dict:
    """
    Get a quick summary of a loan schedule.
    
    Args:
        schedule: Amortization schedule DataFrame
    
    Returns:
        Dictionary with summary stats
    """
    return {
        'total_months': len(schedule),
        'total_interest': round(schedule['Interest_Payment'].sum(), 2),
        'final_payment': round(schedule.iloc[-1]['Monthly_Payment'] if 'Monthly_Payment' in schedule.columns else schedule.iloc[-1]['Total_Payment'], 2),
        'avg_monthly_interest': round(schedule['Interest_Payment'].mean(), 2)
    }
