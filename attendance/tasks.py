from celery import shared_task, task
import requests, datetime

@task
def add(a=3,b=1):
    return a+b

@task
def ping():
    r = requests.post("https://requestb.in/1dvp3ch1",{"hello":"World"})
    return r.status_code