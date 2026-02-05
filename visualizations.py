"""
Visualization Functions
=======================
Plotly chart functions for loan analysis visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict


def plot_balance_comparison(base_df: pd.DataFrame, prepay_df: pd.DataFrame) -> go.Figure:
    """
    Create line chart comparing loan balances over time for both scenarios.
    
    Args:
        base_df: Base scenario amortization schedule
        prepay_df: Prepayment scenario schedule
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Base scenario line
    fig.add_trace(go.Scatter(
        x=base_df['Month'],
        y=base_df['Ending_Balance'],
        mode='lines',
        name='Base Scenario',
        line=dict(color='#3498db', width=2),
        hovertemplate='Month %{x}<br>Balance: ₹%{y:,.2f}<extra></extra>'
    ))
    
    # Prepayment scenario line
    fig.add_trace(go.Scatter(
        x=prepay_df['Month'],
        y=prepay_df['Ending_Balance'],
        mode='lines',
        name='With Extra Payments',
        line=dict(color='#27ae60', width=2),
        hovertemplate='Month %{x}<br>Balance: ₹%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Loan Balance Over Time',
        xaxis_title='Month',
        yaxis_title='Remaining Balance (₹)',
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99),
        template='plotly_white'
    )
    
    # Format y-axis with rupee symbol
    fig.update_yaxes(tickformat='₹,.0f')
    
    return fig


