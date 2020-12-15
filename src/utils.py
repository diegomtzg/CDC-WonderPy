from Dates import *

def dictToXML(parameterDict):
    """
    Helper function that transforms a dictionary of parameter -> value
    mappings to an equivalent XML string representation.
    """
    parameterString = ""
    for key in parameterDict:
        parameterString += "<parameter>\n"
        parameterString += "<name>" + key + "</name>\n"

        # If value is a list, concatenate all values
        if isinstance(parameterDict[key], list) or isinstance(parameterDict[key], tuple):
            for value in parameterDict[key]:
                parameterString += "<value>" + value + "</value>\n"
        else:
            parameterString += "<value>" + parameterDict[key] + "</value>\n"

        parameterString += "</parameter>\n"

    return parameterString