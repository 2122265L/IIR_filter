# IIR_filter
Cascade IIR filter class

This class breaks down high order IIR filters into second order filters before filtering a signal.

How it works is by generating 2nd order coeficients from the scipy.signal.butter function.
The resulting filters are then cascaded either in parrales or series depending on the type of filter specifid and the number of off frequencies.

The frequencies should be normalised to nyquist = 0.5.
The order number and the filter type should be specifid too.

## Usage

Access the Module with:
  
  `import IIRpy`

## Initialisation

Create an instance of the function and initialise it as follows:
  
  `Var = IIRpy.IIR(order, Cutoff_frequencies, Filter_type)`

## Filtering

Sample by sample for realtime processing:
i.e with the signal being a single value not an array.
```
  y = Var.filter(signal)
```

## Coding examples
See the the IIRpy_Demo.py document for an example implementation of the filter


Hope you like it,

2122265L
