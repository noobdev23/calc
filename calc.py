import math
import requests
import tkinter as tk

# API endpoint to fetch latest exchange rates
API_ENDPOINT = "https://api.exchangeratesapi.io/latest"

# function to fetch latest exchange rates from the API
def get_exchange_rate(base_currency, target_currency):
    response = requests.get(API_ENDPOINT, params={"base": base_currency, "symbols": target_currency})
    if response.status_code == 200:
        data = response.json()
        return data["rates"][target_currency]
    else:
        return None

# function to calculate EMI for a given loan amount, interest rate, and tenure
def calculate_emi(principal, rate, tenure, frequency=12):
    rate_per_period = rate / (frequency * 100)
    num_periods = tenure * frequency
    emi = (principal * rate_per_period * (1 + rate_per_period) ** num_periods) / ((1 + rate_per_period) ** num_periods - 1)
    return emi

# function to generate amortization schedule for a given loan amount, interest rate, tenure and EMI
def generate_amortization_schedule(principal, rate, tenure, emi, frequency=12):
    rate_per_period = rate / (frequency * 100)
    num_periods = tenure * frequency
    balance = principal
    amortization_schedule = []
    for i in range(1, num_periods + 1):
        interest = balance * rate_per_period
        principal_paid = emi - interest
        balance = balance - principal_paid
        row = {"period": i, "balance": balance, "principal": principal_paid, "interest": interest}
        amortization_schedule.append(row)
    return amortization_schedule

# function to calculate revised EMI and interest savings based on additional prepayments
def calculate_prepayment_impact(principal, rate, tenure, emi, prepayment_amount, prepayment_frequency=1, frequency=12):
    rate_per_period = rate / (frequency * 100)
    num_periods = tenure * frequency
    balance = principal
    revised_emi = calculate_emi(principal - prepayment_amount, rate, tenure, frequency)
    interest_savings = 0
    for i in range(1, num_periods + 1):
        if i % prepayment_frequency == 0:
            balance = balance - prepayment_amount
        interest = balance * rate_per_period
        interest_savings += (emi - revised_emi) + interest
        principal_paid = revised_emi - interest
        balance = balance - principal_paid
    return {"revised_emi": revised_emi, "interest_savings": interest_savings}

# function to display the results in the GUI
def display_results(principal, rate, tenure, base_currency, target_currency, emi, amortization_schedule):
    # create a new window for displaying the results
    result_window = tk.Toplevel(root)
    result_window.title("EMI Calculator - Results")
    result_window.geometry("500x500")
    
    # create a label for displaying the loan amount
    amount_label = tk.Label(result_window, text=f"Loan Amount: {base_currency} {principal:,.2f}", font=("Arial", 16))
    amount_label.pack(pady=10)
    
    # create a label for displaying the interest rate
    rate_label = tk.Label(result_window, text=f"Interest Rate: {rate}%", font=("Arial", 16))
    rate_label.pack(pady=10)
    
    # create a label for displaying the loan tenure
    tenure_label = tk.Label
