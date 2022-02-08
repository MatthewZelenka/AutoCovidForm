# from lib.google import autoLogin, formFiller
from lib import google
from dataclasses import dataclass
from autoCovidForm import * # from lib.webScraper import *
import time

form = "https://docs.google.com/forms/d/e/1FAIpQLSedNWLgRdQKVfNqT4gwYrq0PEJqj2vnOL5GHqfopjwnakC-0g/viewform"

# page procedures when in yrdsb login page
@dataclass
class yrdsbRedirect:
    url = "https://google.yrdsb.ca/EasyConnect/"
    def doPage(self, profile):
        print("YRDSB redirection...")

@dataclass
class yrdsbLogin:
    url = "https://google.yrdsb.ca/LoginFormIdentityProvider/Login.aspx?"
    def doPage(self, profile):
        print("Logging in to YRDSB...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "UserName")))
        login = self.driver.find_element(By.ID, "UserName")
        login.send_keys(profile["user"]["userName"])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
        login = self.driver.find_element(By.ID, "Password")
        login.send_keys(profile["user"]["password"])
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "LoginButton")))
        self.driver.find_element(By.NAME, "LoginButton").click()

def fillForm(self, profile):
    # does google login and attaches yrdsb login code
    google.autoLogin.login(self=self, profile=profile, pageProcedures=[yrdsbRedirect, yrdsbLogin])

    # fills google form
    currentUrl = self.driver.current_url
    if google.formFiller.getFormState(self) == "uncomplete": # fills out form 
        print("Filling out form...")
        google.formFiller.clearAll(self)

        firstName = google.formFiller.textbox(question="Student First Name *", answer=profile["formInfo"]["firstName"])
        lastName = google.formFiller.textbox(question="Student Last Name *", answer=profile["formInfo"]["lastName"])
        covidScreeningV1 = google.formFiller.multipleChoice(question="Have you completed the self-screening test? *\nCOVID 19 School and Child Care Screening Tool is available at https://covid-19.ontario.ca/school-screening/", answer=["Yes"])
        covidScreeningV2 = google.formFiller.multipleChoice(question="Have you completed the self-screening test? *\nCOVID 19 School and Child Care Screening Tool is available at https://covid-19.ontario.ca/school-screening/ *Important Update: The Ministry Of Education and the Chief Medical Officer of Health https://www2.yrdsb.ca/sites/default/files/2022-01/EDU-JointParentsLetterJanuary182022-EN.pdf have provided additional information that may affect your screening results, including:", answer=["Yes"])

        google.formFiller.fillForm(self, firstName, lastName, covidScreeningV1, covidScreeningV2)
        time.sleep(5)
        google.formFiller.submit(self)
    print("Form is {}".format(google.formFiller.getFormState(self)))
    self.waitUrlChange(currentUrl)
    
def createProfile():
    pass