import pandas as pd
import PySimpleGUI as sg
import traceback

'''
Code below takes the stock market dataframe, including ticker, revenue, growth rate, and PE; and filters
for the best and worst stocks in comparison to average growth rate and average PE
'''

#Open pickle data frame
table = pd.DataFrame(pd.read_pickle('stock_table.pkl'))

#Format the user interface with theme and font
sg.theme('Reddit')
sg.set_options(font='calibri', text_color='black')

#create set of sectors from dataframe, will be used in drop down menu
industries = set(table['Sector'])
industries.add('')

#Interface created below, first with the layout being customized
layout = [
    [sg.Text("Enter information below:")],
    [sg.Text("Revenue Min:"),sg.Input(key = 'Rev Min'),sg.Push()],
    [sg.Text("Revenue Max:"), sg.Input(key = 'Rev Max'), sg.Push()],
    [sg.Text("Sector:"), sg.Combo(sorted(list(industries)), key='sector', enable_events=True), sg.Push()],
    [sg.Exit(), sg.Button("OK")]
]

window = sg.Window("Buy/Sell Predictor", layout)

#Once options have been selected above, pop up window will launch with the results
while True:
    try:
        event, values = window.read()
        
        
        #Entries above used to filter the datafram
        if event == "OK":
            current = pd.DataFrame(table)
            if values['Rev Max']:
                current = current[current['Revenue'] <= int(values['Rev Max'])]
                
            if values['Rev Min']:    
                current = current[current['Revenue'] >= int(values['Rev Min'])]
                
            if values['sector'] != '':
                current = current[current['Sector'] == values['sector']]
                
            current.drop('Sector', axis=1, inplace=True)
            
            '''
            Buy/Sell rating calculated as follows:
                - Calculate average growth rate and PE ratio for entire group of stocks
                - A good PE ratio is one that is less than the average, and vice versa
                - A good growth rate is one that is greater than the average, and vice versa
                - Rating = average((stock PE / avg PE - 1)*-1, (stock GR / avg GR - 1))
                - The PE portion is multiplied by -1 since a good stock will result in a negative number 
                
            '''
            
            averageGR = current['Growth Rate '].mean()
            averagePE = current['PE'].mean()
            current['Buy/Sell Rating'] = ((current['Growth Rate ']/averageGR-1)+(current['PE']/averagePE-1)*-1)/2
            
            #Format various columns to 2 decimals places and multiple growth rate by 100 to turn into a %
            current['Buy/Sell Rating'] = round(current['Buy/Sell Rating'],2)
            current['Growth Rate '] = round(current['Growth Rate ']*100,2) 
            current['PE'] = round(current['PE'],2)
            
            #Sort dataframe based on the calculated Buy/Sell column
            current.sort_values('Buy/Sell Rating', inplace=True)
            
            #Update column headers to include unit of measurement
            current = current.rename(columns={'Revenue': 'Revenue ($)'})
            current = current.rename(columns={'Growth Rate ': 'Growth Rate (%)'})
            
            #Create Sell stock dataframe to include in output
            bottom8 = current.head(8)
            
            #Create Buy stock dataframe to include in output
            current.sort_values('Buy/Sell Rating', ascending=False, inplace=True)
            top8 = current.head(8)
            
            #Keys used to allow for default entries for each input parameter
            layout_industry = values['sector'] if values['sector'] else 'All'
            layout_minRev = values['Rev Min'] if values['Rev Min'] else 'Zero'
            layout_maxRev = values['Rev Max'] if values['Rev Max'] else 'Infinity'
            
            #Remaining code is creation of result window and presenting the result window
            layout = [
                [sg.Text(f"Sector: {layout_industry}, Revenue: {layout_minRev} -> {layout_maxRev}")],
                [sg.Text(f'Average Growth Rate: {round(averageGR*100, 2)}%')],
                [sg.Text(f'Average PE Ratio: {round(averagePE,2)}')],
                [sg.Text('Buy:')],
                [sg.Table(values=top8.values.tolist(), headings=top8.columns.tolist())],
                [sg.Text('Sell:')],
                [sg.Table(values=bottom8.values.tolist(), headings=bottom8.columns.tolist())],
                [sg.Button('Exit')]
            ]
            
            newWindow = sg.Window('Results', layout)
            newWindowEvent, newWindowValues = newWindow.read()
            if newWindowEvent == sg.WIN_CLOSED or newWindowEvent == "Exit":
                newWindow.close()
                
        #Closing of user interface entry window
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            break
        
    #Exception thrown if there is an error in the code above, usually related to issues with the initial dataframe
    except Exception as e:
        # print the error message and traceback
        tb = traceback.format_exc()
        print(f"Error: {e} \nTraceback: {tb}")
        # show a popup window with the error message
        sg.popup_no_titlebar(f"Error: {e}", background_color='red', text_color='white')
        break


