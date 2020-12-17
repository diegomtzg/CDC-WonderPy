# CDCWonderPy

### Project report
The link the final project report is [here](https://docs.google.com/document/d/1P3UFiE-uWBVhwtNX628DYGbVvB_h-R51hyMhV3Vm3xA/edit?usp=sharing)


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