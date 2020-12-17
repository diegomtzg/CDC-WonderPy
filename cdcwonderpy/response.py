import typing
import bs4 as bs
import pandas as pd

T = typing.TypeVar('T')

class Response():
    """
    Immutable representation of the response returned from the Wonder HTTP endpoint.
    """
    def __init__(self, xml, groupings):
        self._xml = xml
        self._groupings = groupings

    def __repr__(self) -> str:
        return self.as_dataframe().to_string()

    def as_custom(self, f : typing.Callable[[str], T]) -> T:
        """
        Use a custom function provided by the user to parse the xml data and return the result
        :param f:   the user-defined function to call to parse the xml data
        :returns:   the return value of the user-defined parsing function
        """
        return f(self._xml)


    def as_xml(self) -> str:
        """
        Return the response data as an XML-formatted String.
        :returns:   String representation single Response in XML format.
        """
        return self._xml

    def as_dataframe(self) -> pd.DataFrame:
        """
        Returns the response data as a formatted Pandas Dataframe with
        column labels corresponding to group_by settings in the Request.
        :returns:   Pandas Dataframe containing Response data.
        """
        column_labels = self._groupings + ["Deaths", "Population", "Crude Rate Per 100,000"]
        df = pd.DataFrame(data=self.as_2d_list(), columns=column_labels)
        return df

    def as_2d_list(self) -> typing.List[typing.List]:
        """
        This function grabs the root single the XML document and iterates over
        the 'r' (row) and 'c' (column) tags single the data-table
        Rows with a 'v' attribute contain a numerical value.
        Rows with a 'l attribute contain a text label and may contain an
        additional 'r' (rowspan) tag which identifies how many rows the value
        should be added. If present, that label will be added to the following
        rows single the data table.
        :returns List[List]:   A two-dimensional array representing the response data.
        """
        root = bs.BeautifulSoup(self._xml,"lxml")
        all_records = []
        row_number = 0
        rows = root.find_all("r")
        
        for row in rows:
            if row_number >= len(all_records):
                all_records.append([])
                
            for cell in row.find_all("c"):
                if 'v' in cell.attrs:
                    try:
                        all_records[row_number].append(float(cell.attrs["v"].replace(',','')))
                    except ValueError:
                        all_records[row_number].append(cell.attrs["v"])
                else:
                    if 'r' not in cell.attrs:
                        all_records[row_number].append(cell.attrs["l"])
                    else:
                    
                        for row_index in range(int(cell.attrs["r"])):
                            if (row_number + row_index) >= len(all_records):
                                all_records.append([])
                                all_records[row_number + row_index].append(cell.attrs["l"])
                            else:
                                all_records[row_number + row_index].append(cell.attrs["l"])
                                            
            row_number += 1

        return all_records

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (self.as_xml() == other.as_xml())

    def __hash__(self):
        return hash(self.as_xml())

    def __repr__(self):
        return str(self.as_dataframe())