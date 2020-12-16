from wonder.enums import Grouping

class Ages:
    def __init__(self):
        self._age_set = set()

    @staticmethod
    def Single(age: int):
        result = Ages()
        if isinstance(age, int):
            result._age_set.add(str(age))
        else:
            raise TypeError("Single Age must be an int.")

        return result

    @staticmethod
    def Range(start_age, end_age):
        if not (isinstance(start_age, int) or isinstance(end_age, int)):
            raise TypeError("Age range start and end must be of type int.")

        if end_age < start_age:
            raise ValueError("Starting age must be before or equal to end age; Start: "+str(start_age)+" End: "+str(end_age))

        result = Ages()
        for age in range(start_age, end_age+1):
            result._age_set.add(str(age))

        return result

    def as_list(self):
        return sorted(list(self._age_set))

    def union(self, other):
        if not isinstance(other, Ages):
            raise TypeError("Both objects must be an instance of Ages")

        result = Ages()
        result._age_set = self._age_set.union(other._age_set)
        return result

    ###############################
    ##### Private Methods
    ###############################

    def _is_valid_age_group(self, age_group_type):
        try:
            formatted_grouping = self._as_age_group_type(age_group_type)
        except:
            return False

        age_group_size = 0
        if age_group_type == Grouping.TenYearAgeGroups:
            age_group_size = 10
        elif age_group_type == Grouping.FiveYearAgeGroups:
            age_group_size = 5
        else:
            age_group_size = 1

        for block in formatted_grouping:
            if len(block) != age_group_size:
                print("A")
                return False
            elif block != list(range(block[0], block[-1]+1)):
                print("B")
                return False
            elif age_group_type == Grouping.TenYearAgeGroups and block[0]%10 != 5:
                print(block)
                print("C")
                return False
            elif age_group_type == Grouping.FiveYearAgeGroups and block[0]%10 not in [0,5]:
                print("D")
                return False

        return True

    def _as_age_group_type(self, age_group_type):
        ages = self.as_list()

        age_group_size = 0
        if age_group_type == Grouping.TenYearAgeGroups:
            age_group_size = 10
        elif age_group_type == Grouping.FiveYearAgeGroups:
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

    def __repr__(self):
        return str(self.as_list())
