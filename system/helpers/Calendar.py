from datetime import datetime, timedelta
from calendar import HTMLCalendar

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None,model=None,eventsFunction=None):
        self.model = model
        self.year = year
        self.month = month
        self.eventsFunction = eventsFunction
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        date = str(self.year)+"-"+f"{self.month:02}"+'-'+f"{day:02}"
        today = datetime.today().strftime('%Y-%m-%d')
        events_per_day = events.filter(date__endswith=f"{day:02}")
        d = ''
        for event in events_per_day:
            d += f'<li> {self.eventsFunction(event)} </li>'

        if day != 0:
            if date==today:
                return f"<td style='position:relative;background-color:MediumTurquoise'><div class='date'>{str(day)+' Today'}</div> {d} </td>"
            else:
                return f"<td style='position:relative;'><div class='date'>{day}</div> {d} </td>"
            
        return '<td></td>'
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'
    def formatmonth(self, withyear=True):
        events = self.model.objects.filter(date__contains=str(self.year)+"-"+f"{self.month:02}")

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal+'</table>'