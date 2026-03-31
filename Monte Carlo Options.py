import yfinance as yf
import numpy as np
import datetime
from statistics import NormalDist

# ── NORMAL DISTRIBUTION ADAPTER (no scipy needed) ────────
_norm = NormalDist()

class norm:
    @staticmethod
    def cdf(x): return _norm.cdf(x)
    @staticmethod
    def pdf(x): return _norm.pdf(x)

# ── LIVE DATA PULL ───────────────────────────────────────
ticker = input("Enter ticker symbol (e.g. AAPL, TSLA, NVDA): ").upper().strip()

stock = yf.Ticker(ticker)
hist  = stock.history(period="1y")

# Current price
S = round(hist["Close"].iloc[-1], 2)

# Annualized historical volatility (20-day rolling, annualized)
daily_returns = hist["Close"].pct_change().dropna()
sigma = round(daily_returns.rolling(20).std().iloc[-1] * np.sqrt(252), 4)

# Live 10-year Treasury yield as risk-free rate
tnx = yf.Ticker("^TNX")
r   = round(tnx.history(period="5d")["Close"].iloc[-1] / 100, 4)

# User inputs for strike and expiry
K = float(input(f"\n  Current price of {ticker}: ${S}  |  Enter strike price: $"))
T = float(input("  Enter time to expiration in days (e.g. 30, 60, 90): ")) / 365

# Simulations
simulations = 100_000
N           = 252

print(f"\n  Fetched sigma (volatility): {sigma*100:.2f}%")
print(f"  Fetched risk-free rate:     {r*100:.2f}%")

# ── MONTE CARLO SIMULATION ───────────────────────────────
np.random.seed(42)

dt = T / N

Z             = np.random.standard_normal((simulations, N))
daily_ret     = np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
price_paths   = S * np.cumprod(daily_ret, axis=1)

S_T           = price_paths[:, -1]

call_payoffs  = np.maximum(S_T - K, 0)
put_payoffs   = np.maximum(K - S_T, 0)

call_price    = np.exp(-r * T) * np.mean(call_payoffs)
put_price     = np.exp(-r * T) * np.mean(put_payoffs)

# ── BLACK-SCHOLES GREEKS ─────────────────────────────────
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

call_delta = norm.cdf(d1)
put_delta  = norm.cdf(d1) - 1

gamma      = norm.pdf(d1) / (S * sigma * np.sqrt(T))

call_theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
               - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
put_theta  = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
               + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365

vega       = S * norm.pdf(d1) * np.sqrt(T) * 0.01

# ── OUTPUT ───────────────────────────────────────────────
print("\n" + "=" * 45)
print(f"   MONTE CARLO OPTIONS PRICING  —  {ticker}")
print("=" * 45)
print(f"  Stock Price (S):       ${S:.2f}")
print(f"  Strike Price (K):      ${K:.2f}")
print(f"  Time to Expiry (T):    {T*365:.0f} day(s)")
print(f"  Risk-Free Rate (r):    {r*100:.2f}%")
print(f"  Volatility (sigma):    {sigma*100:.2f}%")
print(f"  Simulations:           {simulations:,}")
print("-" * 45)
print(f"  Call Option Price:     ${call_price:.4f}")
print(f"  Put Option Price:      ${put_price:.4f}")

print("\n" + "=" * 45)
print("   OPTIONS GREEKS (Black-Scholes)")
print("=" * 45)
print(f"  {'Greek':<12} {'Call':>10} {'Put':>10}")
print("-" * 45)
print(f"  {'Delta':<12} {call_delta:>10.4f} {put_delta:>10.4f}")
print(f"  {'Gamma':<12} {gamma:>10.4f} {gamma:>10.4f}")
print(f"  {'Theta':<12} {call_theta:>10.4f} {put_theta:>10.4f}")
print(f"  {'Vega':<12} {vega:>10.4f} {vega:>10.4f}")
print("=" * 45)
print("\n  Interpretation:")
print(f"  > Call Delta {call_delta:.2f}: call gains ${call_delta:.2f} per $1 stock rise")
print(f"  > Theta {call_theta:.4f}: call loses ${abs(call_theta):.4f} in value per day")
print(f"  > Vega {vega:.4f}: option gains ${vega:.4f} per 1% vol increase")
print("=" * 45)