def plot_interest_comparison(comparison_dict: Dict) -> go.Figure:
    """
    Create bar chart showing total interest paid in each scenario.
    
    Args:
        comparison_dict: Dictionary from calculate_scenario_comparison
    
    Returns:
        Plotly figure object
    """
    scenarios = ['Base Scenario', 'With Extra Payments']
    interest_values = [
        comparison_dict['base_total_interest'],
        comparison_dict['prepay_total_interest']
    ]
    colors = ['#3498db', '#27ae60']
    
    fig = go.Figure(data=[
        go.Bar(
            x=scenarios,
            y=interest_values,
            marker_color=colors,
            text=[f'₹{val:,.2f}' for val in interest_values],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Total Interest Comparison',
        yaxis_title='Total Interest Paid (₹)',
        template='plotly_white',
        showlegend=False
    )
    
    fig.update_yaxes(tickformat='₹,.0f')
    
    # Add savings annotation
    if comparison_dict['interest_saved'] > 0:
        fig.add_annotation(
            x=0.5,
            y=max(interest_values) * 0.5,
            text=f"💰 You Save: ₹{comparison_dict['interest_saved']:,.2f}",
            showarrow=False,
            font=dict(size=14, color='#e74c3c'),
            bgcolor='rgba(255,255,255,0.8)'
        )
    
    return fig


def plot_payment_breakdown(schedule_df: pd.DataFrame) -> go.Figure:
    """
    Create stacked area chart showing principal vs interest breakdown over time.
    
    Args:
        schedule_df: Amortization schedule DataFrame
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Principal payment area (bottom)
    fig.add_trace(go.Scatter(
        x=schedule_df['Month'],
        y=schedule_df['Principal_Payment'],
        fill='tozeroy',
        name='Principal',
        mode='lines',
        line=dict(width=0.5, color='#27ae60'),
        fillcolor='rgba(39, 174, 96, 0.6)',
        hovertemplate='Month %{x}<br>Principal: ₹%{y:,.2f}<extra></extra>'
    ))
    
    # Interest payment area (stacked on top)
    fig.add_trace(go.Scatter(
        x=schedule_df['Month'],
        y=schedule_df['Principal_Payment'] + schedule_df['Interest_Payment'],
        fill='tonexty',
        name='Interest',
        mode='lines',
        line=dict(width=0.5, color='#e74c3c'),
        fillcolor='rgba(231, 76, 60, 0.6)',
        hovertemplate='Month %{x}<br>Interest: ₹%{customdata:,.2f}<extra></extra>',
        customdata=schedule_df['Interest_Payment']
    ))
    
    fig.update_layout(
        title='Payment Breakdown Over Time',
        xaxis_title='Month',
        yaxis_title='Payment Amount (₹)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    
    fig.update_yaxes(tickformat='₹,.0f')
    
    return fig


def plot_cumulative_savings(base_df: pd.DataFrame, prepay_df: pd.DataFrame) -> go.Figure:
    """
    Create line chart showing cumulative interest savings over time.
    
    Args:
        base_df: Base scenario schedule
        prepay_df: Prepayment scenario schedule
    
    Returns:
        Plotly figure object
    """
    # Calculate cumulative interest for both scenarios at each month
    max_months = max(len(base_df), len(prepay_df))
    
    savings_data = []
    
    for month in range(1, max_months + 1):
        # Get cumulative interest from base (or last value if past end)
        if month <= len(base_df):
            base_cumulative = base_df[base_df['Month'] == month]['Cumulative_Interest'].values[0]
        else:
            base_cumulative = base_df['Cumulative_Interest'].iloc[-1]
        
        # Get cumulative interest from prepay (or last value if past end)
        if month <= len(prepay_df):
            prepay_cumulative = prepay_df[prepay_df['Month'] == month]['Cumulative_Interest'].values[0]
        else:
            prepay_cumulative = prepay_df['Cumulative_Interest'].iloc[-1]
        
        savings = base_cumulative - prepay_cumulative
        savings_data.append({'Month': month, 'Cumulative_Savings': savings})
    
    savings_df = pd.DataFrame(savings_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=savings_df['Month'],
        y=savings_df['Cumulative_Savings'],
        mode='lines',
        fill='tozeroy',
        name='Interest Savings',
        line=dict(color='#9b59b6', width=2),
        fillcolor='rgba(155, 89, 182, 0.3)',
        hovertemplate='Month %{x}<br>Total Saved: ₹%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Cumulative Interest Savings Over Time',
        xaxis_title='Month',
        yaxis_title='Cumulative Savings (₹)',
        template='plotly_white',
        showlegend=False
    )
    
    fig.update_yaxes(tickformat='₹,.0f')
    
    return fig


def plot_payoff_timeline(base_months: int, prepay_months: int) -> go.Figure:
    """
    Simple visual showing timeline comparison.
    
    Args:
        base_months: Months in base scenario
        prepay_months: Months in prepayment scenario
    
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Base scenario bar
    fig.add_trace(go.Bar(
        y=['Base Scenario'],
        x=[base_months],
        orientation='h',
        name='Base',
        marker_color='#3498db',
        text=f'{base_months} months',
        textposition='inside'
    ))
    
    # Prepayment scenario bar
    fig.add_trace(go.Bar(
        y=['With Extra Payments'],
        x=[prepay_months],
        orientation='h',
        name='Prepayment',
        marker_color='#27ae60',
        text=f'{prepay_months} months',
        textposition='inside'
    ))
    
    fig.update_layout(
        title='Payoff Timeline Comparison',
        xaxis_title='Months',
        template='plotly_white',
        showlegend=False,
        height=250
    )
    
    return fig


def plot_loan_progress(
    original_principal: float,
    current_balance: float,
    months_elapsed: int,
    original_term_months: int
) -> go.Figure:
    """
    Show visual progress of loan repayment.
    
    Args:
        original_principal: Original loan amount
        current_balance: Current outstanding balance
        months_elapsed: Number of months already paid
        original_term_months: Original loan term in months
    
    Returns:
        Plotly figure object
    """
    # Calculate percentages
    principal_paid_pct = ((original_principal - current_balance) / original_principal) * 100
    time_elapsed_pct = (months_elapsed / original_term_months) * 100
    
    fig = go.Figure()
    
    # Principal progress
    fig.add_trace(go.Bar(
        name='Principal Paid',
        x=['Principal'],
        y=[principal_paid_pct],
        marker_color='#2ecc71',
        text=[f'{principal_paid_pct:.1f}%'],
        textposition='inside',
        textfont=dict(color='white', size=14)
    ))
    
    fig.add_trace(go.Bar(
        name='Principal Remaining',
        x=['Principal'],
        y=[100 - principal_paid_pct],
        marker_color='#e74c3c',
        text=[f'{100-principal_paid_pct:.1f}%'],
        textposition='inside',
        textfont=dict(color='white', size=14)
    ))
    
    # Time progress
    fig.add_trace(go.Bar(
        name='Time Elapsed',
        x=['Timeline'],
        y=[time_elapsed_pct],
        marker_color='#3498db',
        text=[f'{time_elapsed_pct:.1f}%'],
        textposition='inside',
        textfont=dict(color='white', size=14)
    ))
    
    fig.add_trace(go.Bar(
        name='Time Remaining',
        x=['Timeline'],
        y=[100 - time_elapsed_pct],
        marker_color='#95a5a6',
        text=[f'{100-time_elapsed_pct:.1f}%'],
        textposition='inside',
        textfont=dict(color='white', size=14)
    ))
    
    fig.update_layout(
        barmode='stack',
        title='Loan Repayment Progress',
        yaxis_title='Percentage',
        showlegend=True,
        height=400,
        template='plotly_white',
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    
    return fig
