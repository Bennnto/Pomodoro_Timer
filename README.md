# POMODORO TIMER (TERMINAL & GUI VERSION)
    - This Simple Pomodoro Timer write in Python use built-in and package module 
    - Files 
        1. pomodoro.py (Terminal Version)
        2. pomodoro_gui.py (GUI Version)

    - How it works 
        This Program work from execute python files 

   - Python Modules
   
| No. | Module | Functions           |
|-----|--------|----------------------|
| 1.  | sys    | stdin and stdout |
| 2.  | argparse | parser argument |
| 3.  | Threading | concurrent program |
| 4.  | Tkinter | graphic user interface |

    - Functions and Execution
    
| No. | Functions | Execution |
|-----|-----------|-----------|
| 1.  | Start timer with default work time | ```python3 pomodoro.py ```|
| 2.  | Start with set work time | ```python3 pomodoro.py --work [minutes]``` |
| 3.  | Start with set work time and break time | ```python3 pomodoro.py --work [minutes] --short [minutes] --long [minutes]``` |
| 4.  | start with set work time, break time and cycles |```python3 pomodoro.py --work [minutes] --short [minutes] --long [minutes] --cycles [int]``` |
| 5.  | Control Pause | ```p``` |
| 6.  | Control Resume | ```r``` |
| 7.  | Control Exit | ```q``` |
| 8.  | Start GUI | ```python3 pomodoro_gui.py``` |

