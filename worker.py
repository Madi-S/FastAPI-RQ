from time import sleep


def sleep_task(seconds: int = 5):
    print('Starting the task ...')
    sleep(seconds)
    
    print('Finished the task ...')
    return {'status': 'completed'}