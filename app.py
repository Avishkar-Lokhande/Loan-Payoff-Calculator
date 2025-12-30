"""
Loan Payoff Calculator - Streamlit Application
==============================================
A comprehensive loan analysis tool with prepayment scenarios.

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import our custom modules
from calculations import (
    calculate_monthly_payment,
    generate_base_amortization_schedule,
    generate_prepayment_schedule,
    calculate_scenario_comparison,
    calculate_target_extra_payment
)
from visualizations import (
    plot_balance_comparison,
    plot_interest_comparison,
    plot_payment_breakdown,
    plot_cumulative_savings,
    plot_payoff_timeline
)
from utils import (
    format_currency,
    format_months_to_years,
    validate_inputs,
    get_loan_type_suggestion
)

# Page configuration
st.set_page_config(
    page_title="Loan Payoff Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .big-number {
        font-size: 2em;
        font-weight: bold;
        color: #1f77b4;
    }
    .savings-highlight {
        background-color: #d4edda;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)


# ============ SIDEBAR INPUTS ============
st.sidebar.title("💰 Loan Payoff Calculator")
st.sidebar.markdown("---")

# Loan Details Section
st.sidebar.header("📋 Loan Details")

principal = st.sidebar.number_input(
    "Loan Amount ($)",
    min_value=1000,
    max_value=10_000_000,
    value=300_000,
    step=1000,
    help="The total amount you're borrowing"
)

annual_rate_percent = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.0,
    max_value=30.0,
    value=6.5,
    step=0.1,
    help="Your loan's annual interest rate"
)

term_years = st.sidebar.number_input(
    "Loan Term (years)",
    min_value=1,
    max_value=40,
    value=30,
    step=1,
    help="Total length of the loan"
)

# Prepayment Options Section
st.sidebar.markdown("---")
st.sidebar.header("💵 Extra Payment Options")

extra_monthly = st.sidebar.number_input(
    "Extra Monthly Payment ($)",
    min_value=0,
    max_value=100_000,
    value=0,
    step=50,
    help="Additional amount you'll pay each month"
)

lump_sum = st.sidebar.number_input(
    "One-Time Lump Sum ($)",
    min_value=0,
    max_value=1_000_000,
    value=0,
    step=1000,
    help="A single extra payment you plan to make"
)

term_months = term_years * 12
lump_sum_month = st.sidebar.number_input(
    "Lump Sum Payment Month",
    min_value=1,
    max_value=term_months,
    value=min(12, term_months),
    step=1,
    help="Which month will you make the lump sum payment?"
)

# Validate inputs
is_valid, error_msg = validate_inputs(
    principal, annual_rate_percent, term_years, extra_monthly, lump_sum
)

if not is_valid:
    st.sidebar.error(f"⚠️ {error_msg}")
    st.stop()

# Convert rate to decimal
annual_rate = annual_rate_percent / 100

# Calculate base monthly payment
monthly_payment = calculate_monthly_payment(principal, annual_rate, term_months)

st.sidebar.markdown("---")
st.sidebar.success(f"📊 Base Monthly Payment: **{format_currency(monthly_payment)}**")

# Show loan type suggestion
loan_suggestion = get_loan_type_suggestion(principal, term_years)
st.sidebar.info(loan_suggestion)


# ============ MAIN CONTENT AREA ============
st.title("🏦 Loan Payoff Analysis")
st.markdown(f"*Analysis generated on {datetime.now().strftime('%B %d, %Y')}*")

# Generate schedules
with st.spinner("Calculating your loan scenarios..."):
    try:
        base_schedule = generate_base_amortization_schedule(
            principal, annual_rate, monthly_payment, term_months
        )

        prepay_schedule = generate_prepayment_schedule(
            principal, annual_rate, monthly_payment,
            extra_monthly, lump_sum, lump_sum_month
        )

        comparison = calculate_scenario_comparison(base_schedule, prepay_schedule, principal)
    except Exception as e:
        st.error(f"An error occurred during calculation: {e}")
        st.stop()

# Check if prepayment makes a difference
has_prepayment = extra_monthly > 0 or lump_sum > 0

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Summary", 
    "📅 Amortization Schedule", 
    "📈 Visualizations",
    "🔮 What-If Scenarios",
    "📖 Methodology"
])


# ============ TAB 1: SUMMARY ============
with tab1:
    st.header("Loan Comparison Summary")
    
    if has_prepayment:
        # Show savings metrics in columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Interest Saved",
                value=format_currency(comparison['interest_saved']),
                delta=f"{comparison['savings_percentage']}% less interest"
            )
        
        with col2:
            st.metric(
                label="Time Saved",
                value=format_months_to_years(comparison['months_saved']),
                delta=f"{comparison['months_saved']} fewer payments"
            )
        
        with col3:
            net_savings = comparison['interest_saved'] - comparison['total_extra_payments']
            st.metric(
                label="Net Savings",
                value=format_currency(net_savings),
                delta="after extra payments"
            )
        
        st.markdown("---")
    
    # Comparison table
    st.subheader("📋 Detailed Comparison")
    
    comparison_data = {
        'Metric': [
            'Monthly Payment',
            'Total Months',
            'Payoff Time',
            'Total Interest',
            'Total Amount Paid',
            'Extra Payments Made'
        ],
        'Base Scenario': [
            format_currency(monthly_payment),
            comparison['base_months'],
            format_months_to_years(comparison['base_months']),
            format_currency(comparison['base_total_interest']),
            format_currency(comparison['base_total_paid']),
            format_currency(0)
        ],
        'With Prepayment': [
            format_currency(monthly_payment + extra_monthly),
            comparison['prepay_months'],
            format_months_to_years(comparison['prepay_months']),
            format_currency(comparison['prepay_total_interest']),
            format_currency(comparison['prepay_total_paid']),
            format_currency(comparison['total_extra_payments'])
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    if has_prepayment:
        st.markdown("""
        <div class="savings-highlight">
            <strong>💡 Key Insight:</strong> By making extra payments, you'll save 
            <strong>{}</strong> in interest and pay off your loan 
            <strong>{}</strong> earlier!
        </div>
        """.format(
            format_currency(comparison['interest_saved']),
            format_months_to_years(comparison['months_saved'])
        ), unsafe_allow_html=True)
    else:
        st.info("💡 **Tip:** Add extra monthly payments or a lump sum in the sidebar to see potential savings!")


# ============ TAB 2: AMORTIZATION SCHEDULE ============
with tab2:
    st.header("Amortization Schedule")
    
    schedule_choice = st.radio(
        "Select Schedule to View:",
        ["Base Scenario", "Prepayment Scenario"],
        horizontal=True
    )
    
    if schedule_choice == "Base Scenario":
        display_schedule = base_schedule.copy()
    else:
        display_schedule = prepay_schedule.copy()
    
    # Format currency columns for display
    currency_cols = ['Beginning_Balance', 'Monthly_Payment', 'Principal_Payment', 
                     'Interest_Payment', 'Ending_Balance', 'Cumulative_Interest']
    
    if 'Extra_Payment' in display_schedule.columns:
        currency_cols.extend(['Extra_Payment', 'Total_Payment'])
    
    # Create formatted version for display
    formatted_schedule = display_schedule.copy()
    for col in currency_cols:
        if col in formatted_schedule.columns:
            formatted_schedule[col] = formatted_schedule[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(formatted_schedule, use_container_width=True, hide_index=True)
    
    # Download button
    csv = display_schedule.to_csv(index=False)
    st.download_button(
        label="📥 Download Schedule as CSV",
        data=csv,
        file_name=f"amortization_schedule_{schedule_choice.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
    
    # Quick stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Months", len(display_schedule))
    with col2:
        st.metric("Total Interest", format_currency(display_schedule['Interest_Payment'].sum()))
    with col3:
        first_interest = display_schedule.iloc[0]['Interest_Payment']
        st.metric("First Month Interest", format_currency(first_interest))
    with col4:
        last_interest = display_schedule.iloc[-1]['Interest_Payment']
        st.metric("Last Month Interest", format_currency(last_interest))


# ============ TAB 3: VISUALIZATIONS ============
with tab3:
    st.header("Visual Analysis")
    
    # Balance comparison chart
    st.subheader("📉 Loan Balance Over Time")
    st.caption("See how quickly your loan balance decreases with each scenario")
    fig_balance = plot_balance_comparison(base_schedule, prepay_schedule)
    st.plotly_chart(fig_balance, use_container_width=True)
    
    st.markdown("---")
    
    # Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💵 Total Interest Comparison")
        st.caption("Compare total interest paid in each scenario")
        fig_interest = plot_interest_comparison(comparison)
        st.plotly_chart(fig_interest, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Payoff Timeline")
        st.caption("Visual comparison of loan duration")
        fig_timeline = plot_payoff_timeline(
            comparison['base_months'], 
            comparison['prepay_months']
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    st.markdown("---")
    
    # Payment breakdown
    st.subheader("📊 Payment Breakdown Over Time")
    st.caption("See how your payment splits between principal and interest each month")
    
    breakdown_choice = st.radio(
        "Select scenario:",
        ["Base Scenario", "With Prepayment"],
        horizontal=True,
        key="breakdown_radio"
    )
    
    if breakdown_choice == "Base Scenario":
        fig_breakdown = plot_payment_breakdown(base_schedule)
    else:
        fig_breakdown = plot_payment_breakdown(prepay_schedule)
    
    st.plotly_chart(fig_breakdown, use_container_width=True)
    
    # Cumulative savings
    if has_prepayment:
        st.markdown("---")
        st.subheader("💰 Cumulative Interest Savings")
        st.caption("Watch your savings grow over time with extra payments")
        fig_savings = plot_cumulative_savings(base_schedule, prepay_schedule)
        st.plotly_chart(fig_savings, use_container_width=True)


# ============ TAB 4: WHAT-IF SCENARIOS ============
with tab4:
    st.header("What-If Scenario Planner")
    
    st.markdown("""
    Use this tool to explore different payoff strategies and find the right balance 
    for your budget.
    """)
    
    st.subheader("🎯 Target Payoff Calculator")
    st.caption("Find out how much extra you need to pay to reach your goal")
    
    # Target years slider
    target_years = st.slider(
        "I want to pay off my loan in...",
        min_value=1,
        max_value=term_years,
        value=max(1, term_years // 2),
        format="%d years"
    )
    
    target_months = target_years * 12
    
    if target_months < term_months:
        required_extra = calculate_target_extra_payment(
            principal, annual_rate, monthly_payment, target_months
        )
        
        # Calculate the resulting scenario
        target_schedule = generate_prepayment_schedule(
            principal, annual_rate, monthly_payment,
            extra_monthly=required_extra, lump_sum_amount=0, lump_sum_month=1
        )
        
        target_comparison = calculate_scenario_comparison(
            base_schedule, target_schedule, principal
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            ### 🎯 To pay off in {target_years} years:
            
            **Extra monthly payment needed:** {format_currency(required_extra)}
            
            **New total monthly payment:** {format_currency(monthly_payment + required_extra)}
            """)
        
        with col2:
            st.info(f"""
            ### 💰 Your Savings:
            
            **Interest saved:** {format_currency(target_comparison['interest_saved'])}
            
            **Time saved:** {format_months_to_years(target_comparison['months_saved'])}
            """)
    else:
        st.info("Select a target that's shorter than your current loan term to see required extra payments.")
    
    st.markdown("---")
    
    # Custom scenario comparison
    st.subheader("📊 Compare Multiple Scenarios")
    st.caption("Add different extra payment amounts to compare side by side")
    
    # Initialize session state for scenarios
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = [100, 200, 500]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_amount = st.number_input(
            "Extra payment amount to add:",
            min_value=0,
            max_value=50000,
            value=300,
            step=50
        )
    with col2:
        if st.button("➕ Add Scenario"):
            if new_amount not in st.session_state.scenarios:
                st.session_state.scenarios.append(new_amount)
    
    if st.button("🗑️ Clear All Scenarios"):
        st.session_state.scenarios = []
    
    # Generate comparison table
    if st.session_state.scenarios:
        scenario_results = []
        
        for extra in sorted(st.session_state.scenarios):
            scenario_schedule = generate_prepayment_schedule(
                principal, annual_rate, monthly_payment,
                extra_monthly=extra, lump_sum_amount=0, lump_sum_month=1
            )
            
            scenario_comparison = calculate_scenario_comparison(
                base_schedule, scenario_schedule, principal
            )
            
            scenario_results.append({
                'Extra Monthly': format_currency(extra),
                'Total Monthly': format_currency(monthly_payment + extra),
                'Months to Payoff': scenario_comparison['prepay_months'],
                'Payoff Time': format_months_to_years(scenario_comparison['prepay_months']),
                'Interest Saved': format_currency(scenario_comparison['interest_saved']),
                'Total Interest': format_currency(scenario_comparison['prepay_total_interest'])
            })
        
        scenarios_df = pd.DataFrame(scenario_results)
        st.dataframe(scenarios_df, use_container_width=True, hide_index=True)


