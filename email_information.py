from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import datetime


def email_information(email_dataframe, delta_days):

    if len(email_dataframe[email_dataframe['Algoritm1'] == 1]) == 0:
        df_email = f'no matches:   {date.today() + datetime.timedelta(days=delta_days)}'
        msg = MIMEMultipart()
        msg['Subject'] = "Automated odds report"  # set email subject
        msg.attach(MIMEText(df_email))  # add text contents
    else:
        df_email = email_dataframe[email_dataframe['Algoritm1_inv'] == 1].copy()
        df_email1 = df_email[['Home Team', 'Away Team', 'Home Team Odds', 'Away Team Odds', 'Form', 'Form Value']].copy()

        df_email1.columns = ['Home', 'Away', 'Win1', 'Win2', 'Form', 'Form Value']

        html = """\
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
        """.format(df_email1.to_html())

        part1 = MIMEText(html, 'html')

        msg = MIMEMultipart()
        msg['Subject'] = "Automated odds report"  # set email subject
        msg.attach(part1)

    return msg.as_string()
