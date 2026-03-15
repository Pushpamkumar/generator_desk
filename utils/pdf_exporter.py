"""
PDF Export Handler - Export desk notes as PDF
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.platypus import Preformatted
from io import BytesIO
import textwrap

class PDFExporter:
    """Export desk notes as professional PDF documents"""
    
    @staticmethod
    def export_to_pdf(report_content: str, company_name: str) -> BytesIO:
        """
        Export report to PDF
        
        Parameters:
        - report_content: Formatted report text
        - company_name: Name of the company
        
        Returns:
        - BytesIO object containing PDF
        """
        
        pdf_buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Override and create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#003366'),
            spaceAfter=8,
            spaceBefore=8,
            borderPadding=5,
            borderColor=colors.HexColor('#CCCCCC'),
            borderWidth=0.5
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#333333'),
            alignment=4  # Left alignment
        )
        
        # Add title
        title = Paragraph(
            f"Equity Research Desk Note<br/>{company_name}",
            title_style
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Split content by sections and add
        sections = report_content.split('\n\n')
        
        for section in sections:
            if section.strip():
                # Check if this is a heading (contains numbers and dots like "1. SECTION")
                if section.strip()[0].isdigit() and '.' in section[:3]:
                    heading_text = section.split('\n')[0]
                    heading = Paragraph(heading_text, heading_style)
                    elements.append(heading)
                    
                    # Add the rest of the section content
                    body_content = '\n'.join(section.split('\n')[1:]).strip()
                    if body_content:
                        # Break into smaller paragraphs if too long
                        body = Paragraph(body_content[:500], body_style)  # Truncate for performance
                        elements.append(body)
                else:
                    # Regular body content
                    if len(section.strip()) < 2000:  # Only add if not too long
                        body = Paragraph(section[:500], body_style)
                        elements.append(body)
                
                elements.append(Spacer(1, 0.1*inch))
        
        # Add disclaimer at the end
        elements.append(PageBreak())
        disclaimer_title = Paragraph("IMPORTANT DISCLAIMER", heading_style)
        elements.append(disclaimer_title)
        
        disclaimer_text = """This report is generated for EDUCATIONAL AND LEARNING PURPOSES ONLY using AI. 
        It is NOT professional financial advice and NOT a substitute for advice from qualified financial advisors. 
        All financial data is sample data for educational purposes. This is NOT investment solicitation. 
        Past performance does not guarantee future results. Users should consult licensed financial advisors before 
        making any investment decisions."""
        
        disclaimer = Paragraph(disclaimer_text, body_style)
        elements.append(disclaimer)
        
        # Build PDF
        try:
            doc.build(elements)
            pdf_buffer.seek(0)
            return pdf_buffer
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None
    
    @staticmethod
    def export_to_text(report_content: str, company_name: str) -> str:
        """
        Export report as plain text file
        
        Parameters:
        - report_content: Formatted report text
        - company_name: Name of the company
        
        Returns:
        - Text content ready for file export
        """
        
        text_output = f"""
EQUITY RESEARCH DESK NOTE - INDIA
Company: {company_name}
Generated by: AI Investment Desk Note Generator (Educational Tool)

{'='*80}

{report_content}

{'='*80}
End of Report
"""
        return text_output