# ============ TAB 5: METHODOLOGY ============
with tab5:
    st.header("How It Works")
    
    st.markdown("""
    This calculator uses standard financial formulas to compute loan amortization 
    schedules and analyze the impact of prepayments.
    """)
    
    with st.expander("📐 Monthly Payment Formula", expanded=True):
        st.markdown("""
        The monthly payment is calculated using the standard amortization formula:
        
        $$PMT = P \\times \\frac{r(1+r)^n}{(1+r)^n - 1}$$
        
        Where:
        - **PMT** = Monthly payment
        - **P** = Principal (loan amount)
        - **r** = Monthly interest rate (annual rate / 12)
        - **n** = Total number of payments (months)
        
        *We use numpy-financial's `pmt()` function which implements this formula.*
        """)
    
    with st.expander("💰 Interest Calculation"):
        st.markdown("""
        For each month, interest is calculated on the remaining balance:
        
        $$Interest = Balance \\times \\frac{Annual\\ Rate}{12}$$
        
        The principal portion of your payment is:
        
        $$Principal\\ Payment = Monthly\\ Payment - Interest$$
        
        Your new balance becomes:
        
        $$New\\ Balance = Previous\\ Balance - Principal\\ Payment$$
        """)
    
    with st.expander("🚀 Prepayment Logic"):
        st.markdown("""
        When you make extra payments:
        
        1. **Extra Monthly Payments** - Added to each month's payment, going entirely 
           toward principal
        2. **Lump Sum Payments** - One-time payment applied in a specific month, 
           reducing principal immediately
        
        Benefits of prepayment:
        - Reduces total interest paid
        - Shortens loan term
        - Builds equity faster
        
        **Note:** Extra payments are applied directly to principal, which then reduces 
        future interest charges since interest is calculated on remaining balance.
        """)
    
    with st.expander("⚠️ Disclaimer"):
        st.warning("""
        **Important Notice:**
        
        This calculator provides estimates for educational purposes only. Actual loan 
        terms may vary based on:
        
        - Your lender's specific calculation methods
        - Prepayment penalties (if any)
        - Payment timing and processing
        - Rounding differences
        - Additional fees not included here
        
        Always consult with your lender or a financial advisor for exact figures 
        and personalized advice.
        """)
    
    st.markdown("---")
    st.caption("Built with Streamlit • Made for Finance Enthusiasts")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <strong>Pro Tip:</strong> Even small extra payments can make a big difference over time!</p>
</div>
""", unsafe_allow_html=True)
