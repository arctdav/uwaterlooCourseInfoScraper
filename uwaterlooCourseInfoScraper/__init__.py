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

    Parameters:
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

    Parameters:
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
    try:
        req = requestCourseEnroll(sess, subject, cournum)
        
        # Create a BeautifulSoup object
        soup = BeautifulSoup(req.text, 'html.parser')
        #print(soup.prettify())
        print(soup.find(border="2").contents)
        enrollTable = soup.find(border="2")
        
    except Exception as e:
        print(f"ERROR: getCourseEnrollInfo -> {e}")
        raise




"""


    Return:
        List[tuple(int, int)], [(Enrl Cap, Enrl Tot), ...]
"""
try:
    sess, subject, cournum = 1201, "Cs", 135
    
    if sess <= 1000 or not subject or cournum < 100:
        raise AssertionError("Wrong Parameters, sess <= 1000 or not subjet or cournum < 100")
    req = requestCourseEnroll(sess, subject, cournum)
    if req == None or req.status_code != requests.codes.ok:
        raise AssertionError("Request to server is unsuccessful")
    # Create a BeautifulSoup object
    soup = BeautifulSoup(req.text, 'html.parser')
    enrollTable = soup.find(border="2")
    if len(enrollTable.contents) == 1:
        print([(0, 0)]) # TODO: turn to return when joining
    
    # Request successful, not parsing a not existing course, all params correct
    alltr = enrollTable.find_all("tr")
    print(alltr[0].contents)
    
except AssertionError as ae:
    print(ae)
    raise
except Exception as e:
    print(f"ERROR: getCourseEnrollInfo -> {e}")
    raise


