from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Create PDF
pdf_file = 'contract.pdf'
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add title
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor='black',
    spaceAfter=0.3*inch,
    alignment=1
)
story.append(Paragraph('SERVICE AGREEMENT', title_style))
story.append(Spacer(1, 0.2*inch))

# Add content
content = """
<b>THIS SERVICE AGREEMENT</b> ("Agreement") is entered into as of the date of execution, between the undersigned parties.

<b>1. SERVICES</b><br/>
The Service Provider agrees to provide consulting and advisory services as outlined in this Agreement. Services shall commence upon execution and continue for a period of twelve (12) months unless terminated earlier by mutual written consent.

<b>2. COMPENSATION</b><br/>
In consideration for services rendered, Client agrees to pay Service Provider a monthly fee of USD 5,000.00, payable on the first business day of each month.

<b>3. CONFIDENTIALITY</b><br/>
Both parties agree to maintain confidentiality of any proprietary information disclosed during the course of this engagement. This obligation shall survive termination of this Agreement for a period of two (2) years.

<b>4. TERM AND TERMINATION</b><br/>
This Agreement may be terminated by either party upon thirty (30) days written notice. Upon termination, all obligations shall cease except those that by their nature are intended to survive.

<b>5. GOVERNING LAW</b><br/>
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of law principles.

<b>6. ENTIRE AGREEMENT</b><br/>
This Agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, and agreements.

IN WITNESS WHEREOF, the parties execute this Agreement as of the date first written above.

SERVICE PROVIDER: _________________________ DATE: _________

CLIENT: _________________________ DATE: _________
"""

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    leading=14,
    spaceAfter=0.1*inch
)
story.append(Paragraph(content, body_style))

# Build PDF
doc.build(story)
print('✓ Contract PDF created: contract.pdf')
