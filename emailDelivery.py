from email.mime.text import MIMEText
import smtplib



def send_email(email, salary, count, average_salary):
    email_from = "yoyoshubhamsingh5@gmail.com"
    password_from = "jojohoneysingh"
    email_to = email

    subject = "Average salary data"
    message = "Hey there, <br> Your salary is $<strong>%s</strong>. <br> Based on <strong>%s</strong> numbers of suveys, average salary of Canadian population is $<strong>%s</strong> <br> <br> Thanks!"  % (salary, count, average_salary)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = email_to

    msg['From'] = email_from
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_from, password_from)
    gmail.send_message(msg)