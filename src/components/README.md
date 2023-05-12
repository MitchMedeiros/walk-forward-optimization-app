<h2>About This Directory</h2>

This directory holds all the the apps visual components such as buttons and dropdowns. It contains all of the front end of the app. In addition, certain modules have callbacks defined in them for executing backend operations based on user input, such as updating plots when the user changes the dates. 

The entire UI is constructed in layout.py inside the `create_layout()` function by bringing together the components and any additional formatting inside a div. The div is then provided to `app.layout` in main.py for displaying.