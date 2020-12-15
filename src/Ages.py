class Ages:
    def __init__(self):
        self._date_set = set()

    @staticmethod
    def single(age):
        result = Dates()
        if isinstance(timePeriod, Year):
            for i in range(1, CalendarMonth.NUM_MONTHS+1):
                result._date_set.add(CalendarMonth(i, timePeriod.get_year()))

        elif isinstance(timePeriod, CalendarMonth):
            result._date_set.add(timePeriod)

        else:
            raise TypeError("Time period must be either a CalendarMonth or a Year")

        return result

    @staticmethod
    def range(start_age, end_age):
        if not (isinstance(beginPeriod, Year) or isinstance(beginPeriod, CalendarMonth)) or not (isinstance(endPeriod, Year) or isinstance(endPeriod, CalendarMonth)):
            raise TypeError("Time periods must be either CalendarMonths or Years")
        if (isinstance(beginPeriod, CalendarMonth) and not isinstance(endPeriod, CalendarMonth)) or (isinstance(beginPeriod, Year) and not isinstance(endPeriod, Year)):
            raise TypeError("Begin period and end period type must match (either both CalendarMonth or both Year)")

        if beginPeriod.is_after(endPeriod):
            raise ValueError("Begin period must be before or equal to end period; Begin: "+str(beginPeriod)+" End: "+str(endPeriod))

        result = Dates()
        if(isinstance(beginPeriod, Year)):
            for year in range(beginPeriod.get_year(), endPeriod.get_year()+1):
                for month in range(1, CalendarMonth.NUM_MONTHS+1):
                    result._date_set.add(CalendarMonth(month, year))
        else:
            curr_year = beginPeriod.get_year()
            curr_month = beginPeriod.get_month()
            end_year = endPeriod.get_year()
            end_month = endPeriod.get_month()
            while(not (curr_month == end_month and curr_year == end_year)):
                result._date_set.add(CalendarMonth(curr_month, curr_year))
                curr_month+=1
                if(curr_month > CalendarMonth.NUM_MONTHS):
                    curr_month = 1
                    curr_year+=1
            result._date_set.add(CalendarMonth(end_month, end_year))
        return result

    def get_months(self):
        return list(self._date_set)

    @staticmethod
    def union(dates1, dates2):
        if not isinstance(dates1, Dates) or not isinstance(dates2, Dates):
            raise TypeError("Both objects must be and instance of Dates")

        result = Dates()
        result._date_set = dates1._date_set.union(dates2._date_set)
        return result

    def __repr__(self):
        return str(self.get_months())