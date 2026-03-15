"""
Financial Analysis and Metrics Calculator
MBA Finance Concepts: Ratio Analysis, Financial Performance Metrics
"""
import pandas as pd
import numpy as np

class FinancialCalculator:
    """Calculate key financial metrics and ratios"""
    
    @staticmethod
    def calculate_growth_rate(data: pd.DataFrame, column: str) -> dict:
        """
        Calculate YoY growth rate
        - Input: DataFrame with yearly data
        - Output: Growth rates as percentages
        """
        if len(data) < 2:
            return {}
        
        growth_rates = {}
        for i in range(1, len(data)):
            year = data.iloc[i]['Year']
            if data.iloc[i-1][column] != 0:
                growth = ((data.iloc[i][column] - data.iloc[i-1][column]) / 
                         data.iloc[i-1][column] * 100)
                growth_rates[f"{int(year)}"] = round(growth, 2)
        
        return growth_rates
    
    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR)
        MBA Finance: Growth Metric
        """
        if start_value <= 0 or years == 0:
            return 0
        
        cagr = (pow(end_value / start_value, 1 / years) - 1) * 100
        return round(cagr, 2)
    
    @staticmethod
    def evaluate_profitability(net_margin: float, operating_margin: float) -> str:
        """
        Qualitative assessment of profitability
        MBA Finance: Profitability Analysis
        """
        if net_margin >= 15:
            return "Excellent - Strong pricing power and cost control"
        elif net_margin >= 10:
            return "Good - Healthy profitability"
        elif net_margin >= 5:
            return "Moderate - Revenue growth opportunities"
        else:
            return "Weak - Margin expansion needed"
    
    @staticmethod
    def evaluate_efficiency(roe: float, roa: float) -> str:
        """
        Evaluate operational efficiency
        MBA Finance: ROE & ROA Analysis
        """
        if roe >= 20 and roa >= 8:
            return "Excellent - Best-in-class capital efficiency"
        elif roe >= 15 and roa >= 5:
            return "Good - Effective capital deployment"
        elif roe >= 10:
            return "Moderate - Reasonable returns"
        else:
            return "Weak - Capital optimization needed"
    
    @staticmethod
    def evaluate_leverage(debt_equity: float) -> str:
        """
        Evaluate financial leverage
        MBA Finance: Capital Structure Analysis
        """
        if debt_equity <= 0.3:
            return "Conservative - Low financial risk"
        elif debt_equity <= 0.6:
            return "Moderate - Balanced capital structure"
        elif debt_equity <= 1.0:
            return "Elevated - Manageable leverage"
        else:
            return "High - Strategic focus on deleveraging"
    
    @staticmethod
    def evaluate_valuation(pe_ratio: float, sector: str) -> str:
        """
        Evaluate valuation metrics vs sector context
        MBA Finance: Valuation Analysis
        """
        sector_pe_benchmarks = {
            'IT': 30,
            'Banking': 18,
            'Pharma': 22,
            'Auto': 15,
            'FMCG': 25,
            'Energy': 12
        }
        
        benchmark = sector_pe_benchmarks.get(sector, 20)
        
        if pe_ratio < benchmark * 0.8:
            return f"Attractive - Trading below sector average ({benchmark}x)"
        elif pe_ratio < benchmark * 1.2:
            return f"Fair - In line with sector average ({benchmark}x)"
        else:
            return f"Premium - Trading above sector average ({benchmark}x)"
    
    @staticmethod
    def generate_investment_view(financials: dict, trends: dict, valuations: dict) -> dict:
        """
        Generate Buy/Hold/Sell recommendation based on MBA finance framework
        
        Parameters:
        - financials: Latest financial metrics
        - trends: Growth and momentum indicators
        - valuations: Valuation assessment
        
        Returns:
        - Investment view with justification
        """
        score = 0
        factors = []
        
        # Profitability scoring
        if financials.get('net_margin', 0) >= 12:
            score += 2
            factors.append("Strong profitability margins")
        elif financials.get('net_margin', 0) >= 8:
            score += 1
        else:
            factors.append("Weak profitability margins")
        
        # ROE scoring
        if financials.get('roe', 0) >= 18:
            score += 2
            factors.append("Excellent capital efficiency (ROE > 18%)")
        elif financials.get('roe', 0) >= 12:
            score += 1
        
        # Revenue growth
        if trends.get('revenue_growth', 0) >= 12:
            score += 2
            factors.append("Strong revenue growth trajectory")
        elif trends.get('revenue_growth', 0) >= 8:
            score += 1
        else:
            factors.append("Moderate growth momentum")
        
        # Valuation
        if valuations.get('pe_signal') == "Attractive":
            score += 2
            factors.append("Attractive valuation metrics")
        elif valuations.get('pe_signal') == "Fair":
            score += 1
        else:
            factors.append("Premium valuation")
        
        # Leverage
        if financials.get('debt_equity', 1) <= 0.5:
            score += 1
            factors.append("Conservative balance sheet")
        elif financials.get('debt_equity', 1) > 1.0:
            score -= 1
            factors.append("Elevated leverage requires monitoring")
        
        # Determine recommendation
        if score >= 8:
            recommendation = "BUY"
            rationale = "Strong fundamentals with attractive risk-reward profile"
        elif score >= 4:
            recommendation = "HOLD"
            rationale = "Fairly valued with balanced profile"
        else:
            recommendation = "SELL"
            rationale = "Weak fundamentals or unfavorable valuation"
        
        return {
            'view': recommendation,
            'rationale': rationale,
            'key_factors': factors,
            'confidence_score': score
        }
    
    @staticmethod
    def identify_risks(financials: dict) -> list:
        """
        Identify key risks based on financial metrics
        MBA Finance: Risk Management Framework
        """
        risks = []
        
        if financials.get('debt_equity', 0) > 1.0:
            risks.append("High leverage - Elevated refinancing and default risk")
        
        if financials.get('net_margin', 0) < 5:
            risks.append("Weak margins - Limited pricing power or cost pressures")
        
        if financials.get('roe', 0) < 10:
            risks.append("Low ROE - Inefficient capital deployment")
        
        if financials.get('operating_margin', 0) < 10:
            risks.append("Low operating efficiency - Operational leverage challenges")
        
        return risks if risks else ["No significant financial risks identified"]
    
    @staticmethod
    def identify_strengths(financials: dict) -> list:
        """
        Identify key strengths based on financial metrics
        """
        strengths = []
        
        if financials.get('net_margin', 0) >= 12:
            strengths.append("Excellent profitability with strong cost control")
        
        if financials.get('roe', 0) >= 18:
            strengths.append("Best-in-class capital efficiency")
        
        if financials.get('operating_margin', 0) >= 20:
            strengths.append("Strong operational leverage and scalability")
        
        if financials.get('debt_equity', 0) <= 0.3:
            strengths.append("Conservative balance sheet with financial flexibility")
        
        return strengths if strengths else ["Stable financial performance"]
