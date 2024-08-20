import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def sanitize_filename(title):
    # Remove any character that is not alphanumeric, space, hyphen, or underscore
    sanitized_title = re.sub(r'[^a-zA-Z0-9 \-_]', '', title)
    return sanitized_title


def create_pdf_with_video_details(video_details, buffer):
    try:
        sanitized_title = sanitize_filename(video_details["Title"])
        sanitized_author = sanitize_filename(video_details["Author"])
        filename = f"{sanitized_author}_{sanitized_title}.pdf"

        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)
        styles = getSampleStyleSheet()
        story = []

        # Add Title
        title_paragraph = Paragraph(f'<b>{video_details["Title"]}</b>', styles['Title'])
        story.append(title_paragraph)
        story.append(Spacer(1, 0.2 * inch))

        # Add other details as a table
        data = [
            ["Author", video_details["Author"]],
            ["Subscription", video_details["Subscription"]],
            ["Comment Count", video_details["Comment Count"]],
            ["Like Count", video_details["Like Count"]],
            ["View Count", video_details["View Count"]],
            ["Media Type", video_details["Media Type"]],
            ["Length", video_details["Length"]],
            ["Video URL", video_details["Video URL"]],
        ]

        table = Table(data, colWidths=[1.5 * inch, 4.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

        # Add Script text
        text_paragraph = Paragraph(f'<b>Script:</b><br/>{video_details["Script"]}', styles['BodyText'])
        story.append(text_paragraph)

        # Build the PDF
        doc.build(story)
        print(f"PDF created with filename: {filename}")
        return filename
    except Exception as exe:
        print(f"Error while generating PDF for title: {video_details['Title']}")
        print(f"Error: {exe}")
