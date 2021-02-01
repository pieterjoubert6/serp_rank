###Installing

*  Change run_crawler and crontab to contain the correct paths
*  Add InfluxDB config parameters to conf.py   
*  pip install -r requirements.txt
*  Add crontab item to crontab and change folder path to correct user

###Populate data

*  scrapy runspider populate_influxbd.py