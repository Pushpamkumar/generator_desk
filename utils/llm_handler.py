"""
LLM Integration Handler - Google Gemini API (Free Tier)
Generates professional equity research content using AI
"""
import os
import json
from typing import Optional
import google.generativeai as genai

class LLMHandler:
    """Handle LLM API calls for desk note generation using Google Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Google Gemini client"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_company_overview(self, company_name: str, sector: str) -> str:
        """Generate company overview section"""
        prompt = f"""Generate a professional 100-150 word company overview for {company_name} 
        in the {sector} sector, suitable for an equity research desk note.
        
        Focus on:
        - Company's core business and history
        - Market position in Indian market
        - Key products/services
        
        Keep it factual and professional. Do not make up specific numbers."""
        
        return self._call_api(prompt)
    
    def generate_business_model(self, company_name: str, sector: str) -> str:
        """Generate business model and competitive position analysis"""
        prompt = f"""Analyze the business model and competitive position for {company_name} 
        ({sector} sector) in India.
        
        Include:
        - Revenue model and main business segments
        - Competitive advantages/moat
        - Industry cyclicality if applicable
        - Market dynamics in {sector.lower()} sector
        
        Keep to 150-200 words. Be professional and avoid speculation."""
        
        return self._call_api(prompt)
    
    def generate_financial_commentary(self, company_name: str, financials: dict, 
                                     trends: dict) -> str:
        """Generate financial performance commentary"""
        
        metrics_text = self._format_metrics_for_llm(financials, trends)
        
        prompt = f"""Based on these financial metrics for {company_name}, 
provide a professional 150-200 word analysis:

{metrics_text}

Discuss:
- Revenue and profit trends
- Profitability metrics (margins)
- Capital efficiency (ROE/ROA)
- Balance sheet strength (Debt-Equity ratio)
- Valuation reasonableness given the sector

Use MBA finance terminology. No specific price targets."""
        
        return self._call_api(prompt)
    
    def generate_investment_thesis(self, company_name: str, strengths: list, 
                                  risks: list, valuation: str) -> str:
        """Generate investment thesis"""
        
        strengths_text = ", ".join(strengths[:3])
        risks_text = ", ".join(risks[:3])
        
        prompt = f"""Create a concise investment thesis for {company_name} (100-150 words).

Key Strengths: {strengths_text}
Key Risks: {risks_text}
Valuation Assessment: {valuation}

Structure:
- Bull case (why investors should own this stock)
- Bear case (key risks to monitor)
- Overall investment merit

Professional tone, MBA finance framework."""
        
        return self._call_api(prompt)
    
    def generate_risk_analysis(self, company_name: str, risks: list) -> str:
        """Generate detailed risk analysis"""
        
        risks_text = "\n".join([f"- {risk}" for risk in risks])
        
        prompt = f"""Write a risk analysis for {company_name} (100-150 words).

Identified Financial Risks:
{risks_text}

Address:
- Severity of each risk
- Time horizon for risk materialization
- Mitigation options (if any)
- What to monitor

Professional, balanced perspective."""
        
        return self._call_api(prompt)
    
    def generate_desk_note_executive_summary(self, company_name: str, sector: str, 
                                            view: str, rationale: str) -> str:
        """Generate executive summary for the desk note"""
        
        prompt = f"""Create a 100-word executive summary for an equity research desk note on {company_name}.

Investment View: {view}
Rationale: {rationale}
Sector: {sector}

Include:
- One-line thesis
- Key reasons to own/avoid
- Price target horizon (qualitative only)

Professional, punchy, MBA-level quality."""
        
        return self._call_api(prompt)
    
    def _call_api(self, prompt: str) -> str:
        """Call Google Gemini API with given prompt"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    @staticmethod
    def _format_metrics_for_llm(financials: dict, trends: dict) -> str:
        """Format financial metrics into readable text for LLM"""
        
        text = f"""Financial Metrics (Latest Year):
- Net Profit Margin: {financials.get('net_margin', 'N/A')}%
- Operating Margin: {financials.get('operating_margin', 'N/A')}%
- ROE (Return on Equity): {financials.get('roe', 'N/A')}%
- ROA (Return on Assets): {financials.get('roa', 'N/A')}%
- Debt-Equity Ratio: {financials.get('debt_equity', 'N/A')}
- P/E Ratio: {financials.get('pe_ratio', 'N/A')}x

Growth Trends:
- Revenue Growth: {trends.get('revenue_growth', 'N/A')}% YoY
- EBITDA Growth: {trends.get('ebitda_growth', 'N/A')}% YoY
- Net Profit Growth: {trends.get('profit_growth', 'N/A')}% YoY
"""
        return text
