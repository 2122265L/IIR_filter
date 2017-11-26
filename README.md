# IIR_filter
Cascade IIR filter class

This class was created to make IIR filters simpler to use.

How it works is by generating 2nd order coeficients from butter function.
And then cascading the all the generated filters either in parrales or series depending on the type of filter specifid and it cut off frequencies.

It takes the cutoff frequencies, as are needed to get the right bands in the frequency responce.
The frequencies should be normalised to nyquist = 0.5.

The order number and the filter type should be specifid too.

Hope you like it,

2122265L
