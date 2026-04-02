# Advanced Monte Carlo Options Pricing Engine
**Python | NumPy | yfinance**

---

## What It Does
Prices European-style call and put options for any stock using Monte Carlo simulation.
Enter a ticker, strike price, and expiration — the model pulls live market data and outputs
a fair option price alongside a full Greeks table for risk analysis.

---

## How It Works
- Simulates **100,000 future price paths** using Geometric Brownian Motion
- Pulls **live stock price, volatility, and the 10-Year Treasury yield** via yfinance
- Calculates option fair value as the discounted average payoff across all paths
- Outputs **Delta, Gamma, Theta, and Vega** using Black-Scholes closed-form

---

## Sample Output
```
Enter ticker symbol: AAPL

=============================================
   MONTE CARLO OPTIONS PRICING  —  AAPL
=============================================
  Stock Price (S):       $246.63
  Strike Price (K):      $220.00
  Time to Expiry (T):    90 day(s)
  Risk-Free Rate (r):    4.34%
  Volatility (sigma):    16.13%
  Simulations:           100,000
---------------------------------------------
  Call Option Price:     $29.4275
  Put Option Price:      $0.4777
=============================================
  Greek              Call        Put
---------------------------------------------
  Delta            0.9452    -0.0548
  Gamma            0.0056     0.0056
  Theta           -0.0364    -0.0105
  Vega             0.1358     0.1358
=============================================
```

