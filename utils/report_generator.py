"""
Report Generator - Format and structure the Equity Research Desk Note
"""
from datetime import datetime

class ReportGenerator:
    """Generate formatted equity research desk notes"""
    
    @staticmethod
    def generate_full_report(company_name: str, sector: str, generated_content: dict,
                           financials: dict, trends: dict, investment_view: dict) -> str:
        """
        Generate complete formatted desk note
        
        Parameters:
        - company_name: Name of the company
        - sector: Sector classification
        - generated_content: AI-generated text sections
        - financials: Financial metrics
        - trends: Growth trends
        - investment_view: Investment recommendation
        
        Returns:
        - Formatted desk note string
        """
        
        report = ""
        
        # Header
        report += ReportGenerator._generate_header(company_name, sector)
        report += "\n" + "="*80 + "\n"
        
        # Executive Summary
        report += "\n📊 EXECUTIVE SUMMARY\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('executive_summary', 'N/A') + "\n"
        
        # Investment View Box
        report += "\n" + ReportGenerator._generate_investment_box(investment_view)
        
        # Company Overview
        report += "\n\n1. COMPANY OVERVIEW\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('company_overview', 'N/A') + "\n"
        
        # Business Model & Competitive Position
        report += "\n\n2. BUSINESS MODEL & COMPETITIVE POSITION\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('business_model', 'N/A') + "\n"
        
        # Financial Performance
        report += "\n\n3. FINANCIAL PERFORMANCE SNAPSHOT\n"
        report += "-" * 80 + "\n"
        report += ReportGenerator._generate_financial_snapshot(financials, trends)
        
        # Financial Commentary
        report += "\n\n4. FINANCIAL ANALYSIS\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('financial_commentary', 'N/A') + "\n"
        
        # Key Positives
        report += "\n\n5. KEY POSITIVES\n"
        report += "-" * 80 + "\n"
        report += ReportGenerator._format_list(investment_view.get('strengths', []))
        
        # Key Risks
        report += "\n\n6. KEY RISKS & CONCERNS\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('risk_analysis', 'N/A') + "\n"
        report += "\nGFInancial Risk Indicators:\n"
        report += ReportGenerator._format_list(investment_view.get('risks', []))
        
        # Investment Thesis
        report += "\n\n7. INVESTMENT THESIS\n"
        report += "-" * 80 + "\n"
        report += generated_content.get('investment_thesis', 'N/A') + "\n"
        
        # Valuation
        report += "\n\n8. VALUATION COMMENTARY\n"
        report += "-" * 80 + "\n"
        report += ReportGenerator._generate_valuation_section(financials, sector)
        
        # Investment Recommendation
        report += "\n\n9. INVESTMENT VIEW & RECOMMENDATION\n"
        report += "-" * 80 + "\n"
        report += ReportGenerator._generate_recommendation_section(investment_view)
        
        # Monitoring Points
        report += "\n\n10. KEY MONITORING POINTS\n"
        report += "-" * 80 + "\n"
        report += ReportGenerator._generate_monitoring_points(investment_view)
        
        # Disclaimer & Footer
        report += "\n\n" + "="*80 + "\n"
        report += ReportGenerator._generate_disclaimer()
        
        return report
    
    @staticmethod
    def _generate_header(company_name: str, sector: str) -> str:
        """Generate report header"""
        today = datetime.now().strftime("%d %B %Y")
        header = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                EQUITY RESEARCH DESK NOTE - INDIA                          ║
