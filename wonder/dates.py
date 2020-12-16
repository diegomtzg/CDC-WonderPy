import typing

class Dates:
    def __init__(self):
        self._date_set = set()

    @staticmethod
    def single(timePeriod : typing.Union['Year', 'YearAndMonth']) -> 'Dates':
        result = Dates()
        if isinstance(timePeriod, Year):
            for i in range(1, YearAndMonth.NUM_MONTHS + 1):
                result._date_set.add(YearAndMonth(i, timePeriod.get_year()))

        elif isinstance(timePeriod, YearAndMonth):
            result._date_set.add(timePeriod)

        else:
            raise TypeError("Time period must be either a YearAndMonth or a Year")

        return result

    @staticmethod
    def range(beginPeriod : typing.Union['Year', 'YearAndMonth'], endPeriod : typing.Union['Year', 'YearAndMonth']) -> 'Dates':
        if not (isinstance(beginPeriod, Year) or isinstance(beginPeriod, YearAndMonth)) or not (isinstance(endPeriod, Year) or isinstance(endPeriod, YearAndMonth)):
            raise TypeError("Time periods must be either CalendarMonths or Years")
        if (isinstance(beginPeriod, YearAndMonth) and not isinstance(endPeriod, YearAndMonth)) or (isinstance(beginPeriod, Year) and not isinstance(endPeriod, Year)):
            raise TypeError("Begin period and end period type must match (either both YearAndMonth or both Year)")

        if beginPeriod.is_after(endPeriod):
            raise ValueError("Begin period must be before or equal to end period; Begin: "+str(beginPeriod)+" End: "+str(endPeriod))

        result = Dates()
        if(isinstance(beginPeriod, Year)):
            for year in range(beginPeriod.get_year(), endPeriod.get_year()+1):
                for month in range(1, YearAndMonth.NUM_MONTHS + 1):
                    result._date_set.add(YearAndMonth(year, month))
        else:
            curr_year = beginPeriod.get_year()
            curr_month = beginPeriod.get_month()
            end_year = endPeriod.get_year()
            end_month = endPeriod.get_month()
            while(not (curr_month == end_month and curr_year == end_year)):
                result._date_set.add(YearAndMonth(curr_year, curr_month))
                curr_month+=1
                if(curr_month > YearAndMonth.NUM_MONTHS):
                    curr_month = 1
                    curr_year+=1
            result._date_set.add(YearAndMonth(end_year, end_month))
        return result

    def get_months(self) -> 'YearAndMonth':
        return list(self._date_set)

    def union(self, other : 'Dates') -> 'Dates':
        if not isinstance(self, Dates) or not isinstance(other, Dates):
            raise TypeError("Both objects must be and instance single Dates")

        result = Dates()
        result._date_set = self._date_set.union(other._date_set)
        return result

    def __repr__(self):
        return str(self.get_months())


class Year:
    def __init__(self, year : int):
        if not isinstance(year, int):
            raise TypeError("Year must be constructed using an integer to represent a valid year")
        
        self._year = year

    def get_year(self) -> int:
        return self._year

    def is_before(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        if isinstance(other, Year) or isinstance(other, YearAndMonth):
            return self._year < other.get_year()
        else:
            raise TypeError("Other must be a Year or YearAndMonth")

    def is_after(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        if isinstance(other, Year) or isinstance(other, YearAndMonth):
            return self._year > other.get_year()
        else:
            raise TypeError("Other must be a Year or YearAndMonth")

    def __repr__(self):
        return str(self._year)

    def __eq__(self, other):
        if isinstance(other, Year):
            return self._year == other._year
        return False

    def __hash__(self):
        return hash(self._year)

class YearAndMonth:
    NUM_MONTHS = 12
    def __init__(self, year : int, month : int):
        if not isinstance(month, int) or not isinstance(year, int):
            raise TypeError("YearAndMonth must be constructed using an integer representation for both the month and year. For example, July 1998 would be constructed as YearAndMonth(7, 1998): "+str(month)+", "+str(year))

        if month <= 0 or month > YearAndMonth.NUM_MONTHS:
            raise ValueError("Month parameter must be between 1 and 12 (inclusive): "+str(month))
        
        self._month = month
        self._year = year

    def get_month(self) -> int:
        return self._month

    def get_year(self) -> int:
        return self._year

    def is_before(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        if isinstance(other, Year):
            return self._year < other.get_year()
        elif isinstance(other, YearAndMonth):
            if self._year < other._year:
                return True
            elif self._year == other._year:
                return self._month < other._month
            else:
                return False
        else:
            raise TypeError("Other must be a Year or YearAndMonth")

    def is_after(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        if isinstance(other, Year):
            return self._year > other.get_year()
        elif isinstance(other, YearAndMonth):
            if self._year > other._year:
                return True
            elif self._year == other._year:
                return self._month > other._month
            else:
                return False
        else:
            raise TypeError("Other must be a Year or YearAndMonth")

    def __eq__(self, other):
        if isinstance(other, YearAndMonth):
            return self._month == other._month and self._year == other._year
        return False

    def __repr__(self):
        return f"{self.get_year()}/{self.get_month():02d}"

    def __lt__(self, other):
        if not isinstance(other, YearAndMonth):
            raise TypeError("Can only compare with other YearAndMonth objects")

        return self.is_before(other)

    def __hash__(self):
        return hash((self._month, self._year))
