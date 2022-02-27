from pywebio.input import *
from pywebio.output import *
from pywebio.exceptions import *
from flask import Flask, send_from_directory
from pywebio.platform.flask import webio_view
import argparse
from pywebio import start_server
import time


app = Flask(__name__)


#######################################################
################# validation function #################
#######################################################

# validation check on eligibility platform
def validateCheckEligibility(data):
    
    # validation check on age
    if data['age'] == None:
        return('age', 'Please enter your age. ')
    elif data['age'] <= 0:
        return('age', 'Age cannot be zero or negative value.')
    elif data['age'] > 100:
        return('age', 'Age cannot beyond 100 years old because the average life expectancy in Singapore is 83.5 years old.')
    
    # validation check on citizenship
    if data['citizenship'] == None:
        return('citizenship', 'Please select one of these options. ')
    
    # validation check on current beneficiary
    if data['current_beneficiary'] == None:
        return('current_beneficiary', 'Please select one of these options. ')
    
    # validation check on existing IMDA
    if data['existing_IMDA'] == None:
        return('existing_IMDA', 'Please select one of these options.')
    

# validation check on application form platform
def validateApplicationForm(data1):
    # validation check on name 
    if data1['name'] == '':
        return('name', 'Please enter a valid name as per in NRIC.') 
    elif data1['name'].replace(" ", "").isalpha() == False:
        return('name', 'Please ensure that your name is valid.')
    elif len(data1['name']) > 35:
        return('name', 'Please ensure that your name is below 35 characters.')
    
    # validation check on identification 
    if data1['identification'] == '':
        return('identification', 'Please enter a valid NRIC.')
    elif len(data1['identification']) != 9:
        return('identification', 'Please ensure that your NRIC comes with this format @XXXXXXX# where @ represents a letter `S`, X represents a digit, and # represents a letter')
    elif data1['identification'].isalnum() == False:
        return('identification', 'Please ensure that your NRIC comes with this format @XXXXXXX# where @ represents a letter `S`, X represents a digit, and # represents a letter')
    elif data1['identification'][0].upper() != 'S':
        return('identification', 'Please ensure that you are a Singapore Citizen who was born before 1 January 2000 and is assigned the letter `S`. ')
    elif data1['identification'][-1].isalpha() == False and data1['identification'][1:8].isnumeric() == False:
        return('identification', 'Please ensure that your NRIC comes with this format @XXXXXXX# where @ represents a letter `S`, X represents a digit, and # represents a letter')
    elif data1['identification'][-1].isalpha() == False:
        return('identification', 'Please ensure that the last value of your NRIC is a letter.')
    elif data1['identification'][1:8].isnumeric() == False:
        return('identification', 'Please ensure that your NRIC consists of 7-digit serial number.')
    
    
    # validation check on gender
    if data1['gender'] == None:
        return('gender', 'Please select one of these options.')
    
    # validation check on date of birth
    if data1['dob'] == '':
        return('dob', 'Please enter your date of birth.')
    elif data1['dob'].replace(" ", "").isalnum() == True:
        return('dob', 'Please ensure that your date of birth is in this format: XX/XX/XXXX where X represents a digit.')
    for text in data1['dob']:
        if text in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '{', '}', '[', ']', ':', ';', '<', '>', '?', '.', '-'] or text.isalpha() == True:
            return('dob', 'Please ensure that your date of birth is in this format: XX/XX/XXXX where X represents a digit.')
        
    # obtain the birth year
    splitDOB = data1['dob'].split("/")
    
    # obtain the birth date
    birthDate = splitDOB[0]
    # obtain the birth month
    birthMonth = splitDOB[1]
    # obtain the birth year
    birthYear = splitDOB[2]
    
    # convert the birthDate into numerical data type
    birthDateVal = int(birthDate)
    # convert the birthMonth into numerical data type
    birthMonthVal = int(birthMonth)
    # convert birthYear into numerical data type
    birthYearVal = int(birthYear)
   
    
    if (birthMonthVal < 1 or birthMonthVal > 12) and (birthDateVal < 1 or birthDateVal > 31) and (birthYearVal < 1922 or birthYearVal > 1962):
        return('dob', 'Please ensure that your birth date is in between 01 and 31; your birth month is in between 01 and 12; your birth year in in between 1922 and 1962.')
    
    if birthDateVal < 1 or birthDateVal > 31:
        return('dob', 'Please ensure that your birth date is in between 01 and 31. ')
    
    if birthMonthVal < 1 or birthMonthVal > 12:
        return('dob', 'Please ensure that your birth month is in between 01 and 12.')
    
    if birthYearVal < 1922 or birthYearVal > 1962:
        return('dob', 'Please ensure that your birth year in in between 1922 and 1962.')
    
    
    
    # validation check on home address
    if data1['address'] == '':
        return('address', 'Please enter your home address.')
    
    # validation check on email
    if data1['email'] == '':
        return('email', 'Please enter your designated personal email address. ')
    
    email_format1 = data1['email'].find('@gmail.com')
    email_format2 = data1['email'].find('@hotmail.com')
    email_format3 = data1['email'].find('@ymail.com')
    if email_format1 == -1 and email_format2 == -1 and email_format3 == -1:
        return('email', 'Please ensure that your personal email address is valid and is in this format: XYZ@email.com. ')
    
    for text in data1['email']:
        if text in ['!', '#', '$', '%', '^', '&', '*', '(', ')', '~', '{', '}', '[', ']', ':', ';', '<', '>', '?', '-']:
            return('email', 'Please ensure that your personal email address is valid and is in this format: XYZ@email.com.')
    
    # validation check on telecom 
    if data1['telecom'] == None:
        return('telecom', 'Please select one of these options. ')
    

