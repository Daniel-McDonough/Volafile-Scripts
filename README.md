## Volafile is now defunct

These are random volafile scripts designed for downloading and filtering files. There are two types of scripts: random utilities and a redis-based queueing system.

### Utilities:

vola-grep-links.py: Returns URLs of files in a room

vola-links.py: Old method to pull URLs from room

voladownload.sh: Downloads Vola links via proxychains

wget-list: Uses wget to download Vola URLs in succession

partial-cleanup.sh: Cleans up partially downloaded files



### The queue-based downloader is:

utilities -> redis -> vola downloader worker

clipboard-check.sh: Checks clipboard for volafile links and adds to redis queue.

vola-get-all-links.py: Read all links from a room and add to redis queue

download-redis.sh: Worker that reads from redis and downloads vola links

redis-load.sh:  Read from a file and load to redis

redis-redrive-failed.sh: Sends links from failed queue back into the processing queue

vola-downloader.sh: Old downloader that uses proxychains

vola-watcher.py: Watches a room and sends matching links to redis

