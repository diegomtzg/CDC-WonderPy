# CDCWonderPy

### Project report
The link the final project report is in the base directory of this repo


### Running locally
To install dependencies, run the following command at `src` root:
```
pip install -r requirements.txt
```

The entire API is contained in the folder cdcwonderpy, which is a python package that can be imported from python modules in the base in directory of the repo. For example, you could create a new program "wonder_example.py" in the base directory of this repo and should be able to import the cdcwonderpy library. See the examples folder for what this could look like.

To run unit tests, open a terminal in the base directory of the repo and run the command
```
python -m unittest
```

To run our client code examples located in the "examples" folder, open a terminal in the base directory of the repo and run the command
```
python examples/<exampleToRun>.py
```
with the angle brackets replaced with the desired example module