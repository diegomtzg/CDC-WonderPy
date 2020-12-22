# CDCWonderPy

A wrapper around the CDC Wonder API for the Compressed Mortality dataset meant to alleviate some of the many issues that the CDC's API has. For more information, see projectProposal and finalReport in the root directory.

## Main feature highlights:
* Request class initialized to default values. Users only need to specify parameters they wish to change.
* Parameter and filter names renamed across the board. Users can now specify filters by their appropriate names (i.e. "race()" instead of V_D76.V8) and set their values with intuitive value enums (i.e. Race.WHITE instead of "2106-3").
* Response formatting: Rather than having to parse the XML from the response, Request.send() returns an immutable Response object that has several formatting methods to see the results as 2D lists or a Pandas dataframe.

See examples directory for more information on how to use the API.

### Running locally
To install dependencies, run the following command at `src` root:
```
pip install -r requirements.txt
```

The entire API is contained in the folder cdcwonderpy, which is a python package that can be imported from python modules in the base in directory of the repo. For example, you could create a new program "wonder_example.py" in the base directory of this repo and should be able to import the cdcwonderpy library. See the examples folder for what this could look like.

To run all unit tests, open a terminal in the base directory of the repo and run the command
```
python -m unittest
```

To run specific tests, run `python -m unittest tests/<testToRun>.py` from the top level directory with the angle brackets replaced with the desired test module.

To run our client code examples located in the "examples" folder, open a terminal in the base directory of the repo and run the command
```
python examples/<exampleToRun>.py
```
with the angle brackets replaced with the desired example module
