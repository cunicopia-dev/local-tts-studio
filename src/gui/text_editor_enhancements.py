"""Text editor enhancements for better text editing experience."""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from typing import Optional


class FindReplaceDialog:
    """Find and replace dialog for text widgets."""
    
    def __init__(self, parent, text_widget):
        self.parent = parent
        self.text_widget = text_widget
        self.dialog = None
        self.find_var = tk.StringVar()
        self.replace_var = tk.StringVar()
        self.case_sensitive = tk.BooleanVar()
        self.use_regex = tk.BooleanVar()
        self.current_match = None
        
    def show(self):
        """Show the find/replace dialog."""
        if self.dialog:
            self.dialog.lift()
            self.dialog.focus()
            return
            
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Find and Replace")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self._create_widgets()
        self._bind_events()
        
        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
        # Focus on find entry
        self.find_entry.focus()
        
    def _create_widgets(self):
        """Create dialog widgets."""
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Find section
        ttk.Label(main_frame, text="Find:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.find_entry = ttk.Entry(main_frame, textvariable=self.find_var, width=40)
        self.find_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Replace section
        ttk.Label(main_frame, text="Replace:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.replace_entry = ttk.Entry(main_frame, textvariable=self.replace_var, width=40)
        self.replace_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # Options
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(options_frame, text="Case sensitive", 
                       variable=self.case_sensitive).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(options_frame, text="Use regex", 
                       variable=self.use_regex).pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(button_frame, text="Find Next", 
                  command=self.find_next).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Replace", 
                  command=self.replace_current).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Replace All", 
                  command=self.replace_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Close", 
                  command=self.close).pack(side=tk.RIGHT, padx=2)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        
    def _bind_events(self):
        """Bind keyboard events."""
        self.dialog.bind('<Return>', lambda e: self.find_next())
        self.dialog.bind('<Escape>', lambda e: self.close())
        self.find_entry.bind('<Return>', lambda e: self.find_next())
        self.replace_entry.bind('<Return>', lambda e: self.replace_current())
        
        # Handle dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        
    def find_next(self):
        """Find the next occurrence."""
        search_text = self.find_var.get()
        if not search_text:
            return
            
        # Get current cursor position
        start_pos = self.text_widget.index(tk.INSERT)
        
        try:
            if self.use_regex.get():
                # Use regex search
                flags = 0 if self.case_sensitive.get() else re.IGNORECASE
                pattern = re.compile(search_text, flags)
                
                # Get all text from current position to end
                content = self.text_widget.get(start_pos, tk.END)
                match = pattern.search(content)
                
                if match:
                    # Calculate absolute position
                    match_start = f"{start_pos}+{match.start()}c"
                    match_end = f"{start_pos}+{match.end()}c"
                    
                    self._highlight_match(match_start, match_end)
                    return True
                    
            else:
                # Use simple text search
                if self.case_sensitive.get():
                    pos = self.text_widget.search(search_text, start_pos, tk.END)
                else:
                    pos = self.text_widget.search(search_text, start_pos, tk.END, nocase=True)
                    
                if pos:
                    end_pos = f"{pos}+{len(search_text)}c"
                    self._highlight_match(pos, end_pos)
                    return True
                    
        except re.error as e:
            messagebox.showerror("Regex Error", f"Invalid regular expression: {e}")
            return False
            
        # Not found, try from beginning
        if start_pos != "1.0":
            self.text_widget.mark_set(tk.INSERT, "1.0")
            return self.find_next()
        else:
            messagebox.showinfo("Not Found", f"'{search_text}' not found.")
            return False
            
    def _highlight_match(self, start, end):
        """Highlight a text match."""
        # Clear previous selection
        self.text_widget.tag_remove(tk.SEL, "1.0", tk.END)
        
        # Select and highlight the match
        self.text_widget.tag_add(tk.SEL, start, end)
        self.text_widget.mark_set(tk.INSERT, end)
        self.text_widget.see(start)
        
        self.current_match = (start, end)
        
    def replace_current(self):
        """Replace the current selection."""
        if not self.current_match:
            self.find_next()
            return
            
        start, end = self.current_match
        replace_text = self.replace_var.get()
        
        self.text_widget.delete(start, end)
        self.text_widget.insert(start, replace_text)
        
        # Move cursor and find next
        new_end = f"{start}+{len(replace_text)}c"
        self.text_widget.mark_set(tk.INSERT, new_end)
        self.current_match = None
        self.find_next()
        
    def replace_all(self):
        """Replace all occurrences."""
        search_text = self.find_var.get()
        replace_text = self.replace_var.get()
        
        if not search_text:
            return
            
        count = 0
        self.text_widget.mark_set(tk.INSERT, "1.0")
        
        while self.find_next():
            if self.current_match:
                start, end = self.current_match
                self.text_widget.delete(start, end)
                self.text_widget.insert(start, replace_text)
                count += 1
                
                # Update position for next search
                new_end = f"{start}+{len(replace_text)}c"
                self.text_widget.mark_set(tk.INSERT, new_end)
                self.current_match = None
            else:
                break
                
        messagebox.showinfo("Replace All", f"Replaced {count} occurrences.")
        
    def close(self):
        """Close the dialog."""
        if self.dialog:
            self.dialog.grab_release()
            self.dialog.destroy()
            self.dialog = None


class TextEditorEnhancements:
    """Enhanced text editing functionality for Tkinter Text widgets."""
    
    def __init__(self, text_widget, parent_window):
        self.text_widget = text_widget
        self.parent_window = parent_window
        self.find_replace_dialog = None
        self._setup_shortcuts()
        
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts for the text widget."""
        # Ctrl+A - Select All
        self.text_widget.bind('<Control-a>', self._select_all)
        
        # Ctrl+F - Find/Replace
        self.text_widget.bind('<Control-f>', self._show_find_replace)
        
        # Ctrl+H - Find/Replace (alternative)
        self.text_widget.bind('<Control-h>', self._show_find_replace)
        
        # Ctrl+Z - Undo (built-in but ensure it's enabled)
        self.text_widget.config(undo=True, maxundo=-1)
        
        # Ctrl+Y - Redo
        self.text_widget.bind('<Control-y>', self._redo)
        
        # F3 - Find Next
        self.text_widget.bind('<F3>', self._find_next)
        
        # Escape - Clear selection
        self.text_widget.bind('<Escape>', self._clear_selection)
        
    def _select_all(self, event=None):
        """Select all text in the widget."""
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.INSERT, "1.0")
        self.text_widget.see(tk.INSERT)
        return 'break'  # Prevent default behavior
        
    def _show_find_replace(self, event=None):
        """Show the find/replace dialog."""
        if not self.find_replace_dialog:
            self.find_replace_dialog = FindReplaceDialog(
                self.parent_window, self.text_widget
            )
        self.find_replace_dialog.show()
        return 'break'
        
    def _redo(self, event=None):
        """Redo the last undone action."""
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass  # Nothing to redo
        return 'break'
        
    def _find_next(self, event=None):
        """Find next occurrence if find dialog is open."""
        if self.find_replace_dialog and self.find_replace_dialog.dialog:
            self.find_replace_dialog.find_next()
        return 'break'
        
    def _clear_selection(self, event=None):
        """Clear current selection."""
        self.text_widget.tag_remove(tk.SEL, "1.0", tk.END)
        return 'break'
        
    def add_custom_shortcut(self, key_combination, callback):
        """Add a custom keyboard shortcut.
        
        Args:
            key_combination: Key combination string (e.g., '<Control-k>')
            callback: Function to call when shortcut is pressed
        """
        self.text_widget.bind(key_combination, callback)