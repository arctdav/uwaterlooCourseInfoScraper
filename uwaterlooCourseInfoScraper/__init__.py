# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup
from typing import List

#!######################### Get Course Prefix ##################################
# * Get prefix from: schedule of classes for undergraduate students
def getPrefix() -> List[str]:
    """
    Get the most up-to-date course prefix list from http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html

    Params:
        None
    
    Return:
        List[str]
    """
    course_prefix = []

    # Access the course prefix website
    prefix_page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html')

    # Parse the accessed website page
    prefix_soup = BeautifulSoup(prefix_page.text, 'html.parser')

    # Since all prefix are under select tag in HTML, scrap the information by the select tag.
    all_select = prefix_soup.find_all('select')
    second_select = all_select[1]
    second_select_all_option = second_select.find_all('option')
    for i in second_select_all_option:
        course_prefix.append(i.get('value'))
    return course_prefix

def requestCourseEnroll(sess, subject, cournum):
    """
    Get a request instance from http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl
    after requesting the class enrollment data

    Params:
        sess: int or str
        subject: str
        cournum: int or str
    
    Return:
        Request instance
    """
    try:
        if not sess or not subject or not cournum:
            print("ERROR: please input ALL of the sess, subject, cournum parameters")
            return None
        else:
            url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    
            headers = {"Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "45",
            "Origin": "http://www.adm.uwaterloo.ca",
            "Connection": "keep-alive",
            "Referer": "http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html",
            "Upgrade-Insecure-Requests": "1"}
                
            data = "level=under&sess=%s&subject=%s&cournum=%s" % (sess, subject.upper(), cournum)
    
            req = requests.post(url, headers=headers, data=data)
    
            if req.status_code == requests.codes.ok:
                print("Request Successful")
                return req
            else:
                print("Request ERROR: %s" % req.status_code)
                return req
    except Exception as e:
        print(f"ERROR: requestCourseEnroll -> {e}")
        raise

def getCourseEnrollInfo(sess, subject, cournum):
    """
    Get the section information, in list of tuples 

    Params: 
        sess: int or str
        subject: str
        cournum: int or str

    Return:
        List[Dict("Class": int, "CompSec": str, "EnrlCap": int, "EnrlTot": int, "Instructor": str)]
    """
    try:
        if sess <= 1000 or int(sess) <= 1000 or not subject or cournum < 100 or 1000 <= cournum \
            or int(cournum) < 100 or 1000 < int(cournum):
            raise AssertionError("Wrong Parameters, sess <= 1000 or int(sess) <= 1000 or not subject or cournum < 100 or 1000 < cournum \
            or int(cournum) < 100 or 1000 < int(cournum)")
        req = requestCourseEnroll(sess, subject, cournum)
        if req == None or req.status_code != requests.codes.ok:
            raise AssertionError("Request to server is unsuccessful")
        # * Create a BeautifulSoup object
        soup = BeautifulSoup(req.text, 'html.parser')
        enrollTable = soup.find(border="2")

        # * This course does not exist this term
        if len(enrollTable.contents) == 1:
            return [{"Class": -1, "CompSec": "No Result", "EnrlCap": -1, "EnrlTot": -1, "Instructor": "No Result"}]
        
        # * Request successful, not parsing a not existing course, all params correct
        # * each row in the HTML table 
        alltr = enrollTable.find_all("tr")
        targetTableRows = alltr[2].find_all("tr")
        #print(targetTableRows[7].contents)
        if not targetTableRows:
            targetTableRows = alltr[3].find_all("tr")
        
        # * parse the each row in targetTableRows
        res = []
        for tr in targetTableRows:
            if len(tr) == 13:
                Class_th = tr.contents[0]
                CompSec_th = tr.contents[1]
                EnrlCap_th = tr.contents[6]
                EnrlTot_th = tr.contents[7]
                Instructor_th = tr.contents[12]
                res.append({"Class": int(Class_th.getText().strip()), "CompSec": CompSec_th.getText().strip(),\
                     "EnrlCap": int(EnrlCap_th.getText().strip()), "EnrlTot": int(EnrlTot_th.getText().strip()), "Instructor": Instructor_th.getText().strip()})
        print(res)
        return res
                

    except RuntimeError as re:
        raise re
    except AssertionError as ae:
        #print(ae)
        raise ae
    except Exception as e:
        print(f"ERROR: getCourseEnrollInfo -> {e}")
        raise
