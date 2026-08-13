from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_portfolio_pdf(student_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E1B4B'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#312E81'),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1F2937')
    )

    story = []

    # Title Banner
    story.append(Paragraph("UniNet — Official Verifiable Co-Curricular Portfolio", title_style))
    story.append(Paragraph("Wayamba University of Sri Lanka · Faculty of Applied Sciences", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#6366F1'), spaceAfter=15))

    # Student Details
    name = student_data.get('name', 'Student')
    email = student_data.get('email', 'N/A')
    user_id = student_data.get('id', 'U001')
    stream = student_data.get('degreeStream', 'BSc (Hons) in Computer Science')
    batch = student_data.get('batch', 'Batch of 2022/23')
    tier = student_data.get('badgeTier', 'Gold')
    points = student_data.get('totalPoints', 530)

    user_info_data = [
        [Paragraph(f"<b>Student Name:</b> {name}", body_style), Paragraph(f"<b>Student ID:</b> {user_id}", body_style)],
        [Paragraph(f"<b>Degree Stream:</b> {stream}", body_style), Paragraph(f"<b>Batch:</b> {batch}", body_style)],
        [Paragraph(f"<b>Badge Tier:</b> {tier} Member", body_style), Paragraph(f"<b>Engagement Points:</b> {points} pts", body_style)],
        [Paragraph(f"<b>Email:</b> {email}", body_style), Paragraph("<b>Verification Status:</b> Verified ✅", body_style)],
    ]
    
    info_table = Table(user_info_data, colWidths=[260, 260])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))

    # Digital Badges
    story.append(Paragraph("🏆 Unlocked Digital Badges Catalog", section_heading))
    badges = student_data.get('badges', [])
    if badges:
        badge_rows = [[Paragraph("<b>Badge Title</b>", body_style)]]
        for b in badges:
            badge_rows.append([Paragraph(str(b), body_style)])
        badge_table = Table(badge_rows, colWidths=[520])
        badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(badge_table)
    else:
        story.append(Paragraph("No badges unlocked yet.", body_style))

    story.append(Spacer(1, 15))

    # Engagement History Table
    story.append(Paragraph("📜 Verified Co-Curricular Engagement History", section_heading))
    activities = student_data.get('activities', [])
    if activities:
        act_headers = [
            Paragraph("<b>Role / Designation</b>", body_style),
            Paragraph("<b>Organization</b>", body_style),
            Paragraph("<b>Event / Activity</b>", body_style),
            Paragraph("<b>Category</b>", body_style),
            Paragraph("<b>Period</b>", body_style),
        ]
        act_rows = [act_headers]
        for act in activities:
            act_rows.append([
                Paragraph(act.get('role', ''), body_style),
                Paragraph(act.get('organization', ''), body_style),
                Paragraph(act.get('event', ''), body_style),
                Paragraph(act.get('category', ''), body_style),
                Paragraph(act.get('period', ''), body_style),
            ])
        
        act_table = Table(act_rows, colWidths=[120, 110, 130, 90, 70])
        act_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#312E81')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(act_table)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#9CA3AF'), spaceAfter=10))
    story.append(Paragraph("<i>This is an official document generated by UniNet Co-Curricular Verification Engine. Verified by Faculty of Applied Sciences, Wayamba University of Sri Lanka.</i>", ParagraphStyle('FooterText', parent=body_style, fontSize=8, textColor=colors.HexColor('#6B7280'), alignment=1)))

    doc.build(story)
    buffer.seek(0)
    return buffer
