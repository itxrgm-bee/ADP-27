from datetime import date, timedelta
from attendance.models import Attendance
from attendance.services import workday_state

def report_rows(employee, start, end):
    records={row.attendance_date: row for row in Attendance.objects.filter(employee=employee, attendance_date__range=(start,end))}
    rows=[]; day=start
    while day <= end:
        row=records.get(day); rows.append(row or {"attendance_date": day, "status": workday_state(day) or Attendance.Status.ABSENT})
        day += timedelta(days=1)
    return rows

def summary(rows):
    result={"total_working_days":0,"present_days":0,"late_days":0,"absent_days":0,"holiday_days":0,"weekend_days":0,"incomplete_days":0,"total_late_minutes":0}
    for row in rows:
        status=row.status if isinstance(row, Attendance) else row["status"]
        key={"PRESENT":"present_days","LATE":"late_days","ABSENT":"absent_days","HOLIDAY":"holiday_days","WEEKEND":"weekend_days","INCOMPLETE":"incomplete_days"}.get(status)
        if key: result[key]+=1
        if status not in ("HOLIDAY","WEEKEND"): result["total_working_days"]+=1
        if isinstance(row, Attendance): result["total_late_minutes"] += row.late_minutes
    return result
