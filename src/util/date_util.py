from datetime import timedelta

class DateUtil:
    LEN_WEEK = 7

    @staticmethod
    def get_next_week_date(current_date):
        next_week = current_date + timedelta(days=DateUtil.LEN_WEEK)
        return next_week

    @staticmethod
    def is_date_greater(date, end_date):
        return date > end_date
    
    @staticmethod
    def week_list(initial_date, end_date):
        weeks = []
        current_start = initial_date
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=DateUtil.LEN_WEEK - 1), end_date)
            weeks.append((current_start, current_end))
            current_start = current_end + timedelta(days=1)
        return weeks
        
    @staticmethod
    def get_week_range(date):
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=DateUtil.LEN_WEEK - 1)
        return (start_of_week, end_of_week)
    
    @staticmethod
    def get_final_date(start_date, weeks=12):
        end_date = start_date + timedelta(weeks=weeks)
        return end_date

