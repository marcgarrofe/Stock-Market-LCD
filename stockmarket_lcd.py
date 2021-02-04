#! /usr/bin/env python

# Simple string program. Writes and updates IBEX_35 Stock Market values.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Marc Garrofe

# Import necessary libraries for communication and display use
import drivers
import time
import requests
from bs4 import BeautifulSoup

# Load the driver and set it to "display"
display = drivers.Lcd()


# Get the stock data from a html source and return 3 dictionaries with the stock value, max and min
def getData():
    page = requests.get("https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html")
    soup = BeautifulSoup(page.content, 'html.parser')

    stock_table_soup = soup.find(id="listado_valores").find('tbody')
    stock_value_soup = stock_table_soup.find_all(class_="primera")

    stock_name = []
    stock_value = []

    stock_dict_value = {}
    stock_dict_max = {}
    stock_dict_min = {}

    for name in stock_value_soup:
        stock_name.append(name.get_text())

    stock_value_aux = stock_table_soup.find_all('tr')

    for values in stock_value_aux:
        for line_soup in values:
            line_str = str(line_soup)
            if line_str != "\n" and line_str != "<tr>":
                    if "icono" not in line_str and "class" not in line_str:
                        line_value = line_str.lstrip("<td>")
                        line_value = line_value.rstrip("</td>")
                        stock_value.append(line_value)
                        #print(line_value)

    counter = 0

    for name in stock_name:
        pos = counter * 6
        value = stock_value[pos]
        max_value = stock_value[pos + 1]
        min_value = stock_value[pos + 2]
        counter = counter + 1
        stock_dict_value[name] = value
        stock_dict_max[name] = max_value
        stock_dict_min[name] = min_value

    return stock_dict_value, stock_dict_max, stock_dict_min

# getCompanyPrice() return the value of the company if it exists
def getCompanyPrice(company):
    if company in stock_dict_value:
        return stock_dict_value[company]
    else:
        print("Error: The company doesn't exists")
        return 0

# showAllCompaniesLCDLoop() function shows the price of the stocks
def showAllCompaniesLCDLoop():
    for company in stock_dict_value:
        display.lcd_display_string(company, 1)
        display.lcd_display_string(getCompanyPrice(company), 2)
        time.sleep(2)
        display.lcd_clear()


# Main body of code

# Call getData() function
stock_dict_value = getData()[0].copy() # Get Stock value
stock_dict_max = getData()[1].copy()   # Get Stock Max
stock_dict_min = getData()[2].copy()   # get Stock Min

try:
    while True:
        showAllCompaniesLCDLoop()
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()

