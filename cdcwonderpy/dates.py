import typing

class Dates:
    """
    * Represents an immutable set of dates to filter on in a Request. The dates can be specified to the month.
    * To create a new Dates object, use the static methods Dates.single and Dates.range.
    * The Dates object should not be created via the constructor (doing so will given an empty set of dates).
    """
    def __init__(self):
        self._date_set = set()

    @staticmethod
    def single(timePeriod : typing.Union['Year', 'YearAndMonth']) -> 'Dates':
        """
        Create a new Dates object containing a single time period.
        The timePeriod must be either a Year or a YearAndMonth. A Year will include all months
        :param timePeriod:      the Year or YearAndMonth to include in the new Dates object
        :raises TypeError:      TypeError if timePeriod is not a Year or a YearAndMonth
        :returns:               a new Date object containing the timePeriod
        """
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
        """
        Create a new Dates object containing all dates between the beginPeriod and endPeriod (inclusive on both ends).
        The beginPeriod and endPeriod may either be Year objects or YearAndMonth objects, but they should be the same
        Using Years will include all months from the beginPeriod year through the endPeriod year
        :param beginPeriod:     the beginning Year or YearAndMonth for the desired range (inclusive)
        :param endPeriod:       the end Year or YearAndMonth for the desired range (inclusive)
        :raises TypeError:      if the beginPeriod and endPeriod are not both Year or YearAndMonth and the same
        :raises ValueError:     ValueError if the beginPeriod is stricly after the endPeriod
        :returns:               a new Date object containing all months from beginPeriod to endPeriod
        """
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
        """
        Get the list of months contained in this Dates object
        :returns:       a list of YearAndMonths contained in this Dates object
        """
        return list(self._date_set)

    def union(self, other : 'Dates') -> 'Dates':
        """
        Get the list of months contained in this Dates object
        :param other:       the other Dates object to get the union of
        :raises TypeError:  if the other object is not a Dates object 
        :returns:           a list of YearAndMonths contained in this Dates object
        """
        if not isinstance(other, Dates):
            raise TypeError("Other object must be a Dates object")

        result = Dates()
        result._date_set = self._date_set.union(other._date_set)
        return result

    def __repr__(self):
        return str(self.get_months())


class Year:
    """
    * Represents a particular Gregorian calendar year such as 1998.
    * Used in creating a Dates object as a parameter to Dates.single or Dates.range
    """
    def __init__(self, year : int):
        """
        Create a Year object representing the given calendar year.
        :param year:        the calendar year this object represents
        :raises TypeError:  if the given year is not an integer
        :returns:           a new Year object that represents the given year
        """
        if not isinstance(year, int):
            raise TypeError("Year must be constructed using an integer to represent a valid year")
        
        self._year = year

    def get_year(self) -> int:
        """
        Get the calendar year that is represented by this object.
        :returns:   the calendar year represented by this object
        """
        return self._year

    def is_before(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        """
        Compare this object with a Year or YearAndMonth object and return true if it is strictly before other.
        When comparing with a YearAndMonth object, only the year is considered
        :param other:       the other Year or YearAndMonth object to compare to
        :raises TypeError:  if other is not a Year or YearAndMonth object
        :returns:           true if this object is strictly before other, false otherwise
        """
        if isinstance(other, Year) or isinstance(other, YearAndMonth):
            return self._year < other.get_year()
        else:
            raise TypeError("Other must be a Year or YearAndMonth")

    def is_after(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        """
        Compare this object with a Year or YearAndMonth object and return true if it is strictly after other.
        When comparing with a YearAndMonth object, only the year is considered
        :param other:       the other Year or YearAndMonth object to compare to
        :raises TypeError:  if other is not a Year or YearAndMonth object
        :returns:           true if this object is strictly after other, false otherwise
        """
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
    """
    * Represents a particular Gregorian calendar year and month such as July, 1998.
    * Used in creating a Dates object as a parameter to Dates.single or Dates.range.
    * Months are specified as numbers between 1 and 12, starting with January.
    """
    NUM_MONTHS = 12
    def __init__(self, year : int, month : int):
        """
        Create a Year object representing the given calendar year and month.
        :param year:        the calendar year this object represents
        :param month:       the calendar month this object represents (between 1 and 12, starting at January)
        :raises TypeError:  if the given year or month are not integers
        :raises ValueError: if the given month is not between 1 and 12
        :returns:           a new YearAndMonth object that represents the given year and month
        """
        if not isinstance(month, int) or not isinstance(year, int):
            raise TypeError("YearAndMonth must be constructed using an integer representation for both the month and year. For example, July 1998 would be constructed as YearAndMonth(7, 1998): "+str(month)+", "+str(year))

        if month <= 0 or month > YearAndMonth.NUM_MONTHS:
            raise ValueError("Month parameter must be between 1 and 12 (inclusive): "+str(month))
        
        self._month = month
        self._year = year

    def get_month(self) -> int:
        """
        Get the calendar month that is represented by this object.
        :returns:   the calendar month represented by this object
        """
        return self._month

    def get_year(self) -> int:
        """
        Get the calendar year that is represented by this object.
        :returns:   the calendar year represented by this object
        """
        return self._year

    def is_before(self, other : typing.Union['Year', 'YearAndMonth']) -> bool:
        """
        Compare this object with a Year or YearAndMonth object and return true if it is strictly before other.
        When comparing with a Year object, only the year is considered
        :param other:       the other Year or YearAndMonth object to compare to
        :raises TypeError:  if other is not a Year or YearAndMonth object
        :returns:           true if this object is strictly before other, false otherwise
        """
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
        """
        Compare this object with a Year or YearAndMonth object and return true if it is strictly after other.
        When comparing with a Year object, only the year is considered
        :param other:       the other Year or YearAndMonth object to compare to
        :raises TypeError:  if other is not a Year or YearAndMonth object
        :returns:           true if this object is strictly after other, false otherwise
        """
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
