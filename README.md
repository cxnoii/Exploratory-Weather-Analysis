# Exploratory Weather Analysis

## Overview
The goal of this project is to analyze data from Hawaii Weather Stations to visualize weather patterns from previous years. Data from a SQLite database will be reflected into Python's SQLAlchemy, where the data will be analyzed using Pandas and Matplotlib. Flask will be used in order to create local API endpoints that will return data specified at by the user.

![flask](https://user-images.githubusercontent.com/114107454/224617784-8673f751-af0a-468c-b66a-569a08617ffd.jpg)

## Resources
* [Weather Data Article](https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml)

## Methods
1. In order to access the data in Python, an engine was created using SQLAlchemy and the tables were reflected onto the base model. A session was then created to query the database to explore the data. 
![flask code1](https://user-images.githubusercontent.com/114107454/224622315-c8213de9-f331-44fd-b0c5-cf6b2bd4d88f.jpg)

2. The first point of interest was the amount of precipitation recorded. A query was designed to return the date and amount of precipitation for the most recent year available in the dataset. The results of the query were then saved to a Pandas dataframe and the date column was converted to datetime format. 

![flask_code](https://user-images.githubusercontent.com/114107454/224622827-09335bb0-86af-453d-8935-50590e11a745.jpg)

3. The precipitation data was then plotted using matplotlib.

![flaskssss](https://user-images.githubusercontent.com/114107454/224624067-dd1d3e17-68df-419c-9d0c-1a3341198c11.jpg)

4. The next feature of interest was the temperature; to find the most active weather station, a query was created to count the number of entries each weather station had.

![flask code 3](https://user-images.githubusercontent.com/114107454/224625425-1161e88c-1b2e-42c5-9d24-a87013e58515.jpg)


5. Queries were then designed to find the dates with highest and lowest historical temperatures as well as the average of recorded temperature by the most active station (ID: 'USC00519281').

![flask 4](https://user-images.githubusercontent.com/114107454/224625402-925f1654-ca44-4648-a4fe-6b7da8511bca.jpg)
