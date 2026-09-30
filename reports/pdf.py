from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from django.conf import settings
from django.utils import timezone

def attendance_pdf(title, employee, rows, stats, period):
    output=BytesIO(); doc=SimpleDocTemplate(output,pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36); styles=getSampleStyleSheet(); story=[Paragraph("Employee Attendance Management",styles["Title"]),Paragraph(title,styles["Heading2"]),Paragraph(f"Period: {period} | Generated: {timezone.localtime():%Y-%m-%d %H:%M:%S} ({settings.TIME_ZONE})",styles["Normal"]),Spacer(1,12)]
    if employee: story.append(Paragraph(f"Employee: {employee.name} | Phone: {employee.phone_number} | Designation: {employee.designation}",styles["Normal"]))
    story.append(Spacer(1,12)); story.append(Paragraph("Summary: " + ", ".join(f"{key.replace('_',' ').title()}: {value}" for key,value in stats.items()),styles["Normal"])); story.append(Spacer(1,12))
    data=[["Date","Check in","Check out","Status","Late minutes"]]
    for row in rows:
        if hasattr(row,"attendance_date"): data.append([str(row.attendance_date), str(row.check_in_time or "-"), str(row.check_out_time or "-"), row.status, str(row.late_minutes)])
        else: data.append([str(row["attendance_date"]),"-","-",row["status"],"0"])
    table=Table(data,repeatRows=1); table.setStyle(TableStyle([["BACKGROUND",(0,0),(-1,0),colors.HexColor("#183b56")],["TEXTCOLOR",(0,0),(-1,0),colors.white],["GRID",(0,0),(-1,-1),.25,colors.grey],["FONTSIZE",(0,0),(-1,-1),8]])); story.append(table); doc.build(story); output.seek(0); return output
