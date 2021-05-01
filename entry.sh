#!/bin/bash
alembic upgrade head
scrapyd &
sleep 5
scrapyd-deploy local
python run.py