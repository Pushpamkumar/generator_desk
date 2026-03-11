"""
Main Streamlit Application
AI Investment Desk Note Generator - India
Professional Equity Research Tool with MBA Finance Framework
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from io import BytesIO

# Import custom modules
from utils.financial_calculator import FinancialCalculator
from utils.llm_handler import LLMHandler
from utils.report_generator import ReportGenerator
from utils.pdf_exporter import PDFExporter

# Page configuration
st.set_page_config(
    page_title="AI Investment Desk Note Generator - India",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .header-title {
        color: #003366;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .subheader {
        color: #666666;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .recommendation-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid;
    }
    .buy-box {
        border-left-color: #28a745;
        background-color: #f0f8f5;
    }
    .hold-box {
        border-left-color: #ffc107;
        background-color: #fff8f0;
    }
    .sell-box {
        border-left-color: #dc3545;
        background-color: #fef0f0;
    }
    .disclaimer {
        background-color: #fff3cd;
        border: 1px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'report_content' not in st.session_state:
    st.session_state.report_content = None

# Header
st.markdown('<div class="header-title">📊 AI Investment Desk Note Generator</div>', 
           unsafe_allow_html=True)
st.markdown('<div class="subheader">Professional Equity Research for Indian Listed Companies (NSE/BSE)</div>', 
           unsafe_allow_html=True)

# Important Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ IMPORTANT DISCLAIMER:</strong><br>
    This tool is for EDUCATIONAL AND LEARNING PURPOSES ONLY. It demonstrates MBA Finance concepts 
    through AI-generated equity research. This is NOT professional financial advice and NOT a substitute 
    for advice from qualified financial advisors. All data may be sample/demo data. Not investment solicitation.
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # API Key Section
    st.subheader("LLM Configuration")
    api_key = st.text_input(
        "Enter Google Gemini API Key",
        type="password",
        help="Get your FREE API key from https://ai.google.dev/"
    )
    
    st.divider()
    
    # Tool Selection
    st.subheader("Tool Mode")
    tool_mode = st.radio(
        "Choose Analysis Mode",
        ["Quick Sample Analysis", "Upload Financial Data"],
        help="Quick mode uses sample data. Upload mode allows CSV/Excel upload."
    )
    
    st.divider()
    
    # Company Database Info
    st.subheader("Available Companies (Sample Data)")
    st.info("""
    Sample Dataset Includes:
    • Tata Motors
    • Reliance Industries
    • Infosys Limited
    • HDFC Bank
    • Sun Pharmaceutical
    • ITC Limited
    """)

# Main Content Area
tab1, tab2, tab3 = st.tabs(["📈 Generate Desk Note", "📊 Data Explorer", "ℹ️ About"])

with tab1:
    st.header("Generate Equity Research Desk Note")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Company input
        company_name = st.text_input(
            "Enter Company Name",
            placeholder="e.g., Tata Motors, Reliance Industries, Infosys",
            help="Select from available companies or enter a company name"
        )
    
    with col2:
        # Sector selection
        sector_options = [
            "Select Sector",
            "IT",
            "Banking",
            "Pharma",
            "Auto",
            "FMCG",
            "Energy"
        ]
        sector = st.selectbox(
            "Sector",
            sector_options,
            help="Select the company's sector for better analysis"
        )
    
    st.divider()
    
    # Financial Data Input
    st.subheader("Financial Data Input", help="Provide financial data for analysis")
    
    data_source = st.radio(
        "Data Source",
        ["Use Sample Data", "Upload CSV/Excel"],
        horizontal=True
    )
    
    user_financials = None
    
    if data_source == "Use Sample Data":
        try:
            sample_data = pd.read_csv("data/sample_financials.csv")
            if company_name and company_name in sample_data['Company'].values:
                user_financials = sample_data[sample_data['Company'] == company_name]
                st.success(f"✓ Sample data loaded for {company_name}")
            else:
                st.info("Sample data available. Select a company to proceed.")
        except FileNotFoundError:
            st.warning("Sample data file not found. Using manual entry mode.")
    
    else:  # Upload CSV/Excel
        uploaded_file = st.file_uploader(
            "Upload Financial Data (CSV/Excel)",
            type=["csv", "xlsx"],
            help="Upload a file with columns: Year, Revenue_Cr, EBITDA_Cr, Net_Profit_Cr, etc."
        )
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    user_financials = pd.read_csv(uploaded_file)
                else:
                    user_financials = pd.read_excel(uploaded_file)
                st.success("✓ File uploaded successfully")
                st.dataframe(user_financials, use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    st.divider()
    
    # Generate Button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(
            "🚀 Generate Desk Note",
            use_container_width=True,
            key="generate_btn"
        ):
            if not company_name:
                st.error("❌ Please enter a company name")
            elif sector == "Select Sector":
                st.error("❌ Please select a sector")
            elif user_financials is None or len(user_financials) == 0:
                st.error("❌ Please provide financial data")
            elif not api_key:
                st.error("❌ Please enter your Anthropic API key in the sidebar")
            else:
                # Generate desk note
                st.info("Generating desk note... This may take a moment.")
                
                try:
                    # Initialize LLM handler
                    llm = LLMHandler(api_key=api_key)
                    
                    # Extract latest financial data
                    latest_data = user_financials.iloc[-1]
                    prev_data = user_financials.iloc[-2] if len(user_financials) > 1 else latest_data
                    
                    # Prepare financial metrics
                    financials = {
                        'net_margin': float(latest_data.get('Net_Margin_%', 0)),
                        'operating_margin': float(latest_data.get('Operating_Margin_%', 0)),
                        'roe': float(latest_data.get('ROE_%', 0)),
                        'roa': float(latest_data.get('ROA_%', 0)),
                        'debt_equity': float(latest_data.get('Debt_Equity_Ratio', 0)),
                        'pe_ratio': float(latest_data.get('PE_Ratio', 0)),
                        'market_cap': latest_data.get('Market_Cap_Cr', 0)
                    }
                    
                    # Calculate growth trends
                    revenue_growth = ((latest_data.get('Revenue_Cr', 0) - prev_data.get('Revenue_Cr', 0)) / 
                                    prev_data.get('Revenue_Cr', 1) * 100)
                    ebitda_growth = ((latest_data.get('EBITDA_Cr', 0) - prev_data.get('EBITDA_Cr', 0)) / 
                                    prev_data.get('EBITDA_Cr', 1) * 100)
                    profit_growth = ((latest_data.get('Net_Profit_Cr', 0) - prev_data.get('Net_Profit_Cr', 0)) / 
                                    prev_data.get('Net_Profit_Cr', 1) * 100)
                    
                    trends = {
                        'revenue_growth': round(revenue_growth, 2),
                        'ebitda_growth': round(ebitda_growth, 2),
                        'profit_growth': round(profit_growth, 2)
                    }
                    
                    # Get financial assessments
                    strengths = FinancialCalculator.identify_strengths(financials)
                    risks = FinancialCalculator.identify_risks(financials)
                    
                    # Generate investment view
                    valuation_signal = FinancialCalculator.evaluate_valuation(
                        financials.get('pe_ratio', 0), sector
                    )
                    
                    investment_view = FinancialCalculator.generate_investment_view(
                        financials, trends, {'pe_signal': 'Attractive' if 'Attractive' in valuation_signal else 'Fair'}
                    )
                    investment_view['strengths'] = strengths
                    investment_view['risks'] = risks
                    
                    # Generate AI content
                    progress_placeholder = st.empty()
                    
                    progress_placeholder.info("🤖 Generating company overview...")
                    executive_summary = llm.generate_desk_note_executive_summary(
                        company_name, sector, investment_view['view'], investment_view['rationale']
                    )
                    
                    progress_placeholder.info("🤖 Generating business model analysis...")
                    company_overview = llm.generate_company_overview(company_name, sector)
                    
                    progress_placeholder.info("🤖 Analyzing business model...")
                    business_model = llm.generate_business_model(company_name, sector)
                    
                    progress_placeholder.info("🤖 Analyzing financial metrics...")
                    financial_commentary = llm.generate_financial_commentary(
                        company_name, financials, trends
                    )
                    
                    progress_placeholder.info("🤖 Assessing investment thesis...")
                    investment_thesis = llm.generate_investment_thesis(
                        company_name, strengths, risks, valuation_signal
                    )
                    
                    progress_placeholder.info("🤖 Analyzing risks...")
                    risk_analysis = llm.generate_risk_analysis(company_name, risks)
                    
                    progress_placeholder.empty()
                    
                    # Generate full report
                    generated_content = {
                        'executive_summary': executive_summary,
                        'company_overview': company_overview,
                        'business_model': business_model,
                        'financial_commentary': financial_commentary,
                        'investment_thesis': investment_thesis,
                        'risk_analysis': risk_analysis
                    }
                    
                    report = ReportGenerator.generate_full_report(
                        company_name, sector, generated_content, financials, trends, investment_view
                    )
                    
                    # Store in session state
                    st.session_state.report_generated = True
                    st.session_state.report_content = report
                    st.session_state.company_name = company_name
                    st.session_state.financials = financials
                    st.session_state.trends = trends
                    st.session_state.investment_view = investment_view
                    
                    st.success("✅ Desk note generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating desk note: {str(e)}")
                    st.info("Please check your API key and try again.")
    
    # Display generated report
    if st.session_state.report_generated and st.session_state.report_content:
        st.divider()
        st.header("📋 Generated Desk Note")
        
        # Investment Recommendation Box
        inv_view = st.session_state.investment_view
        view_color = {
            'BUY': 'buy-box',
            'HOLD': 'hold-box',
            'SELL': 'sell-box'
        }
        
        box_class = view_color.get(inv_view['view'], 'hold-box')
        
        st.markdown(f"""
        <div class="recommendation-box {box_class}">
            <h3>Investment Recommendation: {inv_view['view']}</h3>
            <p><strong>Rationale:</strong> {inv_view['rationale']}</p>
            <p><strong>Key Factors:</strong><br>
            {''.join([f'• {factor}<br>' for factor in inv_view.get('key_factors', [])])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Financial Charts
        st.subheader("Financial Performance Visualization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue and Profit Chart
            if len(user_financials) > 0:
                fig_rev = go.Figure()
                fig_rev.add_trace(go.Scatter(
                    x=user_financials['Year'],
                    y=user_financials['Revenue_Cr'],
                    mode='lines+markers',
                    name='Revenue (₹ Cr)',
                    line=dict(color='#003366', width=3),
                    marker=dict(size=8)
                ))
                fig_rev.update_layout(
                    title="Revenue Trend",
                    xaxis_title="Year",
                    yaxis_title="Revenue (₹ Cr)",
                    hovermode='x unified',
                    template='plotly_white'
                )
                st.plotly_chart(fig_rev, use_container_width=True)
        
        with col2:
            # Profit Chart
            if len(user_financials) > 0:
                fig_profit = go.Figure()
                fig_profit.add_trace(go.Scatter(
                    x=user_financials['Year'],
                    y=user_financials['Net_Profit_Cr'],
                    mode='lines+markers',
                    name='Net Profit (₹ Cr)',
                    line=dict(color='#28a745', width=3),
                    marker=dict(size=8)
                ))
                fig_profit.update_layout(
                    title="Net Profit Trend",
                    xaxis_title="Year",
                    yaxis_title="Net Profit (₹ Cr)",
                    hovermode='x unified',
                    template='plotly_white'
                )
                st.plotly_chart(fig_profit, use_container_width=True)
        
        # Financial Metrics Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Net Margin %", f"{st.session_state.financials['net_margin']:.2f}%")
            st.metric("ROE %", f"{st.session_state.financials['roe']:.2f}%")
        
        with col2:
            st.metric("Operating Margin %", f"{st.session_state.financials['operating_margin']:.2f}%")
            st.metric("ROA %", f"{st.session_state.financials['roa']:.2f}%")
        
        with col3:
            st.metric("P/E Ratio", f"{st.session_state.financials['pe_ratio']:.1f}x")
            st.metric("Debt-Equity", f"{st.session_state.financials['debt_equity']:.2f}x")
        
        # Full Report Text
        st.subheader("Full Desk Note")
        
        report_text = st.session_state.report_content
        
        # Display report
        st.text_area(
            "Desk Note Content",
            value=report_text,
            height=400,
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Download options
        st.divider()
        st.subheader("Download Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download as Text
            text_export = PDFExporter.export_to_text(
                report_text,
                st.session_state.company_name
            )
            st.download_button(
                label="📄 Download as TXT",
                data=text_export,
                file_name=f"{st.session_state.company_name}_desk_note.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            # Download as PDF
            try:
                pdf_buffer = PDFExporter.export_to_pdf(
                    report_text,
                    st.session_state.company_name
                )
                if pdf_buffer:
                    st.download_button(
                        label="📕 Download as PDF",
                        data=pdf_buffer,
                        file_name=f"{st.session_state.company_name}_desk_note.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.info("PDF export requires reportlab library")
        
        with col3:
            # Download as CSV (Financials)
            csv_data = user_financials.to_csv(index=False)
            st.download_button(
                label="📊 Download Financials CSV",
                data=csv_data,
                file_name=f"{st.session_state.company_name}_financials.csv",
                mime="text/csv",
                use_container_width=True
            )

with tab2:
    st.header("📊 Data Explorer")
    
    try:
        sample_data = pd.read_csv("data/sample_financials.csv")
        
        st.subheader("Sample Financial Database")
        st.info("Explore the sample financial data used for analysis")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_company = st.selectbox(
                "Select Company",
                sorted(sample_data['Company'].unique())
            )
        
        with col2:
            selected_sector = st.selectbox(
                "Select Sector",
                sorted(sample_data['Sector'].unique())
            )
        
        with col3:
            show_all = st.checkbox("Show All Data")
        
        # Apply filters
        if show_all:
            filtered_data = sample_data
        else:
            filtered_data = sample_data[
                (sample_data['Company'] == selected_company) &
                (sample_data['Sector'] == selected_sector)
            ]
        
        # Display table
        st.dataframe(filtered_data, use_container_width=True, height=400)
        
        # Summary statistics
        st.subheader("Summary Statistics by Sector")
        sector_summary = sample_data.groupby('Sector')[
            ['Net_Margin_%', 'ROE_%', 'Debt_Equity_Ratio', 'PE_Ratio']
        ].mean()
        
        st.dataframe(sector_summary, use_container_width=True)
        
    except FileNotFoundError:
        st.warning("Sample data file not found")

with tab3:
    st.header("ℹ️ About This Tool")
    
    st.markdown("""
    ## AI Investment Desk Note Generator - India
    
    ### Purpose
    This tool demonstrates how AI can automate parts of equity research and desk note preparation 
    for Indian stock markets. It's designed as an educational tool for MBA Finance students, 
    equity research analysts, and finance professionals.
    
    ### MBA Finance Concepts Demonstrated
    
    ✅ **Fundamental Analysis**
    - Analysis of company financials and business model
    
    ✅ **Financial Ratio Analysis**
    - Net Margin, Operating Margin
    - Return on Equity (ROE) and Return on Assets (ROA)
    - Debt-Equity Ratio for capital structure analysis
    - P/E Ratio for valuation
    
    ✅ **Equity Research Methodology**
    - Company overview and industry positioning
    - Financial performance analysis
    - Risk identification and assessment
    - Investment thesis formulation
    
    ✅ **Valuation Perspective**
    - P/E multiple analysis
    - Market Capitalization context
    - Valuation relative to sector peers
    
    ✅ **Risk Analysis**
    - Financial risk identification
    - Leverage assessment
    - Efficiency metrics evaluation
    
    ### Technology Stack
    - **Frontend**: Streamlit
    - **Backend**: Python
    - **LLM Integration**: Anthropic Claude API
    - **Data Processing**: Pandas
    - **Visualization**: Plotly
    - **Export**: PDF, CSV, TXT
    
    ### Data Sources
    - Sample financial data for Indian companies
    - Data is clearly labeled as "sample/demo data"
    - No real-time market data or live prices included
    - Suitable for educational and learning purposes
    
    ### Key Features
    
    📊 **Generate Professional Desk Notes**
    - One-click generation of comprehensive equity research reports
    
    📈 **Financial Visualization**
    - Interactive charts showing revenue and profit trends
    - Key metrics dashboard
    
    💾 **Multiple Export Formats**
    - Download as PDF, TXT, or CSV
    - Share findings easily
    
    🔄 **Flexible Data Input**
    - Use sample data for quick analysis
    - Upload custom CSV/Excel files
    
    ### Report Sections
    
    1. **Company Overview** - Business summary and positioning
    2. **Business Model** - Revenue drivers and competitive advantages
    3. **Financial Performance** - Key metrics and trends
    4. **Financial Analysis** - Ratio interpretation and commentary
    5. **Key Positives** - Strengths and opportunities
    6. **Key Risks** - Financial and operational risks
    7. **Investment Thesis** - bull and bear case
    8. **Valuation** - P/E and market cap analysis
    9. **Investment View** - BUY / HOLD / SELL recommendation
    10. **Monitoring Points** - Key metrics to track
    
    ### Limitations & Disclaimers
    
    ⚠️ **Educational Purpose Only**
    - This is NOT professional financial advice
    - NOT a substitute for advice from qualified financial advisors
    - For learning and academic purposes
    
    ⚠️ **Sample Data**
    - Financial data used may be sample/demo data
    - No real-time NSE/BSE prices
    - No live market data
    
    ⚠️ **AI-Generated Content**
    - AI content may contain inaccuracies
    - Complex situations require professional analysis
    - Not investment solicitation
    
    ### Sample Companies in Database
    - Tata Motors (Auto)
    - Reliance Industries (Energy)
    - Infosys Limited (IT)
    - HDFC Bank (Banking)
    - Sun Pharmaceutical (Pharma)
    - ITC Limited (FMCG)
    
    ### How to Use
    
    1. **Select a Company** - Choose from sample database or enter a company name
    2. **Choose Sector** - Select the appropriate sector classification
    3. **Provide Financial Data** - Use sample data or upload CSV
    4. **Configure LLM** - Enter your Anthropic API key
    5. **Generate Desk Note** - Click to create report
    6. **Review & Download** - View results and export in desired format
    
    ### Contact & Support
    
    This tool is developed as a portfolio project demonstrating:
    - Full-stack development (Streamlit + Python)
    - MBA Finance concepts
    - LLM integration
    - Creating business-grade applications
    
    ---
    
    **Status**: Educational Tool | **Version**: 1.0 | **Last Updated**: 2025
    
    *For academic and learning purposes. Not investment advice.*
    """)

# Footer
st.divider()
st.markdown("""
---
<div style='text-align: center; color: #888888; font-size: 12px; margin-top: 20px;'>
    <p>AI Investment Desk Note Generator - India | Educational Tool for MBA Finance Learning</p>
    <p>⚠️ <strong>DISCLAIMER:</strong> For educational purposes only. Not professional financial advice. 
    Sample data used. Consult qualified financial advisors before making investment decisions.</p>
    <p>© 2025 | Powered by Streamlit + Claude AI</p>
</div>
""", unsafe_allow_html=True)