║                                                                            ║
║  Company: {company_name:<50}
║  Sector: {sector:<54}
║  Report Date: {today:<49}
║                                                                            ║
║  *** FOR ACADEMIC AND LEARNING PURPOSES ONLY ***                          ║
║  *** NOT A SUBSTITUTE FOR PROFESSIONAL FINANCIAL ADVICE ***               ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
        return header
    
    @staticmethod
    def _generate_investment_box(investment_view: dict) -> str:
        """Generate investment recommendation box"""
        view = investment_view.get('view', 'N/A')
        rationale = investment_view.get('rationale', 'N/A')
        
        box = f"""
┌────────────────────────────────────────────────────────────────────┐
│ INVESTMENT RECOMMENDATION                                          │
├────────────────────────────────────────────────────────────────────┤
│ VIEW: {view:<58}
│                                                                    │
│ RATIONALE: {rationale:<51}
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
"""
        return box
    
    @staticmethod
    def _generate_financial_snapshot(financials: dict, trends: dict) -> str:
        """Generate financial snapshot table"""
        
        snapshot = """
LATEST YEAR METRICS:
┌─────────────────────────────────────┬──────────────┐
│ Metric                              │ Value        │
├─────────────────────────────────────┼──────────────┤
"""
        
        metrics = [
            ("Net Profit Margin", f"{financials.get('net_margin', 'N/A')}%"),
            ("Operating Margin", f"{financials.get('operating_margin', 'N/A')}%"),
            ("ROE (Return on Equity)", f"{financials.get('roe', 'N/A')}%"),
            ("ROA (Return on Assets)", f"{financials.get('roa', 'N/A')}%"),
            ("Debt-to-Equity Ratio", f"{financials.get('debt_equity', 'N/A')}x"),
            ("P/E Ratio", f"{financials.get('pe_ratio', 'N/A')}x"),
        ]
        
        for metric, value in metrics:
            snapshot += f"│ {metric:<36} │ {str(value):>11} │\n"
        
        snapshot += "└─────────────────────────────────────┴──────────────┘\n\n"
        
        snapshot += "GROWTH TRENDS (YoY):\n"
        snapshot += "┌─────────────────────────────────────┬──────────────┐\n"
        snapshot += "│ Metric                              │ Growth %     │\n"
        snapshot += "├─────────────────────────────────────┼──────────────┤\n"
        
        growth_metrics = [
            ("Revenue Growth", f"{trends.get('revenue_growth', 'N/A')}%"),
            ("EBITDA Growth", f"{trends.get('ebitda_growth', 'N/A')}%"),
            ("Net Profit Growth", f"{trends.get('profit_growth', 'N/A')}%"),
        ]
        
        for metric, value in growth_metrics:
            snapshot += f"│ {metric:<36} │ {str(value):>11} │\n"
        
        snapshot += "└─────────────────────────────────────┴──────────────┘\n"
        
        return snapshot
    
    @staticmethod
    def _generate_valuation_section(financials: dict, sector: str) -> str:
        """Generate valuation commentary"""
        
        pe = financials.get('pe_ratio', 'N/A')
        market_cap = financials.get('market_cap', 'N/A')
        
        section = f"""
Current Valuation Metrics:
• P/E Ratio: {pe}x
• Market Capitalization: ₹{market_cap:,} Cr (if applicable)
• Sector: {sector}

Valuation Assessment:
The current valuation should be evaluated in context of:
- Company's earnings growth trajectory
- Sector average P/E multiples and cyclicality
- Return on equity relative to cost of capital
- Competitive positioning and market share trends

*** Note: This analysis is based on historical data ***
*** Live market prices and real-time valuations not included ***
"""
        return section
    
    @staticmethod
    def _generate_recommendation_section(investment_view: dict) -> str:
        """Generate recommendation section"""
        
        view = investment_view.get('view', 'N/A')
        factors = investment_view.get('key_factors', [])
        confidence = investment_view.get('confidence_score', 0)
        
        section = f"""
RECOMMENDATION: {view}

Key Supporting Factors:
"""
        section += ReportGenerator._format_list(factors)
        
        section += f"\n\nAnalysis Confidence Score: {confidence}/10\n"
        
        return section
    
    @staticmethod
    def _generate_monitoring_points(investment_view: dict) -> str:
        """Generate key monitoring points"""
        
        monitoring_points = [
            "Quarterly revenue and margin trends",
            "Return on equity (ROE) trajectory",
            "Debt-to-equity ratio and leverage management",
            "Market share movements in key segments",
            "Competitive positioning relative to peers",
            "Macroeconomic factors relevant to the sector",
            "Management commentary on guidance and outlook",
        ]
        
        return ReportGenerator._format_list(monitoring_points)
    
    @staticmethod
    def _format_list(items: list) -> str:
        """Format list items with bullets"""
        formatted = ""
        for item in items:
            formatted += f"• {item}\n"
        return formatted
    
    @staticmethod
    def _generate_disclaimer() -> str:
        """Generate disclaimer footer"""
        
        disclaimer = """IMPORTANT DISCLAIMER AND DISCLAIMER

════════════════════════════════════════════════════════════════════════════════

This Equity Research Desk Note is generated using AI for EDUCATIONAL AND 
LEARNING PURPOSES ONLY. It is designed to demonstrate:

✓ MBA Finance Concepts (Fundamental Analysis, Ratio Analysis, Valuation)
✓ Equity Research Methodology
✓ Financial Statement Interpretation
✓ Investment Thesis Development

⚠️  DISCLAIMERS:

1. NOT PROFESSIONAL FINANCIAL ADVICE
   - This is not a substitute for professional financial advice from qualified
     advisors, brokers, or financial consultants.

2. NO REAL-TIME DATA
   - Financial data used is sample data for educational purposes.
   - No live market data, stock prices, or real-time information included.
   - All valuations and recommendations are illustrative only.

3. LIMITATIONS
   - AI-generated content may contain inaccuracies or oversimplifications.
   - Complex financial situations require professional analysis.
   - Past performance does not guarantee future results.

4. NOT INVESTMENT SOLICITATION
   - This is not a solicitation to buy, sell, or hold any security.
   - Investment decisions should be based on comprehensive analysis and personal
     financial circumstances.

5. REGULATORY COMPLIANCE
   - Users in regulated jurisdictions should consult with licensed financial
     advisors before making investment decisions.

════════════════════════════════════════════════════════════════════════════════
Generated by: AI Investment Desk Note Generator - India
Purpose: Educational Tool for MBA Finance Learning
Status: Sample/Demo Report
════════════════════════════════════════════════════════════════════════════════
"""
        return disclaimer
