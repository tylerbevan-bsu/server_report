#!python3
import globus_sdk
import pickle
import os
from subprocess import call
import sys
import sqlite3 as lite
import server_report.auth as auth

def list_endpoints():
    tc = auth.authenticate()
    print("My Managed Endpoints:")
    for ep in tc.endpoint_manager_monitored_endpoints():
        print("[{}] {}".format(ep["id"], ep["display_name"]))

def user_frequency(endpointid, startdate, enddate):
    tc = auth.authenticate()
    con = lite.connect(':memory:')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE People(Name TEXT)")
        for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_completion_time="{},{}".format(str(startdate), str(enddate))):
            cur.execute("INSERT INTO People VALUES(\'{}\')".format(task["owner_string"]))
        cur.execute("SELECT Name, count(*) FROM People GROUP BY Name ORDER BY count(*) DESC")
        for row in cur:
            print('{}\t{}'.format(row[1], row[0]))

def job_count(endpointid, startdate, enddate):
    tc = auth.authenticate()
    con = lite.connect(':memory:')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE Jobs(Name TEXT)")
        for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_completion_time="{},{}".format(str(startdate), str(enddate))):
            cur.execute("INSERT INTO Jobs VALUES(\'{}\')".format(task["owner_string"]))
        cur.execute("SELECT count(*) FROM Jobs")
        for row in cur:
            print('{}'.format(row[0]))

def running_count(endpointid):
    tc = auth.authenticate()
    con = lite.connect(':memory:')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE Jobs(Name TEXT)")
        for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_status="ACTIVE"):
            cur.execute("INSERT INTO Jobs VALUES(\'{}\')".format(task["owner_string"]))
        cur.execute("SELECT count(*) FROM Jobs")
        for row in cur:
            print('{}'.format(row[0]))

