import threading
import sys
import argparse
import time


class Pomodoro() :
    def __init__(self, work=25*60, short_break=5*60, long_break=15*60, cycles_before_long=4):
        self.work = work
        self.short_break = short_break
        self.long_break = long_break
        self.cycle_before_long = cycles_before_long
        
        self.lock = threading.Lock()
        self._running = False
        self._paused = False
        self._start_monotonic = None
        self._pause_monotonic = None
        self._elapsed_while_paused = 0
        self._state = 'ready' #ready, work break
        self._cycle_count = 0
        self._current_duration = work
        
    def now(self):
        return time.monotonic()
    
    def start(self):
        with self.lock:
            if self._running:
                return
            self._running = True
            self._paused = False
            self._start_monotonic = self.now()
            self._elapsed_while_paused = 0
            self._state = 'work'
            self._current_duration = self.work
        threading.Thread(target=self._run_loop, daemon=True).start()
        
    def pause(self):
        with self.lock:
            if not self._running or self._paused:
                return
            self._pause_monotonic = self.now()
            self._paused = True
            
    def resume(self):
        with self.lock:
            if not self._running or not self._paused:
                return
            paused_for = self.now() - self._pause_monotonic   
            self._elapsed_while_paused += paused_for
            self._paused = False
            self._pause_monotonic = None     
            
    def stop(self):
        with self.lock:
            self._running = False
    
    def _run_loop(self):
        while True:
            with self.lock:
                if not self._running:
                    break
                if self._paused:
                    pass
                else:
                    elapsed = self.now() - self._start_monotonic - self._elapsed_while_paused
                    remaining = self._current_duration - elapsed
                    if remaining <= 0:
                        #Transition to next stage
                        if self._state == 'work':
                            self._cycle_count += 1
                            #Decide break type
                            if self._cycle_count % self.cycle_before_long == 0:
                                self._state = 'break'
                                self._current_duration = self.long_break
                                print('\nWork done - Time for a long break!')
                            else:
                                self._state = 'break'
                                self._current_duration = self.short_break
                                print('\nWork done - Time for a short break!')
                        else : 
                            #afterbreak => Start Work
                            self._state = 'work'
                            self._current_duration = self.work
                            self._start_monotonic = self.now()
                            self._elapsed_while_paused = 0
                            print('\nBreak over - Starting Work')
                            continue
                        #Set new start for break
                        self._start_monotonic = self.now()
                        self._elapsed_while_paused = 0
                        continue
                    #Print remaining every second
                    mins = int(remaining) // 60
                    secs = int(remaining) % 60
                    
                    sys.stdout.write(f"\r[{self._state.upper()}] {mins:02d} : {secs:02d}")
                    sys.stdout.flush()
            time.sleep(0.5)
            
def run_cli():
    parser = argparse.ArgumentParser(description='Pomodoro Timer')
    parser.add_argument("--work", type=int, default=25, help="Work duration in minutes (default : 25)")
    parser.add_argument("--short", type=int, default=5, help="Short break duration in minutes (default : 5)")
    parser.add_argument("--long", type=int, default=15, help="Long break duration in minutes (default : 15)")
    parser.add_argument("--cycles", type=int, default=4, help="Number of work cycle before long break (default : 4)")
    args = parser.parse_args()

    timer = Pomodoro(work=args.work*60, short_break=args.short*60, long_break=args.long*60, cycles_before_long=args.cycles)
    print("\nStart Pomodoro : Control p = pause, r = resume, s = stop, q = exit\n")
    timer.start()
    try:
        while True:
            ch = sys.stdin.read(1)
            if not ch:
                break
            ch = ch.lower()
            if ch == 'p' :
                timer.pause()
                print("\nPaused")
            elif ch == 'r' :
                timer.resume()
                print('\nResumed')
            elif ch == 's' :
                timer.stop()
                print('\nStopped')
            elif ch == 'q' :
                timer.stop()
                print('\nExiting')
                break
    except KeyboardInterrupt:
        timer.stop()
        print('\nInterrupted Exiting')
        
if __name__ == "__main__":
    run_cli()
