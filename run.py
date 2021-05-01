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
            'http://localhost/schedule.json',
            {
                'project': 'produkto_sercxilo',
                'spider': spider,
            }
        )
    sleep(10800)
