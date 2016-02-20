# bitcoin-price-check #
Python script to check the price of bitcoin to USD and then add values to a mysql database.

Script to scrape and store bitcoin prices from json object.


## Needed for this application: ##
	mysql database running
	python
	may need to install modules with pip


## Need to do: ##
	Program needs to make a guess on a future price based on data


## In this order, the program needs to: ##
	Get the values from the database;
	Specifiy which database values are needed, over what Period of time
	Change the time values into integers
	Calculate StandardError of the line
	Calculate the values up until the most recent database entry
	Make a guess for the price at the next hour.
	Based on the guess, either make more predictions like that one, or make different predictions

### Side-Note: ###
	I would prefer that the program just sends data to another portion of the program rather than calculting guessed values,
	but programming this would cause server-client programming, and I dont feel like adding this functionality until
	a further date. 

	Graph the data and then find a best fit curve for the data.
	Turn Time into an Integer, then graph and estimate the values


## Currently being added: ##
	Guessing ability.. /Predictions from the database

### Later Functionality: ###
	When to start the program and when to stop it
	Graphics, Graphs and Charts showing extimated values
