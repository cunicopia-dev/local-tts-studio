"""Main window for the TTS application."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import logging
from typing import Optional

from src.core.tts_engine import TTSEngine
from src.utils.text_processing import (
    load_text_file, extract_text_from_pdf, chunk_text, estimate_reading_time
)
from src.utils.audio_utils import AudioPlayer, save_audio
from src.config.settings import Settings

logger = logging.getLogger(__name__)


class MainWindow:
    """Main application window."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.tts_engine = TTSEngine(
            model_name=settings.tts.model_name,
            use_gpu=settings.tts.use_gpu
        )
        self.audio_player = AudioPlayer()
        self.last_audio = None
        
        # Initialize GUI
        self.root = tk.Tk()
        self._setup_window()
        self._create_widgets()
        self._create_menu()
        
        # Initialize TTS in background
        threading.Thread(target=self._init_tts, daemon=True).start()
        
        # Check audio device status
        self._check_audio_status()
        
    def _check_audio_status(self):
        """Check and display audio device status."""
        if not self.audio_player.has_audio_device():
            self.status_var.set("Ready (No audio device - will simulate playback)")
            logger.warning("No audio device detected - playback will be simulated")
        
    def _init_tts(self):
        """Initialize TTS engine in background."""
        try:
            self.status_var.set("Initializing TTS engine...")
            self.tts_engine.initialize()
            if self.audio_player.has_audio_device():
                self.status_var.set("Ready")
            else:
                self.status_var.set("Ready (No audio device - will simulate playback)")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            self.root.after(0, lambda: messagebox.showerror(
                "Initialization Error", 
                f"Failed to initialize TTS engine:\n{str(e)}"
            ))
            self.status_var.set("Initialization failed")
            
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Local TTS Studio")
        self.root.geometry(
            f"{self.settings.app.window_width}x{self.settings.app.window_height}"
        )
        
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Text area with scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_box = tk.Text(
            text_frame, 
            wrap=tk.WORD,
            font=(self.settings.app.font_family, self.settings.app.font_size),
            yscrollcommand=scrollbar.set
        )
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_box.yview)
        
        # Control panel
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=8, pady=4)
        
        # Buttons
        self.btn_speak = tk.Button(
            control_frame, text="Speak", command=self._on_speak, width=12
        )
        self.btn_speak.pack(side=tk.LEFT, padx=4)
        
        self.btn_stop = tk.Button(
            control_frame, text="Stop", command=self._on_stop, 
            width=12, state=tk.DISABLED
        )
        self.btn_stop.pack(side=tk.LEFT, padx=4)
        
        self.btn_save = tk.Button(
            control_frame, text="Save Audio", command=self._on_save, width=12
        )
        self.btn_save.pack(side=tk.LEFT, padx=4)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame, orient=tk.HORIZONTAL, mode='determinate'
        )
        self.progress.pack(fill=tk.X, expand=True, padx=8)
        
        # Status bar
        self.status_var = tk.StringVar(value="Initializing...")
        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var, 
            anchor=tk.W, relief=tk.SUNKEN
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Text...", command=self._on_open_text)
        file_menu.add_command(label="Open PDF...", command=self._on_open_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Clear Text", command=self._on_clear_text)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Voice menu
        voice_menu = tk.Menu(menubar, tearoff=0)
        voice_menu.add_command(
            label="Load Voice Sample...", command=self._on_load_voice
        )
        menubar.add_cascade(label="Voice", menu=voice_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._on_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def _on_open_text(self):
        """Handle opening text file."""
        file_path = filedialog.askopenfilename(
            title="Open Text File",
            filetypes=[("Text files", "*.txt *.md"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            text = load_text_file(Path(file_path))
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, text)
            
            # Update status with reading time estimate
            time_est = estimate_reading_time(text)
            self.status_var.set(
                f"Loaded: {Path(file_path).name} "
                f"(~{time_est:.1f} min reading time)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            
    def _on_open_pdf(self):
        """Handle opening PDF file."""
        file_path = filedialog.askopenfilename(
            title="Open PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            text = extract_text_from_pdf(Path(file_path))
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, text)
            
            time_est = estimate_reading_time(text)
            self.status_var.set(
                f"Loaded PDF: {Path(file_path).name} "
                f"(~{time_est:.1f} min reading time)"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF:\n{str(e)}")
            
    def _on_clear_text(self):
        """Clear the text area."""
        self.text_box.delete("1.0", tk.END)
        self.status_var.set("Text cleared")
        
    def _on_load_voice(self):
        """Handle loading voice sample."""
        file_path = filedialog.askopenfilename(
            title="Select Voice Sample",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            self.tts_engine.set_speaker_voice(Path(file_path))
            self.status_var.set(f"Voice loaded: {Path(file_path).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load voice:\n{str(e)}")
            
    def _on_speak(self):
        """Handle speak button click."""
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter or load text first.")
            return
            
        # Disable speak button, enable stop
        self.btn_speak.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        # Start synthesis in background thread
        threading.Thread(
            target=self._synthesize_and_play, 
            args=(text,), 
            daemon=True
        ).start()
        
    def _synthesize_and_play(self, text: str):
        """Synthesize and play text in background."""
        try:
            # Prepare chunks
            chunks = chunk_text(text, self.settings.tts.chunk_size)
            total_chunks = len(chunks)
            
            self.progress['maximum'] = total_chunks
            self.progress['value'] = 0
            
            def update_progress(current, total):
                self.progress['value'] = current
                self.status_var.set(f"Synthesizing chunk {current}/{total}")
                
            # Synthesize
            self.status_var.set("Starting synthesis...")
            audio = self.tts_engine.synthesize(chunks, update_progress)
            self.last_audio = audio
            
            # Play
            if self.audio_player.has_audio_device():
                self.status_var.set("Playing audio...")
            else:
                self.status_var.set("Simulating audio playback...")
            self.audio_player.play(audio)
            
            # Monitor playback
            while self.audio_player.is_playing():
                threading.Event().wait(0.1)
                
            self.status_var.set("Playback complete")
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            error_msg = str(e)
            self.root.after(0, lambda msg=error_msg: messagebox.showerror(
                "Synthesis Error", msg
            ))
            self.status_var.set("Error occurred")
            
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.btn_speak.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))
            
    def _on_stop(self):
        """Handle stop button click."""
        self.audio_player.stop()
        self.status_var.set("Playback stopped")
        self.btn_stop.config(state=tk.DISABLED)
        self.btn_speak.config(state=tk.NORMAL)
        
    def _on_save(self):
        """Handle save audio."""
        if self.last_audio is None:
            messagebox.showwarning(
                "No Audio", 
                "Please generate audio first before saving."
            )
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Audio",
            defaultextension=".wav",
            filetypes=[
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        try:
            output_path = Path(file_path)
            format = "mp3" if output_path.suffix.lower() == ".mp3" else "wav"
            save_audio(self.last_audio, output_path, format)
            self.status_var.set(f"Saved: {output_path.name}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save audio:\n{str(e)}")
            
    def _on_about(self):
        """Show about dialog."""
        messagebox.showinfo(
            "About Local TTS Studio",
            "Local TTS Studio\n\n"
            "A professional offline text-to-speech studio with voice cloning support.\n\n"
            "Built with Coqui TTS and XTTS-v2"
        )
        
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()