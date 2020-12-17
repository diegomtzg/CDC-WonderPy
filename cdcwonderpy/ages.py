import typing
from cdcwonderpy.enums import Grouping

class Ages:
    """
    Immutable representation of collections of ages upon which CDC Wonder Requests can filter.
    """
    def __init__(self):
        """
        Initializes an empty Ages instance.
        """
        self._age_set = set()
    
    def __repr__(self) -> str:
        """
        Returns the string representation of the Ages instance as a sorted 2D list.

        @returns:   String representation of the Ages instance.
        """
        return str(self.as_list())

    @staticmethod
    def Single(age: int) -> Ages:
        """
        Static method for generating a new Ages instance corresponding to a single age value.
        Valid ages that can be filtered upon range between 1 and 99, inclusive.
        
        @param  age:        Positive int representing the age value to be stored by the new instance.
        @raises TypeError:  If the user inputs a non-int age value.
        @raises ValueError: If the user inputs an age int less than 1 or greater than 99.
        @returns            Ages instance representing the age int passed into the static method.
        """
        result = Ages()
        if not isinstance(age, int):
            raise TypeError("Single Age must be an int.")
        elif age < 1 or age > 99:
            raise ValueError(f"Valid age values range from 1 to 99, inclusive, and user inputted: {age}")
        else:
            result._age_set.add(str(age))

        return result

    @staticmethod
    def Range(start_age: int, end_age: int) -> Ages:
        """
        Static method for generating a new Ages instance corresponding to a range of age values.
        Valid ages that can be filtered upon range between 1 and 99, inclusive.
        
        @param  start_age:  Positive int representing the start of the age range to be stored by the new instance.
        @param  end_age:    Positive int representing the end (inclusive) of the age range to be stored by the new instance.
        @raises TypeError:  If the user inputs a non-int age value.
        @raises ValueError: If the user inputs an age int less than 1 or greater than 99.
        @returns            Ages instance representing the age range passed into the static method.
        """
        if not (isinstance(start_age, int) or isinstance(end_age, int)):
            raise TypeError("Age range start and end must be of type int.")
        elif (start_age < 1 or start_age > 99) or (end_age < 1 or end_age > 99):
            raise ValueError(f"Valid age values range from 1 to 99, inclusive, and user inputted: {start_age}-{end_age}")
        if end_age < start_age:
            raise ValueError("Starting age must be before or equal to end age; Start: "+str(start_age)+" End: "+str(end_age))

        result = Ages()
        for age in range(start_age, end_age+1):
            result._age_set.add(str(age))

        return result

    def as_list(self) -> list:
        """
        Method for retrieving the Ages instance values as a sorted list of represented age values.

        @returns:   List containing sorted age values represented by called upon Ages instance.
        """
        return sorted(list(self._age_set))

    def union(self, other: Ages) -> Ages:
        """
        Method for generating a new Ages instance containing the union of the ages represented by
        the called upon instance and the other passed in instance.

        @param  other:      A second Ages instance to be unioned.
        @raises TypeError:  If user does not input an Ages instance as `other`.
        @returns:           A new instance representing the union of the two target Ages instances.
        """
        if not isinstance(other, Ages):
            raise TypeError("Both objects must be an instance of Ages")

        result = Ages()
        result._age_set = self._age_set.union(other._age_set)
        return result

    ###############################
    ##### Private Methods
    ###############################

    def _is_valid_age_group(self, age_group_type: Grouping) -> bool:
        """
        Module internal method for calculating if the called upon Ages instance contains a valid series of
        Ages for age_group_type. Valid input options include the TEN, FIVE, and SINGLE YEAR AGE GROUPS
        options for the Grouping enum.
        
        For example:
            Ages.Range(15,44)._is_valid_age_group(Grouping.TEN_YEAR_AGE_GROUPS) == True
            Ages.Range(15,39)._is_valid_age_group(Grouping.TEN_YEAR_AGE_GROUPS) == False
            Ages.Range(15,39)._is_valid_age_group(Grouping.FIVE_YEAR_AGE_GROUPS) == True
            Ages.Range(15,38)._is_valid_age_group(Grouping.FIVE_YEAR_AGE_GROUPS) == False
            Ages.Range(15,38)._is_valid_age_group(Grouping.SINGLE_YEAR_AGE_GROUPS) == True

        @param  age_group_type: Grouping instance corresponding to types of age groups to be analyzed.
        @raises TypeError:      If inputted age_group_type is not a valid Grouping age group Enum.
        @returns:               Boolean representing if Ages instance is of valid age group type.
        """
        if age_group_type not in [Grouping.TEN_YEAR_AGE_GROUPS,
                                  Grouping.FIVE_YEAR_AGE_GROUPS,
                                  Grouping.SINGLE_YEAR_AGE_GROUPS]:
            raise TypeError("age_group_type not of valid type within the Grouping Enum class.")

        try:
            formatted_grouping = self._as_age_group_type(age_group_type)
        except:
            return False

        age_group_size = 0
        if age_group_type == Grouping.TEN_YEAR_AGE_GROUPS:
            age_group_size = 10
        elif age_group_type == Grouping.FIVE_YEAR_AGE_GROUPS:
            age_group_size = 5
        else:
            age_group_size = 1

        for block in formatted_grouping:
            if len(block) != age_group_size:
                return False
            elif block != list(range(block[0], block[-1]+1)):
                return False
            elif age_group_type == Grouping.TEN_YEAR_AGE_GROUPS and block[0]%10 != 5:
                return False
            elif age_group_type == Grouping.FIVE_YEAR_AGE_GROUPS and block[0]%10 not in [0,5]:
                return False

        return True

    def _as_age_group_type(self, age_group_type: Grouping) -> typing.List[typing.List]:
        """
        Module internal method for returning the Ages instance as a 2D list where the ages stored by
        the instance are partitioned into sorted lists of max size corresponding to the intended size
        of the passed in age_group_type. For example, Grouping.TEN_YEAR_AGE_GROUPS corresponds to a
        maximum partition size of 10 age elements.

        @param  age_group_type: Grouping instance corresponding to types of age groups to be analyzed.
        @raises TypeError:      If inputted age_group_type is not a valid Grouping age group Enum.
        @returns:               2D list representing partitions of the called upon Ages instance.
        """
        if age_group_type not in [Grouping.TEN_YEAR_AGE_GROUPS,
                                  Grouping.FIVE_YEAR_AGE_GROUPS,
                                  Grouping.SINGLE_YEAR_AGE_GROUPS]:
            raise TypeError("age_group_type not of valid type within the Grouping Enum class.")

        ages = self.as_list()

        age_group_size = 0
        if age_group_type == Grouping.TEN_YEAR_AGE_GROUPS:
            age_group_size = 10
        elif age_group_type == Grouping.FIVE_YEAR_AGE_GROUPS:
            age_group_size = 5
        else:
            age_group_size = 1
        
        groups, curr_block, block_index = [], [], 0
        for age in ages:
            curr_block.append(int(age))
            block_index += 1
            if len(curr_block) == age_group_size:
                groups.append(curr_block)
                curr_block = []
                block_index = 0
        
        if block_index != 0:
            raise ValueError(f"Invalid Group Size: Cannot group ages by type {age_group_type.name}")

        return groups
