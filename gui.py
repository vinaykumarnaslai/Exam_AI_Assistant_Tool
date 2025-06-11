# gui.py
import tkinter as tk
from PIL import ImageGrab
import pyautogui
import time
from datetime import datetime
from ocr_engine import extract_text_from_image
from gpt_answer import get_answer_from_gpt
from tkinter import messagebox
import screeninfo
import pyttsx3
import tkinter as tk
from tkinter import filedialog, messagebox
import pyttsx3
import pyperclip
from fpdf import FPDF
import threading

# Global engine for stopping speech
tts_engine = pyttsx3.init()

def open_floating_window():
    window = tk.Tk()
    window.title("AI Exam Assistant")
    window.geometry("300x200+100+100")
    window.attributes('-topmost', True)
    window.resizable(False, False)

    label = tk.Label(window, text="AI Assistant Ready", font=("Arial", 14))
    label.pack(pady=20)

    screenshot_button = tk.Button(window, text="Capture Screenshot", command=select_region)
    screenshot_button.pack(pady=10)

    window.mainloop()

def select_region():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.config(bg='black')

    canvas = tk.Canvas(root, cursor="cross", bg='gray')
    canvas.pack(fill=tk.BOTH, expand=True)

    start_x = start_y = 0
    rect = None

    def on_mouse_down(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_mouse_drag(event):
        nonlocal rect
        canvas.delete("rect")
        rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='red', width=2, tag="rect")

    def on_mouse_up(event):
        end_x, end_y = event.x, event.y
        root.destroy()
        time.sleep(0.2)  # Let screen stabilize
        capture_and_save(min(start_x, end_x), min(start_y, end_y), max(start_x, end_x), max(start_y, end_y))

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

def show_answer_popup(question, answer):
    def speak_text():
        def run_tts():
            tts_engine.say(answer)
            tts_engine.runAndWait()
        threading.Thread(target=run_tts, daemon=True).start()

    def stop_speaking():
        tts_engine.stop()

    def copy_to_clipboard():
        pyperclip.copy(answer)
        messagebox.showinfo("Copied", "Answer copied to clipboard!")

    def save_to_file():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt")]
        )
        if file_path:
            if file_path.endswith(".pdf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in answer.split("\n"):
                    pdf.multi_cell(0, 10, line)
                pdf.output(file_path)
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(answer)
            messagebox.showinfo("Saved", f"Saved to {file_path}")

    # Popup Window
    window = tk.Toplevel()
    window.title("AI Answer")
    window.geometry("500x400")
    window.attributes('-topmost', True)

    # Canvas + Scrollbar
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Question + Answer Labels
    tk.Label(scroll_frame, text="Question:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    tk.Label(scroll_frame, text=question, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=5)

    tk.Label(scroll_frame, text="Answer:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    tk.Label(scroll_frame, text=answer, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=5)

    # Button Frame
    button_frame = tk.Frame(scroll_frame)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="🔊 Read", command=speak_text).pack(side="left", padx=5)
    tk.Button(button_frame, text="🛑 Stop", command=stop_speaking).pack(side="left", padx=5)
    tk.Button(button_frame, text="📋 Copy", command=copy_to_clipboard).pack(side="left", padx=5)
    tk.Button(button_frame, text="📝 Save", command=save_to_file).pack(side="left", padx=5)

    window.mainloop()



def capture_and_save(x1, y1, x2, y2):
    # Limit the region to screen size
    screen = screeninfo.get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height

    x1 = max(0, min(x1, screen_width))
    y1 = max(0, min(y1, screen_height))
    x2 = max(0, min(x2, screen_width))
    y2 = max(0, min(y2, screen_height))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    img = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    img.save(filename)
    print(f"✅ Screenshot saved as '{filename}'")

    time.sleep(0.3)
    text = extract_text_from_image(filename)
    print("\n🧠 Extracted Text:\n", text)

    from gpt_answer import get_answer_from_gpt
    answer = get_answer_from_gpt(text)
    print("\n💡 AI Answer:\n", answer)

    # Show answer in popup
    show_answer_popup(text, answer)
