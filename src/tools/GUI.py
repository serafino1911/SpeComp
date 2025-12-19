"""
SpeComp - Modern GUI Interface
A comprehensive tool for Raman spectroscopy analysis with modern design
"""

from modules.importer import *
import modules.gui_functions as gf



class SpeCompModernGUI:
    """Modern GUI for Spectral Comparator with improved design and UX"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configure main window properties"""
        self.root.title('SpeComp - Spectral Comparator')
        self.root.geometry('800x600')
        self.root.resizable(True, True)
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)  # Header
        self.root.rowconfigure(1, weight=1)  # Main content
        self.root.rowconfigure(2, weight=0)  # Status bar
        
    def setup_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Use a modern theme
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
        
        # Custom styles
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), 
                       foreground='#2c3e50', padding=10)
        style.configure('Section.TLabel', font=('Segoe UI', 11, 'bold'), 
                       foreground='#34495e', padding=5)
        style.configure('Info.TLabel', font=('Segoe UI', 9), 
                       foreground='#7f8c8d')
        style.configure('Action.TButton', font=('Segoe UI', 10), 
                       padding=10)
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Create menu bar
        self.create_menu()
        
        # Create header
        self.create_header()
        
        # Create main content area with notebook (tabs)
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
        
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open Spectrum...', 
                             command=lambda: gf.select_file(self.root, False, self.file_entry),
                             accelerator='Ctrl+O')
        file_menu.add_command(label='Open Filter...', 
                             command=lambda: gf.select_filter_file(self.root, self.filter_entry))
        file_menu.add_separator()
        file_menu.add_command(label='Configuration...', 
                             command=lambda: gf.configuration_window(self.root),
                             accelerator='Ctrl+,')
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit, 
                             accelerator='Alt+F4')
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Tools', menu=tools_menu)
        tools_menu.add_command(label='Filter Subtraction', 
                              command=lambda: gf.filter_subtraction(self.root))
        tools_menu.add_command(label='Noise Modification', 
                              command=lambda: gf.modify_enter(self.root))
        tools_menu.add_command(label='Display Multiple Spectra', 
                              command=lambda: gf.display_filex(self.root))
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='View', menu=view_menu)
        view_menu.add_command(label='Display Configuration', 
                             command=lambda: gf.configuration_display(self.root))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Documentation', command=self.show_help)
        help_menu.add_command(label='About SpeComp', command=self.show_about)
        
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root, relief='flat', borderwidth=0)
        header_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        header_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(header_frame, text='📈 SpeComp - Spectral Comparator', 
                               style='Header.TLabel')
        title_label.grid(row=0, column=0, sticky='w')
        
        subtitle_label = ttk.Label(header_frame, 
                                  text='Raman Spectroscopy Analysis & Database Comparison',
                                  style='Info.TLabel')
        subtitle_label.grid(row=1, column=0, sticky='w', padx=5)
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').grid(row=1, column=0, sticky='ew', pady=5)
        
    def create_main_content(self):
        """Create main content area with tabs"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky='nsew')
        
        # Tab 1: Analysis
        self.create_analysis_tab()
        
        # Tab 2: Preprocessing
        self.create_preprocessing_tab()
        
    def create_analysis_tab(self):
        """Create the main analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(analysis_frame, text='  Analysis  ')
        
        # Configure grid
        analysis_frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # === File Selection Section ===
        section_label = ttk.Label(analysis_frame, text='📁 Data Files', 
                                 style='Section.TLabel')
        section_label.grid(row=current_row, column=0, columnspan=3, sticky='w', pady=(0, 10))
        current_row += 1
        
        # Working file
        ttk.Label(analysis_frame, text='Working File:', font=('Segoe UI', 10)).grid(
            row=current_row, column=0, sticky='w', pady=5, padx=(20, 10))
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(analysis_frame, textvariable=self.file_var, 
                                    font=('Segoe UI', 9))
        self.file_entry.grid(row=current_row, column=1, sticky='ew', pady=5, padx=5)
        # Set initial value
        if gf.FILE_LOADED and gf.WORKING_FILE:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, gf.WORKING_FILE)
        else:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, 'No file loaded')
        
        load_btn = ttk.Button(analysis_frame, text='Browse...', 
                             command=lambda: gf.select_file(self.root, False, self.file_entry),
                             style='Action.TButton')
        load_btn.grid(row=current_row, column=2, pady=5, padx=(5, 0))
        current_row += 1
        
        # Filter file
        ttk.Label(analysis_frame, text='Filter File:', font=('Segoe UI', 10)).grid(
            row=current_row, column=0, sticky='w', pady=5, padx=(20, 10))
        
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(analysis_frame, textvariable=self.filter_var, 
                                      font=('Segoe UI', 9))
        self.filter_entry.grid(row=current_row, column=1, sticky='ew', pady=5, padx=5)
        # Set initial value
        if gf.FILTER_FILE:
            self.filter_entry.delete(0, 'end')
            self.filter_entry.insert(0, gf.FILTER_FILE)
        else:
            self.filter_entry.delete(0, 'end')
            self.filter_entry.insert(0, 'No filter loaded')
        
        filter_btn = ttk.Button(analysis_frame, text='Browse...', 
                               command=lambda: gf.select_filter_file(self.root, self.filter_entry),
                               style='Action.TButton')
        filter_btn.grid(row=current_row, column=2, pady=5, padx=(5, 0))
        current_row += 1
        
        # Separator
        ttk.Separator(analysis_frame, orient='horizontal').grid(
            row=current_row, column=0, columnspan=3, sticky='ew', pady=20)
        current_row += 1
        
        # === Wavelength Range Section ===
        section_label = ttk.Label(analysis_frame, text='📊 Wavelength Range', 
                                 style='Section.TLabel')
        section_label.grid(row=current_row, column=0, columnspan=3, sticky='w', pady=(0, 10))
        current_row += 1
        
        # Range frame
        range_frame = ttk.Frame(analysis_frame)
        range_frame.grid(row=current_row, column=0, columnspan=3, sticky='ew', padx=20)
        range_frame.columnconfigure(1, weight=1)
        range_frame.columnconfigure(3, weight=1)
        current_row += 1
        
        # Min/Max
        ttk.Label(range_frame, text='Min:', font=('Segoe UI', 9)).grid(
            row=0, column=0, sticky='w', pady=5, padx=(0, 5))
        self.min_var = tk.StringVar()
        min_entry = ttk.Entry(range_frame, textvariable=self.min_var, width=15)
        min_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        min_entry.insert(0, 'None')
        
        ttk.Label(range_frame, text='Max:', font=('Segoe UI', 9)).grid(
            row=0, column=2, sticky='w', pady=5, padx=(20, 5))
        self.max_var = tk.StringVar()
        max_entry = ttk.Entry(range_frame, textvariable=self.max_var, width=15)
        max_entry.grid(row=0, column=3, sticky='w', pady=5, padx=5)
        max_entry.insert(0, 'None')
        
        use_range_btn = ttk.Button(range_frame, text='Apply', 
                                   command=lambda: gf.use_limit(self.root, self.min_var, self.max_var))
        use_range_btn.grid(row=0, column=4, pady=5, padx=(10, 0))
        
        # Exclusion zone
        ttk.Label(range_frame, text='Exclude Min:', font=('Segoe UI', 9)).grid(
            row=1, column=0, sticky='w', pady=5, padx=(0, 5))
        self.ex_min_var = tk.StringVar()
        ex_min_entry = ttk.Entry(range_frame, textvariable=self.ex_min_var, width=15)
        ex_min_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        ex_min_entry.insert(0, 'None')
        
        ttk.Label(range_frame, text='Exclude Max:', font=('Segoe UI', 9)).grid(
            row=1, column=2, sticky='w', pady=5, padx=(20, 5))
        self.ex_max_var = tk.StringVar()
        ex_max_entry = ttk.Entry(range_frame, textvariable=self.ex_max_var, width=15)
        ex_max_entry.grid(row=1, column=3, sticky='w', pady=5, padx=5)
        ex_max_entry.insert(0, 'None')
        
        use_ex_btn = ttk.Button(range_frame, text='Apply', 
                               command=lambda: gf.use_exclusion(self.root, self.ex_min_var, self.ex_max_var))
        use_ex_btn.grid(row=1, column=4, pady=5, padx=(10, 0))
        
        # Separator
        ttk.Separator(analysis_frame, orient='horizontal').grid(
            row=current_row, column=0, columnspan=3, sticky='ew', pady=20)
        current_row += 1
        
        # === Action Buttons ===
        action_frame = ttk.Frame(analysis_frame)
        action_frame.grid(row=current_row, column=0, columnspan=3, pady=20)
        current_row += 1
        
        # Configuration button
        config_btn = ttk.Button(action_frame, text='⚙️ Configuration', 
                               command=lambda: gf.configuration_window(self.root),
                               style='Action.TButton', width=20)
        config_btn.grid(row=0, column=0, padx=5, pady=5)
        
        # Start analysis button (primary action)
        start_btn = ttk.Button(action_frame, text='▶️ Start Analysis', 
                              command=lambda: gf.start(self.root),
                              style='Primary.TButton', width=20)
        start_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Display button
        display_btn = ttk.Button(action_frame, text='📊 Display Results', 
                                command=lambda: gf.display_filex(self.root),
                                style='Action.TButton', width=20)
        display_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Spacer to push info to bottom
        analysis_frame.rowconfigure(current_row, weight=1)
        current_row += 1
        
        # Info text
        info_frame = ttk.Frame(analysis_frame, relief='flat', borderwidth=1)
        info_frame.grid(row=current_row, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        
        info_text = """💡 Quick Start:
1. Load your working spectrum file
2. Configure analysis settings (algorithms, database path)
3. Click 'Start Analysis' to compare against database
4. View and save results"""
        
        info_label = ttk.Label(info_frame, text=info_text, style='Info.TLabel', 
                              justify='left', padding=10)
        info_label.grid(row=0, column=0, sticky='w')
        
    def create_preprocessing_tab(self):
        """Create preprocessing and filtering tab"""
        preproc_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(preproc_frame, text='  Preprocessing  ')
        
        preproc_frame.columnconfigure(0, weight=1)
        preproc_frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # === Left Column: Filter Subtraction ===
        filter_frame = ttk.LabelFrame(preproc_frame, text='🎯 Background Subtraction', padding=15)
        filter_frame.grid(row=current_row, column=0, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(filter_frame, text='Remove background signals',
                 font=('Segoe UI', 9), foreground='#7f8c8d').pack(anchor='w', pady=(0, 10))
        
        ttk.Label(filter_frame, text='• Simple / Smart / Manual Peaks',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=10, pady=2)
        
        ttk.Button(filter_frame, text='🔧 Filter Subtraction', 
                  command=lambda: gf.filter_subtraction(self.root),
                  style='Primary.TButton', width=25).pack(pady=10)
        
        # === Right Column: Noise & Filtering ===
        noise_frame = ttk.LabelFrame(preproc_frame, text='🔊 Noise & Filtering', padding=15)
        noise_frame.grid(row=current_row, column=1, sticky='nsew', padx=5, pady=5)
        
        ttk.Label(noise_frame, text='Advanced preprocessing tools',
                 font=('Segoe UI', 9), foreground='#7f8c8d').pack(anchor='w', pady=(0, 10))
        
        ttk.Label(noise_frame, text='• Gaussian / Baseline / Differential',
                 font=('Segoe UI', 9)).pack(anchor='w', padx=10, pady=2)
        
        ttk.Button(noise_frame, text='🔧 Noise Modification', 
                  command=lambda: gf.modify_enter(self.root),
                  style='Primary.TButton', width=25).pack(pady=10)
        
        current_row += 1
        
        # === Display Configuration (Full Width) ===
        display_frame = ttk.LabelFrame(preproc_frame, text='👁️ Display Settings', padding=15)
        display_frame.grid(row=current_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Label(display_frame, text='Configure normalization and filters for visualization',
                 font=('Segoe UI', 9), foreground='#7f8c8d').pack(side='left', padx=(0, 10))
        
        ttk.Button(display_frame, text='⚙️ Display Configuration', 
                  command=lambda: gf.configuration_display(self.root),
                  style='Action.TButton').pack(side='right')
        
    def create_status_bar(self):
        """Create status bar at bottom of window"""
        status_frame = ttk.Frame(self.root, relief='sunken', borderwidth=1)
        status_frame.grid(row=3, column=0, sticky='ew')
        
        self.status_var = tk.StringVar()
        self.status_var.set('Ready')
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=('Segoe UI', 9), padding=5)
        status_label.grid(row=0, column=0, sticky='w')
        
        # Version info
        version_label = ttk.Label(status_frame, text='SpeComp v2.0', 
                                 font=('Segoe UI', 9), foreground='#7f8c8d', padding=5)
        version_label.grid(row=0, column=1, sticky='e')
        
        status_frame.columnconfigure(0, weight=1)
        
    def show_help(self):
        """Show documentation help"""
        help_window = tk.Toplevel(self.root)
        help_window.title('SpeComp Documentation')
        help_window.geometry('600x400')
        
        help_frame = ttk.Frame(help_window, padding=20)
        help_frame.pack(fill='both', expand=True)
        
        ttk.Label(help_frame, text='📚 SpeComp Documentation', 
                 font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 20))
        
        docs = [
            ('USAGE.md', 'Complete usage guide with step-by-step workflows and tips'),
            ('METHODS.md', 'Mathematical descriptions of all comparison algorithms'),
            ('INSTALL.md', 'Installation guide with troubleshooting'),
            ('README.md', 'Quick start guide and overview'),
        ]
        
        for doc, desc in docs:
            doc_frame = ttk.Frame(help_frame)
            doc_frame.pack(fill='x', pady=5)
            
            ttk.Label(doc_frame, text=f'• {doc}', 
                     font=('Segoe UI', 10, 'bold')).pack(anchor='w')
            ttk.Label(doc_frame, text=f'  {desc}', 
                     font=('Segoe UI', 9), foreground='#7f8c8d').pack(anchor='w', padx=15)
        
        ttk.Label(help_frame, text='\n💡 Tip: All documentation files are in the repository root',
                 font=('Segoe UI', 9), foreground='#3498db').pack(anchor='w', pady=(20, 0))
        
        ttk.Button(help_frame, text='Close', command=help_window.destroy).pack(pady=20)
        
    def show_about(self):
        """Show about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title('About SpeComp')
        about_window.geometry('500x400')
        about_window.resizable(False, False)
        
        about_frame = ttk.Frame(about_window, padding=30)
        about_frame.pack(fill='both', expand=True)
        
        # Title
        ttk.Label(about_frame, text='🔬 SpeComp', 
                 font=('Segoe UI', 20, 'bold')).pack(pady=(0, 5))
        
        ttk.Label(about_frame, text='Spectral Comparator', 
                 font=('Segoe UI', 12)).pack(pady=(0, 20))
        
        # Version and info
        info_text = """Version 2.0
December 2025

A comprehensive tool for Raman spectroscopy analysis,
database comparison, and interactive spectral manipulation.

Features:
• Multiple comparison algorithms (7 methods)
• Interactive filter subtraction
• Advanced preprocessing tools
• Database matching and ranking
• Modern, user-friendly interface"""
        
        ttk.Label(about_frame, text=info_text, 
                 font=('Segoe UI', 10), justify='center').pack(pady=10)
        
        # Credits
        ttk.Separator(about_frame, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Label(about_frame, text='Developed by:', 
                 font=('Segoe UI', 9, 'bold')).pack()
        ttk.Label(about_frame, text='Matteo Santostefano', 
                 font=('Segoe UI', 9)).pack()
        ttk.Label(about_frame, text='PM_TEN S.r.l', 
                 font=('Segoe UI', 9)).pack(pady=(0, 10))
        
        # GitHub link
        ttk.Label(about_frame, text='github.com/serafino1911/SpeComp', 
                 font=('Segoe UI', 9), foreground='#3498db').pack(pady=5)
        
        ttk.Button(about_frame, text='Close', command=about_window.destroy).pack(pady=20)


def main():
    """Main entry point for the modern GUI"""
    root = tk.Tk()
    app = SpeCompModernGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
