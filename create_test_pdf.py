"""
Create Test PDF
Generates a realistic test pitch deck PDF with founder experience details
For testing the Pitch Deck Analyzer API
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, grey
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path

def create_test_pitch_deck():
    """
    Create a realistic test pitch deck PDF with founder experience.
    Includes all sections needed for analysis.
    """
    
    # File configuration
    pdf_path = "test_pitch_deck.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#1f4788'),
        spaceAfter=12,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=8,
        alignment=4  # Justify
    )
    
    # Story for PDF
    story = []
    
    # ===== PAGE 1: COVER SLIDE =====
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("TechAI Analytics Inc", title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("AI-Powered Business Intelligence Platform", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    # Company info table
    company_info = [
        ["Industry:", "AI/ML & Analytics"],
        ["Founded:", "2023"],
        ["Location:", "San Francisco, CA"],
        ["Status:", "Series A"],
    ]
    
    company_table = Table(company_info, colWidths=[1.5*inch, 3.5*inch])
    company_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1f4788')),
        ('TEXTCOLOR', (1, 0), (1, -1), black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f0f0f0'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(company_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Founders section
    story.append(Paragraph("Founding Team", heading_style))
    
    founders_info = [
        ["Name", "Role", "Background", "Experience"],
        ["Sarah Chen", "Founder/CEO", "Stanford (BS CS)", "8 years @ Google, 3 years @ Airbnb"],
        ["Michael Park", "Founder/CTO", "MIT (BS CS)", "7 years @ Meta, 2 years @ OpenAI"],
        ["Emily Watson", "Founder/COO", "Harvard (MBA)", "5 years @ McKinsey, VP Stripe"],
    ]
    
    founders_table = Table(founders_info, colWidths=[1.3*inch, 1.2*inch, 1.5*inch, 1.5*inch])
    founders_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f9f9f9'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(founders_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Key metrics
    story.append(Paragraph("Team Composition", heading_style))
    team_metrics = [
        ["Total Founders:", "3"],
        ["Average Experience:", "7.3 years"],
        ["Top School Graduates:", "3/3 (100%)"],
        ["FAANG Background:", "3/3 (100%)"],
        ["Technical Co-founders:", "2/3"],
        ["Previous Startup Experience:", "Yes"],
    ]
    
    team_table = Table(team_metrics, colWidths=[2.5*inch, 2.5*inch])
    team_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1f4788')),
        ('TEXTCOLOR', (1, 0), (1, -1), black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#f5f5f5'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dddddd')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(team_table)
    story.append(PageBreak())
    
    # ===== PAGE 2: BUSINESS DETAILS =====
    story.append(Paragraph("The Problem", heading_style))
    story.append(Paragraph(
        "Current analytics tools are expensive ($10,000+/month), require deep technical knowledge, "
        "and take weeks to implement. Business teams waste 40% of their time on manual data processing "
        "and report generation instead of strategic decision-making. The global analytics software market "
        "is worth $50 billion and growing at 15% annually.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Our Solution", heading_style))
    story.append(Paragraph(
        "TechAI Analytics is an AI-powered platform that makes enterprise analytics accessible to everyone. "
        "Our natural language interface allows non-technical business users to ask questions in plain English "
        "and get instant insights. We combine cutting-edge AI/ML with intuitive design to reduce implementation "
        "time from weeks to hours, and cost from $10,000/month to $500/month.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("Market Opportunity", heading_style))
    market_data = [
        ["Market Segment", "TAM", "Growth Rate"],
        ["Enterprise Analytics", "$30B", "12% CAGR"],
        ["Mid-Market Analytics", "$15B", "18% CAGR"],
        ["SMB Analytics", "$5B", "25% CAGR"],
        ["Total Addressable Market", "$50B", "15% CAGR"],
    ]
    
    market_table = Table(market_data, colWidths=[1.8*inch, 1.6*inch, 1.8*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f0f0f0'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(market_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Traction & Metrics", heading_style))
    traction_data = [
        ["Metric", "Current", "Target (12 months)"],
        ["Active Customers", "45", "500+"],
        ["Monthly Recurring Revenue", "$85,000", "$1,500,000"],
        ["Customer Acquisition Cost", "$3,200", "$2,500"],
        ["Customer Lifetime Value", "$48,000", "$150,000"],
        ["Net Retention Rate", "125%", "140%"],
        ["Team Size", "12", "35"],
    ]
    
    traction_table = Table(traction_data, colWidths=[1.8*inch, 1.6*inch, 1.8*inch])
    traction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f0f0f0'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(traction_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Business Model", heading_style))
    story.append(Paragraph(
        "<b>SaaS Subscription Model:</b> Tiered pricing based on data volume and team size. "
        "Starter plan at $500/month for SMBs, Professional at $2,500/month for mid-market, "
        "Enterprise custom pricing. 90% of revenue from recurring subscriptions with growing "
        "professional services revenue.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Use of Funds", heading_style))
    funds_data = [
        ["Category", "Allocation", "Details"],
        ["Product Development", "40%", "AI/ML engineers, platform development"],
        ["Sales & Marketing", "35%", "Sales team, customer acquisition"],
        ["Operations", "15%", "Infrastructure, administrative"],
        ["Team Expansion", "10%", "Support, finance, HR"],
    ]
    
    funds_table = Table(funds_data, colWidths=[1.8*inch, 1.5*inch, 1.9*inch])
    funds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f0f0f0'), white]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(funds_table)
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        "We are raising <b>$5M Series A</b> to accelerate product development, build our sales team, "
        "and expand into new markets. Our goal is to reach $10M ARR within 18 months and position "
        "TechAI Analytics as the leading AI-powered analytics platform for mid-market enterprises.",
        normal_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Contact", heading_style))
    story.append(Paragraph(
        "<b>Sarah Chen</b><br/>CEO, TechAI Analytics<br/>"
        "Email: sarah@techaianalytics.com<br/>"
        "Phone: +1 (415) 555-0123",
        normal_style
    ))
    
    # Build PDF
    doc.build(story)
    
    print("✓ Test PDF created successfully!")
    print(f"  File: {pdf_path}")
    print(f"  Size: {Path(pdf_path).stat().st_size / 1024:.1f} KB")
    print(f"\n✓ PDF includes:")
    print(f"  - Founder information (names, roles, backgrounds, experience)")
    print(f"  - Previous companies (Google, Meta, McKinsey, Airbnb, OpenAI, Stripe)")
    print(f"  - Education details (Stanford, MIT, Harvard)")
    print(f"  - Company details (problem, solution, market, traction)")
    print(f"  - Business metrics (revenue, growth, team size)")
    print(f"  - Use of funds and funding ask")

if __name__ == "__main__":
    create_test_pitch_deck()