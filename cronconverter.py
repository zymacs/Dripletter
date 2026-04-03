import re
from typing import List, Union


class CronConverter:
    """Converts  human schedules to cron"""
    
    def __init__(self):
        self.days = {
            'monday': 1, 'mon': 1,
            'tuesday': 2, 'tue': 2,
            'wednesday': 3, 'wed': 3,
            'thursday': 4, 'thu': 4,
            'friday': 5, 'fri': 5,
            'saturday': 6, 'sat': 6,
            'sunday': 0, 'sun': 0
        }
        
        self.day_groups = {
            'weekday': [1, 2, 3, 4, 5],  # Mon-Fri
            'weekdays': [1, 2, 3, 4, 5],
            'weekend': [0, 6],  # Sun, Sat
            'daily': [0, 1, 2, 3, 4, 5, 6],
            'all': [0, 1, 2, 3, 4, 5, 6]
        }

        month_indices = list(range(0,12))
        months = 'january february march april may june july august september october november december'.split()
        months_short = 'jan feb mar apr may june jul aug sept oct nov dec'.split()

        self.months = {month:month_index for month,month_index in zip(months,month_indices)}
        self.months.update({month_short:month_index for month_short, month_index in zip(months_short, month_indices)})
    
    def convert_time(self, time_str: str) -> tuple:
        """Convert time string to (hour, minute) in 24-hour format"""
        time_str = time_str.strip().lower()
        
        # Handle 12-hour format with AM/PM
        if 'am' in time_str or 'pm' in time_str:
            time_part = time_str.replace('am', '').replace('pm', '').strip()
            hour, minute = map(int, time_part.split(':'))
            
            if 'pm' in time_str and hour != 12:
                hour += 12
            elif 'am' in time_str and hour == 12:
                hour = 0
        else:
            # 24-hour format
            hour, minute = map(int, time_str.split(':'))
        
        return hour, minute
    
    def convert_days(self, days_input: Union[str, List[str]]) -> str:
        """Convert day specifications to cron day-of-week string"""
        if isinstance(days_input, str):
            days_input = [d.strip() for d in days_input.split(',')]
        
        day_numbers = []
        for day in days_input:
            day_lower = day.lower()
            
            # Check if it's a day group
            if day_lower in self.day_groups:
                day_numbers.extend(self.day_groups[day_lower])
            # Check if it's a specific day
            elif day_lower in self.days:
                day_numbers.append(self.days[day_lower])
            else:
                raise ValueError(f"Invalid day specification: {day}")
        
        # Remove duplicates and sort
        day_numbers = sorted(set(day_numbers))
        return ','.join(map(str, day_numbers))
    
    def to_cron(self, days: Union[str, List[str]], time_str: str) -> str:
        """Convert days and time to cron format"""
        hour, minute = self.convert_time(time_str)
        day_of_week = self.convert_days(days)
        # implement months
        return f"{minute} {hour} * * {day_of_week}"
    
    def to_cron_line(self, days: Union[str, List[str]], time_str: str, command: str) -> str:
        """Generate full cron line with command"""
        cron_time = self.to_cron(days, time_str)
        return f"{cron_time} {command}"

    def extract_time(self, sentence: str) -> str:
        """Extract time string from some arbitrary sentence string."""

        time_pattern = r'(\d{1,2}:\d{2}\s*(?:am|pm)?)' # the ?:am|pm is a non-capture group
        time_match = re.search(time_pattern, sentence)
        if not time_match:
            raise ValueError("Could not find time in sentence")
        time_str = time_match.group(1)
        return time_str

    def extract_days(self, sentence:str) -> str:
        """Extract days from some arbitrary sentence string."""

        days = []
        for day in self.days.keys():
            if day in sentence:
                days.append(day)
        return days
    
    def parse_sentence(self, sentence: str) -> str:
        """Parse natural language sentence to cron format"""
        sentence = sentence.lower()
        
        # Extract time
        time_str = self.extract_time(sentence)
        
        # Extract days
        days = self.extract_days(sentence)
        
        # If no specific days found, check for day groups
        if not days:
            for group in self.day_groups:
                if group in sentence:
                    days = [group]
                    break
        
        if not days:
            days = ['daily']  # Default to daily
        
        return self.to_cron(days, time_str)
    
    def validate_cron(self, cron_expr: str) -> bool:
        """Validate cron expression"""
        try:
            minute, hour, day, month, day_of_week = cron_expr.split()
            
            # Validate minute
            if minute != '*':
                minutes = minute.split(',')
                for m in minutes:
                    if int(m) not in range(0, 60):
                        return False
            
            # Validate hour
            if hour != '*':
                hours = hour.split(',')
                for h in hours:
                    if int(h) not in range(0, 24):
                        return False
            
            # Validate day of week
            if day_of_week != '*':
                days = day_of_week.split(',')
                for d in days:
                    if int(d) not in range(0, 7):
                        return False

            # Validate month of week
            if month != '*':
                months = months_of_year.split(',')
                for m in months:
                    if int(m) not in range(0,12):
                        return False
            
            return True
        except:
            return False

