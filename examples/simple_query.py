import cdcwonderpy as wonder
from cdcwonderpy.enums import *

if __name__ == '__main__':
    """
        Example of a query that shows how simple it is to get the most general
        version of the data. No need to specify the parameters you don't care about.
        
        Here, we want to get all the male death occurrences in the database and view
        the result as a Pandas dataframe.
        """
    response = wonder.Request().gender(Gender.MALE).send()
    print(response.as_dataframe())
