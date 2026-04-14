import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class MLPortfolioAnalyzer:
    def __init__(self):
        self.market_data = self._generate_market_data()
        
    def _generate_market_data(self):
        """Generate realistic Indian market data with correlations"""
        np.random.seed(42)
        n_periods = 500  # Reduced for better performance
        
        # Generate correlated returns
        means = [0.01, 0.0058, 0.0058, 0.004]  # equity, bonds, gold, cash
        cov = np.array([
            [0.0036, 0.0004, 0.0006, 0.0000],  # equity
            [0.0004, 0.0004, 0.0002, 0.0000],  # bonds
            [0.0006, 0.0002, 0.0016, 0.0000],  # gold
            [0.0000, 0.0000, 0.0000, 0.0001]   # cash
        ])
        
        returns = np.random.multivariate_normal(means, cov, n_periods)
        
        data = {
            'equity_returns': returns[:, 0],
            'bond_returns': returns[:, 1],
            'gold_returns': returns[:, 2],
            'cash_returns': returns[:, 3],
        }
        
        return pd.DataFrame(data)
    
    def calculate_optimal_allocation(self, user_profile):
        """Calculate optimal portfolio using ML-enhanced Modern Portfolio Theory"""
        risk_profile = user_profile['risk_tolerance']
        age = user_profile['age']
        horizon = user_profile['time_horizon']
        
        # Base allocations
        base_allocations = {
            'conservative': {'equity': 30, 'bonds': 50, 'gold': 15, 'cash': 5},
            'moderate': {'equity': 55, 'bonds': 30, 'gold': 10, 'cash': 5},
            'aggressive': {'equity': 75, 'bonds': 15, 'gold': 5, 'cash': 5}
        }
        
        allocation = base_allocations[risk_profile].copy()
        
        # ML-based adjustments
        # Age factor: younger investors can take more risk
        age_factor = max(0, (40 - age) / 40)
        if risk_profile != 'conservative':
            allocation['equity'] += int(age_factor * 10)
            allocation['bonds'] -= int(age_factor * 10)
        
        # Time horizon factor
        horizon_factor = min(1, horizon / 20)
        if risk_profile != 'conservative':
            allocation['equity'] += int(horizon_factor * 8)
            allocation['bonds'] -= int(horizon_factor * 8)
        
        # Ensure allocations sum to 100
        total = sum(allocation.values())
        if total != 100:
            allocation['equity'] += (100 - total)
        
        return allocation
    
    def monte_carlo_simulation(self, allocation, investment_amount, years):
        """Run Monte Carlo simulation for portfolio projections"""
        np.random.seed(42)
        months = years * 12
        n_simulations = 500  # Reduced for better performance
        
        final_values = []
        
        for _ in range(n_simulations):
            portfolio_value = float(investment_amount)
            
            for month in range(months):
                # Sample from historical returns with some noise
                sample_idx = np.random.randint(0, len(self.market_data))
                monthly_return = 0
                
                for asset, percentage in allocation.items():
                    if asset == 'equity':
                        ret = self.market_data.iloc[sample_idx]['equity_returns']
                    elif asset == 'bonds':
                        ret = self.market_data.iloc[sample_idx]['bond_returns']
                    elif asset == 'gold':
                        ret = self.market_data.iloc[sample_idx]['gold_returns']
                    else:  # cash
                        ret = self.market_data.iloc[sample_idx]['cash_returns']
                    
                    # Add some random noise
                    ret += np.random.normal(0, 0.002)
                    monthly_return += (percentage / 100) * ret
                
                portfolio_value *= (1 + monthly_return)
            
            final_values.append(portfolio_value)
        
        # Calculate statistics - ensure all values are JSON serializable
        final_values = np.array(final_values)
        
        # Convert numpy types to native Python types for JSON serialization
        stats = {
            'mean_final': float(np.mean(final_values)),
            'median_final': float(np.median(final_values)),
            'std_final': float(np.std(final_values)),
            'min_final': float(np.min(final_values)),
            'max_final': float(np.max(final_values)),
            'probability_positive': float(np.mean(final_values > investment_amount) * 100),
            'expected_cagr': float((np.mean(final_values) / investment_amount) ** (1/years) - 1),
            'var_95': float(np.percentile(final_values, 5)),
        }
        
        return stats, final_values.tolist()  # Convert numpy array to list
    
    def generate_recommendations(self, allocation, risk_profile):
        """Generate personalized investment recommendations"""
        equity_funds = {
            'conservative': [
                {'name': 'NIFTY 50 Index Fund', 'type': 'Index Fund', 'risk': 'Medium', 
                 'returns': '11-13%', 'description': 'Diversified exposure to top 50 Indian companies'},
                {'name': 'UTI Nifty 50 Index Fund', 'type': 'Index Fund', 'risk': 'Medium',
                 'returns': '11-13%', 'description': 'Low-cost index fund tracking NIFTY 50'},
            ],
            'moderate': [
                {'name': 'NIFTY 50 Index Fund', 'type': 'Index Fund', 'risk': 'Medium',
                 'returns': '11-13%', 'description': 'Core large-cap exposure'},
                {'name': 'NIFTY Next 50 Index Fund', 'type': 'Index Fund', 'risk': 'Medium-High',
                 'returns': '12-15%', 'description': 'Next 50 companies after NIFTY 50'},
                {'name': 'ICICI Prudential Bluechip Fund', 'type': 'Large Cap', 'risk': 'Medium',
                 'returns': '12-14%', 'description': 'Quality large-cap companies'},
            ],
            'aggressive': [
                {'name': 'NIFTY 50 Index Fund', 'type': 'Index Fund', 'risk': 'Medium',
                 'returns': '11-13%', 'description': 'Foundation large-cap holding'},
                {'name': 'SBI Small Cap Fund', 'type': 'Small Cap', 'risk': 'High',
                 'returns': '14-18%', 'description': 'High-growth small companies'},
                {'name': 'Kotak Emerging Equity Fund', 'type': 'Mid Cap', 'risk': 'High',
                 'returns': '13-16%', 'description': 'Mid-cap growth opportunities'},
            ]
        }
        
        debt_funds = {
            'conservative': [
                {'name': 'SBI Magnum Gilt Fund', 'type': 'Government Bonds', 'risk': 'Low',
                 'returns': '7-8%', 'description': 'Highest safety government securities'},
                {'name': 'ICICI Prudential Corporate Bond Fund', 'type': 'Corporate Bonds', 'risk': 'Low-Medium',
                 'returns': '7.5-8.5%', 'description': 'Quality corporate bonds'},
            ],
            'moderate': [
                {'name': 'Nippon India Strategic Debt Fund', 'type': 'Dynamic Bond', 'risk': 'Low-Medium',
                 'returns': '7-8%', 'description': 'Active duration management'},
                {'name': 'HDFC Corporate Bond Fund', 'type': 'Corporate Bonds', 'risk': 'Low-Medium',
                 'returns': '7.5-8.5%', 'description': 'High-quality corporate debt'},
            ],
            'aggressive': [
                {'name': 'ICICI Prudential Credit Risk Fund', 'type': 'Credit Risk', 'risk': 'Medium-High',
                 'returns': '8-10%', 'description': 'Higher yielding corporate bonds'},
                {'name': 'Franklin India Dynamic Accrual Fund', 'type': 'Dynamic Bond', 'risk': 'Medium',
                 'returns': '7.5-9%', 'description': 'Active bond portfolio management'},
            ]
        }
        
        return {
            'equity': equity_funds[risk_profile],
            'debt': debt_funds[risk_profile],
            'gold': [
                {'name': 'Sovereign Gold Bonds (SGB)', 'type': 'Government Bond', 'risk': 'Low',
                 'returns': '2.5% + Gold Appreciation', 'description': 'Government backed with annual interest'},
            ],
            'cash': [
                {'name': 'Liquid Fund', 'type': 'Debt', 'risk': 'Very Low',
                 'returns': '6-7%', 'description': 'High liquidity with better returns than savings'},
            ]
        }
    
    def generate_insights(self, user_profile, allocation, projections):
        """Generate AI-powered investment insights"""
        insights = []
        age = user_profile['age']
        risk_profile = user_profile['risk_tolerance']
        horizon = user_profile['time_horizon']
        
        # Age-based insights
        if age < 30:
            insights.append("🎯 You're in the perfect wealth accumulation phase - consider increasing equity exposure")
            insights.append("💡 Start a SIP of ₹5,000-10,000 monthly and increase by 10% annually")
        elif age > 45:
            insights.append("🛡️ Focus on capital preservation while maintaining growth - consider balanced funds")
            insights.append("💡 Gradually shift 2-3% annually from equity to debt over next 5 years")
        
        # Risk profile insights
        if risk_profile == 'conservative':
            insights.append("📊 Conservative approach minimizes volatility - consider adding 5% equity for inflation protection")
        elif risk_profile == 'aggressive':
            insights.append("🚀 Aggressive profile can capture higher returns - maintain 6-month emergency fund")
        
        # Time horizon insights
        if horizon < 5:
            insights.append("⏰ Short time horizon - focus on capital protection with debt-oriented funds")
        elif horizon > 15:
            insights.append("📈 Long horizon allows riding market cycles - equity can be 5-10% higher than standard allocation")
        
        # General insights
        insights.extend([
            "📊 Rebalance portfolio annually to maintain target allocation",
            "🇮🇳 Indian equity has strong demographic growth potential - stay invested for long term",
            "🛡️ Gold provides hedge against inflation and currency risk - maintain 5-15% allocation",
            "💰 Increase SIP by 10% annually to accelerate wealth creation",
        ])
        
        return insights