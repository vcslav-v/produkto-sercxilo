import requests
from time import sleep

spiders = [
    'anthonyboyd_spider',
    'mrmockup_spider',
    'pb_spider',
]

while True:
    for spider in spiders:
        requests.post(
            'http://0.0.0.0:80/schedule.json',
            {
                'project': 'produkto_sercxilo',
                'spider': spider,
            }
        )
    sleep(10800)
