from flask import Flask, render_template, request
import pandas as pd
import traceback
import os
from datetime import datetime

app = Flask(__name__)


# Open pickle data frame
table = pd.DataFrame(pd.read_pickle('stock_table.pkl'))

# Create set of sectors from dataframe, will be used in drop down menu
industries = set(table['Sector'])
industries.add('')

update_time = os.path.getmtime("stock_table.pkl")
update_time= datetime.fromtimestamp(update_time).strftime('%Y-%m-%d')

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html',Sectors=industries,stock_date=update_time)

# Route for processing user input and displaying results
@app.route('/submit', methods=['Post'])
def result():
    try:
        rev_min = request.form['Minimum Revenue']
        rev_max = request.form['Maximum Revenue']
        sector = request.form['Sector']

        # Entries above used to filter the dataframe
        current = pd.DataFrame(table)
        if rev_max:
            current = current[current['Revenue'] <= int(rev_max)]

        if rev_min:
            current = current[current['Revenue'] >= int(rev_min)]

        if sector != '':
            current = current[current['Sector'] == sector]

        averageGR = current['Growth Rate'].mean()
        averagePE = current['PE Ratio'].mean()
        current['Buy/Sell Rating'] = ((current['Growth Rate']/averageGR-1)+(current['PE Ratio']/averagePE-1)*-1)/2

        #Format various columns to 2 decimals places and multiple growth rate by 100 to turn into a %
        current['Buy/Sell Rating'] = round(current['Buy/Sell Rating'],2)
        current['Growth Rate'] = current['Growth Rate'].apply(lambda x: '{:.2%}'.format(x))
        current['Revenue'] = current['Revenue'].apply(lambda x: '{:,}'.format(x))
        current['PE Ratio'] = round(current['PE Ratio'],2)

        current.sort_values('Buy/Sell Rating', ascending=False, inplace=True)

        #Create Sell stock dataframe to include in output
        bottom8 = current.tail(8)
        top8 = current.head(8)

        bottom8 = bottom8[bottom8['Buy/Sell Rating'] < 0]
        top8 = top8[top8['Buy/Sell Rating'] > 0]
        
        #Create Buy stock dataframe to include in output
        bottom8.sort_values('Buy/Sell Rating', ascending=True, inplace=True)
    
        # Remaining code for displaying results...
        return render_template('index.html', top8=top8, bottom8=bottom8, 
                               averageGR=str(round(averageGR*100,2))+'%', 
                               averagePE=round(averagePE, 2), 
                               Sectors=industries,stock_date=update_time)

    except Exception as e:
        # Print the error message and traceback
        tb = traceback.format_exc()
        print(f"Error: {e} \nTraceback: {tb}")
        return f"Error: {e}"
    
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


'''
@app.route('/contact', methods=['POST'])
def sendMessage():
    if request.method == 'POST':
        email_address = request.form['email']
        message = request.form['message']

        # Send email
        send_email(email_address, message)

    return render_template('contact.html')

def send_email(email_address, message):

    smtp_server = 'your_smtp_server'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'

    sender_email = 'your_email@example.com'
    receiver_email = 'your_email@example.com'

    subject = 'Stock Score Message Submission'
    body = f'Email: {email_address}\n\nMessage: {message}'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
'''
        

if __name__ == '__main__':
    app.run(debug=True)