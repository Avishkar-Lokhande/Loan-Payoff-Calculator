"""
Utility Functions
=================
Helper functions for formatting and validation.
"""

from typing import Tuple


def format_currency(amount: float) -> str:
    """
    Format a number as INR currency string.
    
    Args:
        amount: Rupee amount to format
    
    Returns:
        Formatted string like "₹1,234.56"
    """
    return f"₹{amount:,.2f}"


def format_months_to_years(months: int) -> str:
    """
    Convert months to a readable years and months string.
    
    Args:
        months: Total number of months
    
    Returns:
        Formatted string like "5 years, 3 months" or "8 months"
    """
    if months < 0:
        return "0 months"
    
    years = months // 12
    remaining_months = months % 12
    
    if years == 0:
        return f"{remaining_months} month{'s' if remaining_months != 1 else ''}"
    elif remaining_months == 0:
        return f"{years} year{'s' if years != 1 else ''}"
    else:
        year_str = f"{years} year{'s' if years != 1 else ''}"
        month_str = f"{remaining_months} month{'s' if remaining_months != 1 else ''}"
        return f"{year_str}, {month_str}"


def validate_inputs(
    principal: float,
    rate: float,
    term: int,
    extra_payment: float = 0,
    lump_sum: float = 0
) -> Tuple[bool, str]:
    """
    Validate all loan calculator inputs.
    
    Args:
        principal: Loan amount
        rate: Annual interest rate as percentage
        term: Loan term in years
        extra_payment: Monthly extra payment amount
        lump_sum: One-time extra payment
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    errors = []
    
    # Check principal
    if principal <= 0:
        errors.append("Loan amount must be greater than ₹0")
    if principal > 100_000_000:
        errors.append("Loan amount seems unreasonably high")
    
    # Check interest rate
    if rate < 0:
        errors.append("Interest rate cannot be negative")
    if rate > 50:
        errors.append("Interest rate seems unreasonably high (max 50%)")
    
    # Check term
    if term <= 0:
        errors.append("Loan term must be at least 1 year")
    if term > 50:
        errors.append("Loan term cannot exceed 50 years")
    
    # Check extra payments
    if extra_payment < 0:
        errors.append("Extra payment cannot be negative")
    if lump_sum < 0:
        errors.append("Lump sum payment cannot be negative")
    
    if errors:
        return False, "; ".join(errors)
    
    return True, ""


def calculate_apr_from_monthly(monthly_rate: float) -> float:
    """
    Convert monthly rate to annual percentage rate.
    
    Args:
        monthly_rate: Monthly interest rate as decimal
    
    Returns:
        Annual rate as percentage
    """
    return monthly_rate * 12 * 100


def calculate_monthly_from_apr(apr: float) -> float:
    """
    Convert APR to monthly rate.
    
    Args:
        apr: Annual percentage rate
    
    Returns:
        Monthly rate as decimal
    """
    return apr / 100 / 12


def get_loan_type_suggestion(principal: float, term_years: int) -> str:
    """
    Suggest what type of loan this might be based on amount and term.
    
    Args:
        principal: Loan amount
        term_years: Loan term in years
    
    Returns:
        Suggestion string
    """
    if principal >= 100_000 and term_years >= 15:
        return "🏠 This looks like a mortgage loan"
    elif principal >= 20_000 and term_years <= 7:
        return "🚗 This looks like an auto loan"
    elif principal < 20_000 and term_years <= 5:
        return "💳 This looks like a personal loan"
    else:
        return "📊 Custom loan parameters"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a number as percentage string.
    
    Args:
        value: Number to format (already in percentage form)
        decimals: Number of decimal places
    
    Returns:
        Formatted string like "6.50%"
    """
    return f"{value:.{decimals}f}%"
