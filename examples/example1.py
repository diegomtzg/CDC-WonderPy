import cdcwonderpy
from cdcwonderpy.enums import *

if __name__ == '__main__':
    response = cdcwonderpy.Request().place_of_death(PlaceOfDeath.DecedentHome).send()
    print(response.as_dataframe())