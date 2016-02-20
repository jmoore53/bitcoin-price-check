import requests
import datetime
import time
import MySQLdb
import smtplib
import traceback
from copy import deepcopy
from email.mime.text import MIMEText
#import random

#Important Program Values
TimeValue = {}
URL = 'https://api.coinbase.com/v2/exchange-rates?currency=BTC'
error_counter = 0
Exception_dictionary = {}
now = datetime.datetime.now().strftime("%m/%d/%Y; %H:%M:%S")

def main():
        print("Starting Real Time Bitcoin Values Script...")
        send_email(1,"Program has just started","Program has just started, please allow ample time for script to run.",now)
        global error_counter
        TimeValueIndex = 0;
        global now
                #Add a while loop listening port and depending on message either start or stop the program.
                #All you have to do is adjust the while loop under this, add a variable and make the while loop check the variable...
                #listening_port_value = (integer)
                #example: while(error_counter <= 100 && listening_value_start == true)
        while(error_counter <= 100):
                while(True):
                        try:
                                TimeValueIndex = 0
                                for i in range(175):
                                        #Raise_random is a test value for when exceptions are raised to test sending emails and adding errors to error_log
                                        #raise_random()
                                        get_rates(TimeValueIndex)
                                        TimeValueIndex += 1
                                        time.sleep(10)
                                #get_listening_port_value() - this should tell the program when to stop and start, currently the program runs an infinite loop
                                send_email(1,"Prices",str(TimeValue),now)
                                dict_to_file(TimeValue)
                        except Exception as e:
                                trace = traceback.format_exc()
                                send_error_report(str(trace), now)
                                error_counter += 1
                                break
                        finally:
                                if(error_counter == 100):
                                        print("Shutting down program to debug...")
                                        send_email(4,"Program has crashed","Program has crashed.",now)
                        break

def get_rates(TimeValueIndexPar):
	#possibly add an if statement to only add the time and price if the price has changed.
        request = requests.get(URL)
        #resjson = request.json() #windows
        resjson = request.json #linux
        USD_rate = resjson["data"]["rates"]["USD"]
        USD_rate = USD_rate
        now = datetime.datetime.now()
        rateTimelist = [now, USD_rate] 
        TimeValue[TimeValueIndexPar] = rateTimelist
        #print(str(TimeValueIndexPar) +"'s value is: " + str(TimeValue[TimeValueIndexPar]).strip("[]"))
        
        
def dict_to_file(myDictionary):
        global error_counter, now
        print("Dumping Dictionary to file...")
        print("May consume memory...")
        try:
                #connection = MySQLdb.connect(host = "localhost", user = "root", db = "bitcoin")#windows
        	
                connection = MySQLdb.connect(host = "localhost", user = "root", passwd = "sqlpassword", db = "bitcoin")#linux
                cursor = connection.cursor()
                for x in myDictionary:
                        values = myDictionary[x]
                        cursor.execute("""INSERT INTO `time_and_rates` VALUES(%s,%s)""",(values[0],values[1]))
                        #print(str(x) + "'s values has been added to the table")
                connection.commit()
                Success_Message = "Program has successfully written to database!"
                Success_Subject = "Program Successfully Written to Database!"
                send_email(2,Success_Subject, Success_Message, now)
        except Exception as e:
                trace = traceback.format_exc()
                send_error_report(str(trace),now)
                Failure_Subject = "Program Unsuccessfully written to database, Shutting Down"
                Failure_Message = "Unfortunately, the program has not successfully written to database." + str(e)
                send_email(4,Failure_Subject, Failure_message + str(trace), now)
                error_counter += 1
                connection.rollback()
        cursor.close()
        connection.close()
        

def send_error_report(exception, exception_time):
        global Exception_dictionary, error_counter, now
        error_list = [exception, exception_time]
        Exception_dictionary[error_counter] = error_list
        Exception_dict_copy = []


        try:
                #connection = MySQLdb.connect(host = "localhost", user = "root", db = "bitcoin") #windows
                connection = MySQLdb.connect(host = "localhost", user = "root", passwd = "sqlpassword", db = "bitcoin") #linux
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO `error_log` VALUES(%s,%s)""",(str(exception), str(exception_time)))
                connection.commit()
        except Exception as e:
                error_counter = 100
                print(e)
                print("Could not connect to database, sending email and rolling back.")
                error_message = "::: Some database error. shutting program down" + str(e)
                send_email(4,"Could not connect to error_log database, shutting down!", error_message, now)
                connection.rollback()
        finally:
                cursor.close()
                connection.close()
        
        #send email of 5 most recent Errors
        if(error_counter % 5 == 0 and error_counter != 0):
                error_mod = error_counter % 10
                for keys,values in Exception_dictionary.items():
                        Exception_dict_copy.append(str(values).strip('[]'))
                        #print(str(values).strip('[]'))
                print(str(Exception_dict_copy).strip("[]"))

                Message = 'Recent Error Report, errors: '+str(error_counter-5)+" through: "+str(error_counter)+"\n\n\n"+str(Exception_dict_copy).strip("[]")
                Subject = 'List of the 5 most recent errors'

                send_email(4,Subject,Message,now)
                
                Exception_dictionary = {}


def send_email(email_type, email_subject, email_message, time):

        # Email Type:
        # 1 : Information
        # 2 : Success
        # 4 : Error

        global error_counter
        try:
                to = 'moorew1997@gmail.com'
                gmail_user = 'moore.william1997@gmail.com'
                gmail_password = 'pgmr tkwe htbx pasx'

                smtpserver = smtplib.SMTP_SSL('smtp.gmail.com',465)
                smtpserver.ehlo()
                smtpserver.login(gmail_user, gmail_password)
                msg = MIMEText(email_message)
                if email_type == 1:
                        msg['Subject'] = "INFORMATION: "+ str(time)+ " "+email_subject 
                elif email_type == 2:
                        msg['Subject'] = "SUCCESS: "+ str(time)+ " "+email_subject
                elif email_type == 4:
                        msg['Subject'] = "ERROR: "+ str(time)+ " "+email_subject
                msg['From'] = gmail_user
                msg['To'] = to
            
                smtpserver.sendmail(gmail_user, [to], msg.as_string())
                smtpserver.quit()

        except Exception, e:
                print(e)
                error_counter = 100
        finally:
                print("Thank you for sending an email.")



#Test method used to 'raise' exceptions in main method to test whether or not error reporting is done correctly
def raise_random():
        x = random.randint(0, 5)
        if(x == 5):
                raise NameError('This is a NameError')
        elif(x == 4):
                raise KeyError('This is a KeyError')
        elif(x == 3):
                raise StandardError('This is a StandardError')
        elif(x == 2):
                raise LookupError('This is a LookupError')



main()


#Method to predict the next values using statistics and probability


def guess_price(time_span):
	#use the time_span passed value to calculate the price for the next hour, or the next day
	#
	pass

