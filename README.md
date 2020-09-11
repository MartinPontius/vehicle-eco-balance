# vehicle-eco-balance

This library offers functionality to analyse the eco balance of moving vehicles. So far vehicles are restricted to cars (trucks or busses should also work but are not evaluated yet).
It allows users to estimate the fuel or energy demand and co2 emissions along tracks.

To analyse the eco balance of cars, we recommend to use the package envirocar-py (https://github.com/enviroCar/envirocar-py) to download xFCD from the open Citizen Science Platform enviroCar (https://envirocar.org/).

## Installation

The package requires a Python version >= 3.6. The package is available on the PyPI package manager and can be installed with the following command:

```
pip install vehicle-eco-balance --upgrade
```

To install vehicle-eco-balance in develop mode, use the following:

```
python setup.py develop
```


## Examples
Example of the package can be found [here](https://github.com/MartinPontius/vehicle-eco-balance/tree/master/examples).


## Documentation

To check the usage of the provided functions and classes use `help(<class/function>)`, e.g. `help(Consumption)`.


## License ##
    MIT License

    Copyright (c) 2020 The enviroCar Project

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
