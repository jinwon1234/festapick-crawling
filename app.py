from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from fastapi import FastAPI
from crawler import ulsan_cralwer, daegu_crawler

app = FastAPI()

atexit.register(lambda: scheduler.shutdown())
scheduler = BackgroundScheduler(timezone="Asia/Seoul")
scheduler.add_job(ulsan_cralwer.ulsanCrawling, 'cron', hour=21, minute=37)
scheduler.add_job(daegu_crawler.daegCrawling, 'cron', hour=22, minute=48)
scheduler.start()