from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import Dict, Any
import os
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        # Register fonts for different languages
        self._register_fonts()
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()

    def _register_fonts(self):
        # Register Malayalam font if available
        malayalam_font_path = os.path.join('backend', 'app', 'static', 'fonts', 'NotoSansMalayalam-Regular.ttf')
        if os.path.exists(malayalam_font_path):
            pdfmetrics.registerFont(TTFont('Malayalam', malayalam_font_path))
        
        # Register Tamil font if available
        tamil_font_path = os.path.join('backend', 'app', 'static', 'fonts', 'NotoSansTamil-Regular.ttf')
        if os.path.exists(tamil_font_path):
            pdfmetrics.registerFont(TTFont('Tamil', tamil_font_path))

    def _add_custom_styles(self):
        # Add custom styles for different languages
        self.styles.add(ParagraphStyle(
            name='Malayalam',
            fontName='Malayalam',
            fontSize=12,
            leading=14
        ))
        self.styles.add(ParagraphStyle(
            name='Tamil',
            fontName='Tamil',
            fontSize=12,
            leading=14
        ))

    def _get_style_for_language(self, language: str) -> str:
        if language == 'ml':
            return 'Malayalam'
        elif language == 'ta':
            return 'Tamil'
        return 'Normal'

    def generate_horoscope_pdf(self, data: Dict[str, Any], language: str = 'en') -> str:
        """Generate a horoscope PDF report."""
        filename = f"horoscope_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{language}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []

        # Title
        title_style = self.styles['Title']
        title_style.fontName = self._get_style_for_language(language)
        story.append(Paragraph("Horoscope Report", title_style))
        story.append(Spacer(1, 12))

        # Personal Information
        story.append(Paragraph("Personal Information", self.styles['Heading2']))
        personal_data = [
            ["Name", data.get('name', '')],
            ["Date of Birth", data.get('dob', '')],
            ["Time of Birth", data.get('tob', '')],
            ["Place of Birth", data.get('place', '')]
        ]
        table = Table(personal_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self._get_style_for_language(language)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Horoscope Details
        story.append(Paragraph("Horoscope Details", self.styles['Heading2']))
        horoscope_data = [
            ["Rashi", data.get('rashi', '')],
            ["Nakshatra", data.get('nakshatra', '')],
            ["Lagna", data.get('lagna', '')],
            ["Planetary Positions", data.get('planetary_positions', '')]
        ]
        table = Table(horoscope_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self._get_style_for_language(language)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)

        # Generate PDF
        doc.build(story)
        return filename

    def generate_matchmaking_pdf(self, data: Dict[str, Any], language: str = 'en') -> str:
        """Generate a matchmaking PDF report."""
        filename = f"matchmaking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{language}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []

        # Title
        title_style = self.styles['Title']
        title_style.fontName = self._get_style_for_language(language)
        story.append(Paragraph("Matchmaking Report", title_style))
        story.append(Spacer(1, 12))

        # Bride Information
        story.append(Paragraph("Bride's Information", self.styles['Heading2']))
        bride_data = [
            ["Name", data.get('bride_name', '')],
            ["Date of Birth", data.get('bride_dob', '')],
            ["Time of Birth", data.get('bride_tob', '')],
            ["Place of Birth", data.get('bride_place', '')]
        ]
        table = Table(bride_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self._get_style_for_language(language)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Groom Information
        story.append(Paragraph("Groom's Information", self.styles['Heading2']))
        groom_data = [
            ["Name", data.get('groom_name', '')],
            ["Date of Birth", data.get('groom_dob', '')],
            ["Time of Birth", data.get('groom_tob', '')],
            ["Place of Birth", data.get('groom_place', '')]
        ]
        table = Table(groom_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self._get_style_for_language(language)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 12))

        # Matchmaking Results
        story.append(Paragraph("Matchmaking Results", self.styles['Heading2']))
        results_data = [
            ["Guna Score", str(data.get('guna_score', 0))],
            ["Compatibility", data.get('compatibility', '')],
            ["Remarks", data.get('remarks', '')]
        ]
        table = Table(results_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), self._get_style_for_language(language)),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)

        # Generate PDF
        doc.build(story)
        return filename 