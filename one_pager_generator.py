from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

def generate_project_one_pager():
    """Generates a beautiful executive one-pager PDF for Yendoukoa AI and returns bytes."""
    buffer = io.BytesIO()

    # Page size is letter: 612 x 792 points. Margins of 0.5 inches (36 pt)
    # Printable width: 540 pt. Printable height: 720 pt.
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor('#1E3A8A')  # Dark Blue
    c_secondary = colors.HexColor('#3B82F6')  # Electric Blue
    c_text_dark = colors.HexColor('#1F2937')  # Off-black
    c_text_muted = colors.HexColor('#4B5563')  # Slate grey
    c_bg_light = colors.HexColor('#F3F4F6')  # Light grey
    c_bg_blue_tint = colors.HexColor('#EFF6FF')  # Light blue

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        alignment=1, # Center
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#93C5FD'),
        alignment=1, # Center
    )

    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.white,
        spaceAfter=0
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=c_text_dark,
    )

    body_bold_style = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    card_header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=c_primary,
        alignment=1
    )

    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text_muted,
        alignment=1
    )

    story = []

    # 1. Header Banner Table
    header_content = [
        [Paragraph("YENDOUKOA AI", title_style)],
        [Paragraph("The All-in-One Autonomous AI Ecosystem for Developers, SMEs & Governments", subtitle_style)]
    ]
    header_table = Table(header_content, colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 16),
        ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ('BOTTOMMARGIN', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Helper to wrap text with a solid header
    def create_section_header(title_text):
        hdr = Table([[Paragraph(title_text.upper(), section_title_style)]], colWidths=[540])
        hdr.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), c_secondary),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return hdr

    # 2. Executive Summary
    story.append(create_section_header("Executive Summary & Core Architecture"))
    story.append(Spacer(1, 4))

    exec_summary_text = (
        "<b>Yendoukoa AI</b> is a state-of-the-art decentralized AI platform featuring specialized autonomous agents "
        "tailored for high-compute engineering, compliance, security, and strategic tasks. Built on a unique split architecture, "
        "Yendoukoa AI utilizes a static React marketplace frontend optimized for rapid client performance and hosted on GitHub Pages, "
        "powering transactions via a separate, highly scalable Flask API gateway. Users can leverage <b>Multi-Model Intelligence</b>, "
        "accessing world-class systems like Gemini 1.5 Pro, GPT-4o, Anthropic Claude 3.5 Sonnet, Llama 3.1 405B, and NVIDIA Nemotron "
        "seamlessly through a single integrated interface."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 8))

    # 3. Market Demand TAM SAM SOM
    story.append(create_section_header("Market Analysis & Strategy (TAM, SAM, SOM)"))
    story.append(Spacer(1, 4))

    market_cards = [
        [
            Paragraph("TAM (Total Addressable)<br/><font size=11 color='#1E3A8A'><b>$500 Billion+</b></font>", card_header_style),
            Paragraph("SAM (Serviceable Addressable)<br/><font size=11 color='#1E3A8A'><b>$50 Billion</b></font>", card_header_style),
            Paragraph("SOM (Serviceable Obtainable)<br/><font size=11 color='#1E3A8A'><b>500,000 Active Users</b></font>", card_header_style)
        ],
        [
            Paragraph("The global AI software and automated services industry, scaling aggressively to meet worldwide demand by 2030.", card_body_style),
            Paragraph("Focused directly on specialized AI agent development, enterprise workflows, and regional FinTech markets.", card_body_style),
            Paragraph("Immediate capture via developer tools, local USSD banking ecosystems, and SME business management integration.", card_body_style)
        ]
    ]
    market_table = Table(market_cards, colWidths=[180, 180, 180])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_bg_light),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#D1D5DB')),
    ]))
    story.append(market_table)
    story.append(Spacer(1, 8))

    # 4. Monetization Tiers
    story.append(create_section_header("Tiered Monetization & Business Model"))
    story.append(Spacer(1, 4))

    monetization_text = (
        "Our sustainable financial strategy is built on three robust monetization pillars:<br/>"
        "• <b>SaaS Subscription Plans:</b> Powered by Stripe, offering a <b>Free Tier</b> with basic allowance, a <b>Premium Tier</b> "
        "with access to Claude 3.5 & GPT-4o, and a <b>Pro Tier</b> featuring elite workflows, developer APIs, and Gumloop/n8n integration.<br/>"
        "• <b>Pay-Per-Use Credit System:</b> Transparent credit deductions for compute-heavy tasks (such as AI code debugging or deep space analysis). Users can top-up credit packs directly via local credit cards, Paystack, or Flutterwave (V3). Developers earn 80% of execution revenues.<br/>"
        "• <b>USSD & Mobile Financial Networks:</b> Low-tech mobile money ecosystems optimized for Francophone Africa, integrating smart contracts, USSD blockchain gateways, and advanced real-time transaction scam detectors."
    )
    story.append(Paragraph(monetization_text, body_style))
    story.append(Spacer(1, 8))

    # 5. Flagship Specialists
    story.append(create_section_header("Specialized Flagship AI Service Roles"))
    story.append(Spacer(1, 4))

    roles_text = (
        "• <b>AWS Cloud & Security Architect:</b> Configures secure web hosting, Cloud server creation, DNS, and SaaS billing setups.<br/>"
        "• <b>Quantum AI Specialist (IA Quantique):</b> QML, quantum neural networks, combinatorics, and post-quantum cryptography.<br/>"
        "• <b>Cybersecurity Sentinel & Malware Defender:</b> Automated pen-testing, malware signature scanning, and kernel hardening.<br/>"
        "• <b>Affiliate & MLM Specialist:</b> Structuring attribution tracking, downline compensation plans, and FTC compliance audits.<br/>"
        "• <b>Founder Data Room & Investor Assistant:</b> Automated index building, safe notes drafting, and due diligence compilation (.docx).<br/>"
        "• <b>Video Producer & Cinematic Strategist:</b> Full scriptwriting with audio/visual cues, scene pacing, and YouTube optimization."
    )
    story.append(Paragraph(roles_text, body_style))
    story.append(Spacer(1, 8))

    # 6. Global Sponsorships & PSF Direct Support
    story.append(create_section_header("Ecosystem Sustainability & PSF Contribution"))
    story.append(Spacer(1, 4))

    sponsorship_text = (
        "Yendoukoa AI operates with high transparency and is backed by multi-channel global crowdfunding through GitHub Sponsors, "
        "Open Collective, and Patreon. To promote a sustainable future for autonomous intelligence, we allocate direct financial "
        "sponsorship and donations to the <b>Python Software Foundation (PSF)</b> to power PyPI, core Python updates, and global community development."
    )
    story.append(Paragraph(sponsorship_text, body_style))

    # Build the document
    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
