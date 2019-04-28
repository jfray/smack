#!/usr/bin/env python

import django_rq
q = django_rq.get_failed_queue()
while True:
    job = q.dequeue()
    if not job:
        break
    job.delete()  # Will delete key from Redis
