<h2>About This Directory</h2>

This directory contains the backend for running the simulations.
<br></br>
<ul>
  <li>Data.py contains the necessary data management functionality such as querying the database or Yahoo Finance and inputing into a dataframe based on user requests.</li>
  <li>Strategies.py contains all the strategies available for testing, which are given to simulation.py.</li>
  <li>Simulation.py calculates the technical indicator values, trade entries and exits, and the resulting portfolio metrics. It also serves as the primary input to components with callbacks, providing datatables and plots.</li>
</ul>