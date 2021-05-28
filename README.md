# covidBEDashboard

## Introduction

The goal of the app is just to explore pandas, numpy and dash Python libraries and present COVID-19 information provided by Sciensano:
https://epistat.wiv-isp.be/covid/

The selection of the graphs and indicators is just a personal preference. That's because during the COVID crisis I was (and I'm) constantly checking Belgium indicators provided by Sciensano. But the data provided by Sciensano was provided in the format that was not quite convenient for me.
Thus I decided to create my own small dashboard to gather all the information needed for me in one place.

## Technologies used

The app is built using:
* pandas and numpy to load and manipulate data
* dash to visualise data
* dash bootstrap components to get a responsive layout of the app
All needed packages and dependecies are listed in `requirements.txt`

## Future developments

A few things are planned to improve the dashboard:
* separate mobile version to improve presentation of the charts
* add prediction functionality using scipy package to predict values of cases, hostipalisations, etc.