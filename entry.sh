#!/bin/bash
if [[ $DATABASE_URL ]]
then
  alembic upgrade head
  scrapyd &
  sleep 5
  scrapyd-deploy local
  python run.py
fi
