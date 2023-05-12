<h2>About This Directory</h2>

This directory contains all of the app's interactive functionality. The dash callbacks utilize JavaScript to take in user inputs involving the dash components, perform a specified Python function, and then update the arguments of existing components within the app layout. New components can be created from a callback by updating the children argument. 

As an example, selecting a date in the calendar component triggers the callbacks that have the date component as an input. The decorated Python function is then run and when complete should specify one or more return values that update the specified output components.