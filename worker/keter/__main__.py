import os
import sys
from pathlib import Path
from fire import Fire
from redis import Redis
import keter

def _work(queue, job=None, params=None):
    if job:
        try:
            if params:
                getattr(keter, job)(**params)
            else:
                getattr(keter, job)()
        except AttributeError as e:
            if "module 'keter'" not in str(e):
                raise e
            print(f"Error: No job named {job}.")
            print(f"Some possibilites: {', '.join([i for i in dir(keter) if i[0].islower()])}.")
            sys.exit(-1)
    if queue in ['cpu', 'gpu', 'all']:
        keter.work(queue)
    elif queue == 'none':
        pass
    else:
        print(f"Error: Queue {queue} is unsupported")
        sys.exit(-1)

class Controller:
    """
    Available commands: up, work.
    
    See specific commands for built-in help.
    """

    def up(self, queue='all'):
        """
        Run the foreman job and listen for more jobs.

        Keyword arguments:
        queue -- What queue to listen for (eg. gpu, cpu). Use "all" to listen for anything. 
        """
        keter.foreman()
        _work(queue)

    def work(self, queue='all', job='', params=''):
        """
        Spawn a worker and listen for new jobs.
        
        Keyword arguments:
        queue -- What queue to listen for (eg. gpu, cpu). Use "all" to listen for anything. 
                 The queue "none" can be used with the job param to just execute a job.
        job -- Job to execute before joining the queue.
        params -- Job parameters if applicable.
        """
        _work(queue, job, params)

def main():
    Fire(Controller)
