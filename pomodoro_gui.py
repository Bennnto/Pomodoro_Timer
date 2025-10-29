import tkinter as tk 
from tkinter import ttk
import threading
from pomodoro import Pomodoro

class PomodoroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x400")  # Square window
        self.root.resizable(False, False)  # Prevent resizing
        self.setup_ui()
    
    def setup_ui(self):
        # Create main square frame that fills the window
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Large Time display in center
        self.time_label = tk.Label(self.main_frame, font=("Arial", 48, "bold"), 
                                 bg="#2c3e50", fg="white", text="25:00")
        self.time_label.pack(expand=True)
        
        # State label below time
        self.state_label = tk.Label(self.main_frame, font=("Arial", 16), 
                                  bg="#2c3e50", fg="#ecf0f1", text="READY")
        self.state_label.pack()
        
        # Single control button at bottom
        self.control_button = tk.Button(self.main_frame, text="START", 
                                      font=("Arial", 14, "bold"),
                                      bg="#3498db", fg="white",
                                      command=self.toggle_timer,
                                      width=10, height=2)
        
        self.reset_button = tk.Button(self.main_frame, text="RESET", 
                                    font=("Arial", 14, "bold"), 
                                    bg="#e74c3c", fg="white",
                                    command=self.reset_timer, 
                                    width=10, height=2)

        self.control_button.pack(pady=10)
        self.reset_button.pack(pady=10)
        
        # Initialize timer
        self.timer = Pomodoro()
        self.gui_state = "ready"
        self.is_running = False

    def update_display(self):
        #update GUI elements
        self.time_label.config(text=f"{mins:02d} : {secs:02d}")
        self.progress['value'] = progress_percentage

    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()
    
    def start_timer(self):
        self.timer.start()
        self.is_running = True
        self.gui_state = "running"
        self.control_button.config(text="PAUSE", bg="#e74c3c")
        self.state_label.config(text="WORKING", fg="#e74c3c")
        self.schedule_update()
    
    def pause_timer(self):
        self.timer.pause()
        self.is_running = False
        self.gui_state = "paused"
        self.control_button.config(text="RESUME", bg="#f39c12")
        self.state_label.config(text="PAUSED", fg="#f39c12")
    
    def stop_timer(self):
        self.timer.stop()
        self.is_running = False
        self.gui_state = "ready"
        self.control_button.config(text="START", bg="#3498db")
        self.state_label.config(text="READY", fg="#ecf0f1")
        self.time_label.config(text="25:00")
    
    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.gui_state = "ready"
        self.control_button.config(text="START", bg="#3498db")
        self.state_label.config(text="READY", fg="#ecf0f1")
        self.time_label.config(text="25:00")
        # Reset the timer object
        self.timer = Pomodoro()

    def update_display(self):
        if self.is_running:
            # Get remaining time from timer
            with self.timer.lock:
                if self.timer._running and not self.timer._paused:
                    elapsed = self.timer.now() - self.timer._start_monotonic - self.timer._elapsed_while_paused
                    remaining = self.timer._current_duration - elapsed
                    if remaining > 0:
                        mins = int(remaining) // 60
                        secs = int(remaining) % 60
                        self.time_label.config(text=f"{mins:02d}:{secs:02d}")
                        
                        # Update state based on timer state
                        if self.timer._state == 'work':
                            self.state_label.config(text="WORKING", fg="#e74c3c")
                        else:
                            self.state_label.config(text="BREAK", fg="#27ae60")
        
        if self.gui_state == "running":
            self.root.after(1000, self.update_display)


    def schedule_update(self):
        self.update_display()


if __name__ == "__main__":
    app = PomodoroGUI()
    app.root.mainloop()
    