# validation on smartphone selection 
def validateSmartphoneSelection(selected_smartphone):
    if selected_smartphone == '':
        return('Please choose one of these options.')
    
    
    
    

def main():
    ##############################################
    ################# first page #################
    ##############################################
    
    # display the title
    put_html("<h1>Mobile Access for Seniors Scheme </h1>")
    
    # display the header content 
    put_row([
        put_image(open('senior_digital.jpg', 'rb').read()),None,
        put_markdown("<p>Mobile Access for Seniors is a scheme that supports the Seniors Go Digital Programme.\
                  It provides subsidized smartphone and mobile plan to lower-income seniors who want to go digital, but cannot afford them.</p>")])
    
    put_html("<br>")
    put_warning(put_html("<p><b>NOTE:</b> You are required to fill in all the required fields in the application form, otherwise your eligibility check may be inaccurate. </p>"))
    # prompt the user for input to check for eligibility
    data = input_group("Check your eligibility!", [
        input("What is your age as of today? ", name = "age", type = NUMBER, placeholder = "Enter your age (e.g. 56) "),
        radio("What is your citizenship? ", name = "citizenship", options = ['Singapore Ctizen', 'Permanent Resident', 'Non-Singapore Citizen']),
        radio("What is your current beneficiary of the selected government assistance scheme?",
              name = "current_beneficiary",
              options = ['MSF ComCare Long Term Assistance (LTA)', 
                         'MSF ComCare Short-to-Medium Term Assistance (SMTA)', 
                         'HDB Public Rental Scheme',
                         'Others']),
        radio("Are you an existing IMDA Home Access beneficiary who has received a smartphone?",
              name = "existing_IMDA", 
              options = ['Yes', 'No'])], validate = validateCheckEligibility) 
    
    
    clear()
    
    
    
    ###############################################
    ################# second page #################
    ###############################################
    put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
    
    # eligible for mobile access scheme
    if (data['age'] >= 60 and data['age'] <= 100) and data['citizenship'] == 'Singapore Ctizen' and (data['current_beneficiary'] == 'MSF ComCare Long Term Assistance (LTA)' or data['current_beneficiary'] == 'MSF ComCare Short-to-Medium Term Assistance (SMTA)' or data['current_beneficiary'] == 'HDB Public Rental Scheme') and data['existing_IMDA'] == 'No':
        
        # display eligibility outcome 
        put_markdown("<br>")
        put_text("Validate your information... ")
        put_processbar('bar')
        for i in range(1, 11):
            set_processbar('bar', i/10)
            time.sleep(0.5)
        
        clear()
        put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
        put_markdown("<br>")
        put_success(put_markdown("<b>Eligibility Outcome:</b> Based on the information you have provided, you are eligible for Mobile Access for Seniors Scheme."))
        
        
        # prompt the user whether would like to apply for mobile access plan
        apply = actions('Do you wish to apply for mobile access plan?', [{'label': 'Yes, I wish to apply for mobile access plan', 'value': 'yes'},
                                                                         {'label': 'No, I do not wish to apply for mobile access plan', 'value': 'no'}])
        
        while True: 
            # if the user wish to apply for mobile access plan
            if apply == 'yes':
                clear()
                put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                put_markdown("<p>The table below illustrates the details of mobile access plan options for <b>eligible seniors only</b>.")
                # display the table to show the details of mobile access plan
                put_table([
                    ['M1', 'Singtel', 'Starhub', 'TPG'],
                    [span('2-Years Mobile Plan', col = 4)],
                    ['6 GB, 500 mins, 100 SMS', '5 GB, 250 mins, 50 SMS', '8 GB, 250 mins, 200 SMS', '20 GB, 300 mins, 30 SMS'],
                    [span('Smartphone', col = 4)],
                    ['Xiaomi Redmi 9A ($20)', 'OPPO A12 ($20)', 'Xiaomi Redmi 9A ($20)', 'Realme C11 ($20)'],
                    ['Huawei Y7 ($43)', 'Xiaomi Redmi 9A ($20)', 'Realme C21Y ($59)', 'Vivo Y15s ($39)'],
                    ['Samsung Galaxy A12 ($60)', 'Samsung Galaxy A12 ($60)', 'Samsung Galaxy A12 ($60)', 'OPPO A16 ($59)']]).style("text-align: center")
                
                put_html("<br>")
                put_warning(put_html("<p><b>NOTE:</b> You are required to fill in all the required fields in the application form, otherwise your application may be revoke. </p>"))
                # prompt the user for personal particular
                data1 = input_group("Sign Up for 2-Years Mobile Plan (Application Form)", [
                    input("Enter your full name as per in NRIC: ", name = "name", type = TEXT, placeholder = "Enter your name (e.g. David Leong)"),
                    input("Enter your NRIC: ", name = "identification", type = TEXT, placeholder = "Enter your identification number (e.g. S1234567D)"),
                    radio("Select your gender: ", name = "gender", options = [('Male', 'Male'), ('Female', 'Female')]),
                    input("Enter your date of birth: ", name = "dob", type = TEXT, placeholder = "Enter your date of birth (e.g. 13/11/1993)"),
                    input("Enter your home address: ", name = "address", type = TEXT, placeholder = "Enter your home address (e.g. Blk 485, Choa Chu Kang West Ave 4, #06-512, S670485)"),
                    input("Enter your email address: ", name = "email", type = TEXT, placeholder = "Enter your email address (e.g. abc@gmail.com)"),
                    radio("Select one telecom to sign up for 2-years mobile plan:", 
                          name = "telecom", 
                          options = ['M1', 'Singtel','Starhub','TPG'])], validate = validateApplicationForm)
                
                
                
                clear()
                put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                put_markdown("<p>The table below illustrates the details of mobile access plan options for <b>eligible seniors only</b>.")
                # display the table to show the details of mobile access plan
                put_table([
                    ['M1', 'Singtel', 'Starhub', 'TPG'],
                    [span('2-Years Mobile Plan', col = 4)],
                    ['6 GB, 500 mins, 100 SMS', '5 GB, 250 mins, 50 SMS', '8 GB, 250 mins, 200 SMS', '20 GB, 300 mins, 30 SMS'],
                    [span('Smartphone', col = 4)],
                    ['Xiaomi Redmi 9A ($20)', 'OPPO A12 ($20)', 'Xiaomi Redmi 9A ($20)', 'Realme C11 ($20)'],
                    ['Huawei Y7 ($43)', 'Xiaomi Redmi 9A ($20)', 'Realme C21Y ($59)', 'Vivo Y15s ($39)'],
                    ['Samsung Galaxy A12 ($60)', 'Samsung Galaxy A12 ($60)', 'Samsung Galaxy A12 ($60)', 'OPPO A16 ($59)']]).style("text-align: center")
                
                # prompt the user for preferred smartphone
                if data1['telecom'] == 'M1':
                    selected_smartphone = select("Select your preferred smartphone under M1 mobile plan: ",  ['','Xiaomi Redmi 9A','Huawei Y7', 'Samsung Galaxy A12'], validate = validateSmartphoneSelection)
                    
                    if selected_smartphone == 'Xiaomi Redmi 9A':
                        cost = 20.00
                    elif selected_smartphone == 'Huawei Y7':
                        cost = 43.00
                    else:
                        cost = 60.00
                    
                    mobile_plan = '6 GB, 500 mins, 100 SMS'
                
                elif data1['telecom'] == 'Singtel':
                    selected_smartphone = select("Select your preferred smartphone under Singtel mobile plan: ", ['','OPPO A12', 'Xiaomi Redmi 9A', 'Samsung Galaxy A12'], validate = validateSmartphoneSelection)
                    if selected_smartphone == 'OPPO A12':
                        cost = 20.00
                    elif selected_smartphone == 'Xiaomi Redmi 9A':
                        cost = 20.00
                    else:
                        cost = 60.00
                    
                    mobile_plan = '5 GB, 250 mins, 50 SMS'
                
                elif data1['telecom'] == 'Starhub':
                    selected_smartphone = select("Select your preferred smartphone under Starhub mobile plan: ",  ['','Xiaomi Redmi 9A', 'Realme C21Y', 'Samsung Galaxy A12'], validate = validateSmartphoneSelection)
                    if selected_smartphone == 'Xiaomi Redmi 9A':
                        cost = 20.00
                    elif selected_smartphone == 'Realme C21Y':
                        cost = 59.00
                    else:
                        cost = 60.00
                    
                    mobile_plan = '8 GB, 250 mins, 200 SMS'
                
                else:
                    selected_smartphone = select("Select your preferred smartphone under TPG mobile plan: ",  ['','Realme C11','Vivo Y15s','OPPO A16'], validate = validateSmartphoneSelection)
                    if selected_smartphone == 'Realme C11':
                        cost = 20.00
                    elif selected_smartphone == 'Vivo Y15s' :
                        cost = 39.00
                    else:
                        cost = 59.00
                    
                    mobile_plan = '20 GB, 300 mins, 30 SMS'
                
                
                clear()
                
                
                #####################################################
                ################# confirmation page #################
                #####################################################
                put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                
                # prompt the user to review the information are tabulated correctly before submission 
                put_markdown("""
                             <h2>Application Acknowledgement</h2>
                             """)
                put_markdown("""
                             <h4>Details of Application: </h4>
                             """)
                put_markdown("""
                             <p><b>NOTE: </b>Please kindly review the information that is correct before submission.</p>
                             """)
                put_table([[" ", "Information"],
                           ["Name: ", data1["name"]],
                            ["NRIC: ", data1["identification"]],
                            ["Gender: ", data1["gender"]],
                            ["Age: ", data["age"]],
                            ["Citizenship: ", data["citizenship"]],
                            ["Date of Birth: ", data1["dob"]],
                            ["Home Address: ", data1["address"]],
                            ["Email Address: ", data1["email"]],
                            ["Current Beneficiary: ", data["current_beneficiary"]],
                            ["Existing IMDA Home Access Beneficiary?: ", data["existing_IMDA"]],
                            ["Telecom: ", data1["telecom"]],
                            ["2-Years Mobile Plan: ", mobile_plan],
                            ["Selected Smartphone: ", selected_smartphone],
                            ["Price of a smartphone:", put_text("S${:.2f}".format(cost))]]).style("text-align: left")
            
                popup("Warning Message", "Please be informed that if you wish to make any amendments to the current application form, you will have to create a new application form before submission.  All information that has been captured previously will be cleared from the system immediately if you wish to create a new application form.")
                
                # prompt the user whether would like to create a new application form
                amend = actions("Do you wish to create a new application form for amendment? ", [{'label': 'Yes, I wish to create a new application form for amendment', 'value': 'yes'},
                                                                                {'label': 'No, I do not wish to create a new application form for amendment', 'value': 'no'}])
                
                if amend == 'yes':
                    
                    put_markdown("<br>")
                    put_text("Please wait while we are preparing a new application form ...  ")
                    put_processbar('bar')
                    for i in range(1, 11):
                        set_processbar('bar', i/10)
                        time.sleep(0.5)
                    continue
                
                else:
                    
                    # prompt the user whether would like to submit the application form
                    submit = actions('Do you wish to submit this application? ', [{'label': 'Yes, I wish to submit this application', 'value': 'yes'}, 
                                                                                  {'label': 'No, I do not wish to submit this application', 'value': 'no'}])
                    
                    # if submission is true, display a confirmation message that the application form has been successfully submitted
                    if submit == 'yes':
                        popup("Successful Message",
                              "Your application has been successfully submitted. The relevant department will review your application and notify you within 2 weeks from the date of submission.")
                        if popup:
                            clear()
                            put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                            put_text("Thank you for using our app!")
                            put_text("Have a great day ahead!")
                            put_markdown("""
                                         <b>Remarks:</b><br> Please be advised to refresh this website if you wish to check your eligibility and/or submit the application form.
                                         """)
                                        
                            break
                    # if submission is false, display a message
                    else:
                        clear()
                        put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                        put_text("Thank you for using our app!")
                        put_text("Have a great day ahead!")
                        put_markdown("""
                                     <b>Remarks:</b><br> Please be advised to refresh this website if you wish to check your eligibility and/or submit the application form.
                                     """)
                        break
                    
            # if the user do not wish to apply for mobile access plan 
            else:
                clear()
                put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
                put_text("Thank you for using our app!")
                put_text("Have a great day ahead!")
                put_markdown("""
                             <b>Remarks:</b><br> Please be advised to refresh this website if you wish to check your eligibility and/or submit the application form.
                             """)
                break
            
    ######################################################
    ################# ineligibility page #################
    ######################################################
    else:
        # display ineligibility outcome 
       put_markdown("<br>")
       put_text("Validate your information... ")
       put_processbar('bar')
       for i in range(1, 11):
           set_processbar('bar', i/10)
           time.sleep(0.5)
    
       clear()
       put_markdown('<h1>Mobile Access for Seniors Scheme </h1>')
       put_markdown("<br>")
       put_error(put_markdown("<b>Eligibility Outcome:</b> You have not met one or more requirement(s). As such, you are <b>ineligible</b> for Mobile Access for Seniors Scheme."))
       put_text("Thank you for using our app!")
       put_text("Have a great day ahead!")
       put_markdown("""
                    <b>Remarks:</b><br> Please be advised to refresh this website if you wish to check your eligibility and/or submit the application form.
                    """)
        
    
app.add_url_rule('/checkeligibility', 'webio_view', webio_view(main), methods = ['POST', 'GET', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port)

#if __name__ == "__main__":
    #app.run(host = "localhost", port = 80)
