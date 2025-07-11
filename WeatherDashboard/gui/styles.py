"""
Style configuration for GUI elements.
"""

from tkinter import ttk


def configure_styles() -> None:
    '''Configures the styles for the GUI elements.'''
    style = ttk.Style()
    style.configure("FrameLabel.TLabelframe.Label", font=('Arial', 15, 'bold'))
    style.configure("LabelName.TLabel", font=('Arial', 10, 'bold'))
    style.configure("LabelValue.TLabel", font=('Arial', 10))
    style.configure("MainButton.TButton", font=('Arial', 10, 'bold'), padding=5)
    style.configure("Title.TLabel", font=('Comic Sans MS', 20, 'bold'))
    
    style.configure("TNotebook", background="lightgray")
    style.configure("TNotebook.Tab", padding=[12, 8], font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab",
             background=[("selected", "lightblue"), ("active", "lightgreen")],
             foreground=[("selected", "darkblue"), ("active", "darkgreen")])