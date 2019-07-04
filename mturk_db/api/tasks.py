from celery import shared_task


@shared_task(bind=True, name='tasks.create_batch')
def create_batch(self, x, y):
    print('started task ##################')
    for i in range(10):
        import time
        time.sleep(2)
        self.update_state(
            state='PROGRESS',
            meta={'current': i, 'total': 10}
        )

    return x + y