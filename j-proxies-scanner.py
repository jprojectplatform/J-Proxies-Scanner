import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import requests
import socket
import time
import os

# ==========================================
# CONFIGURATION & BRANDING
# ==========================================
TOOL_NAME = "J Proxies Scanner"
VERSION = "v1.4 Ultimate Pro"
FOOTER_TEXT = "Powered by J Project Platform"
FOOTER_URL = "https://jprojectplatform.com"
OUTPUT_FILE = "J_Alive_Proxies.txt"

# Dark Mode Color Palette
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
ACCENT_COLOR = "#007acc"
SUCCESS_COLOR = "#4caf50"
FAIL_COLOR = "#f44336"
WARNING_COLOR = "#ff9800"
ENTRY_BG = "#2d2d2d"

class JProxiesScanner:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{TOOL_NAME} {VERSION}")
        self.root.geometry("750x650")
        self.root.configure(bg=BG_COLOR)

        # Variables
        self.proxy_list = []
        self.is_running = False
        self.scan_thread = None

        # GUI Layout
        self.create_header()
        self.create_controls()
        self.create_logs()
        self.create_footer()

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=BG_COLOR, pady=10)
        header_frame.pack(fill="x")
        
        lbl_title = tk.Label(header_frame, text=TOOL_NAME.upper(), font=("Helvetica", 18, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR)
        lbl_title.pack()
        
        lbl_subtitle = tk.Label(header_frame, text="Advanced Multi-Threaded Proxy Checker", font=("Helvetica", 10), bg=BG_COLOR, fg="#aaaaaa")
        lbl_subtitle.pack()

    def create_controls(self):
        control_frame = tk.LabelFrame(self.root, text="Configuration", bg=BG_COLOR, fg="#aaaaaa", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        control_frame.pack(fill="x", padx=15, pady=5)

        # Row 1: File Selection & Help
        self.btn_load = tk.Button(control_frame, text="📁 Load Proxy List", command=self.load_file, bg=ACCENT_COLOR, fg="white", borderwidth=0, padx=10, pady=5)
        self.btn_load.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.btn_help = tk.Button(control_frame, text="❓ How to Use (Read Me)", command=self.show_instructions_window, bg="#444", fg="white", borderwidth=0, padx=10, pady=5)
        self.btn_help.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.lbl_file_status = tk.Label(control_frame, text="No file loaded", bg=BG_COLOR, fg="#666666", font=("Consolas", 9))
        self.lbl_file_status.grid(row=0, column=2, sticky="w", padx=5)

        # Row 2: Settings
        tk.Label(control_frame, text="Protocol:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="e", padx=5)
        self.protocol_var = tk.StringVar()
        self.cmb_protocol = ttk.Combobox(control_frame, textvariable=self.protocol_var, values=["All", "socks5", "socks4", "http", "https"], state="readonly", width=10)
        self.cmb_protocol.current(0) # Set "All" as Default
        self.cmb_protocol.grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(control_frame, text="Timeout (sec):", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=2, sticky="e", padx=5)
        self.ent_timeout = tk.Entry(control_frame, width=5, bg=ENTRY_BG, fg=FG_COLOR, insertbackground="white")
        self.ent_timeout.insert(0, "5")
        self.ent_timeout.grid(row=1, column=3, sticky="w", padx=5)

        # Row 3: Limits
        tk.Label(control_frame, text="Max Proxies to Scan:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="e", padx=5)
        self.ent_limit = tk.Entry(control_frame, width=10, bg=ENTRY_BG, fg=FG_COLOR, insertbackground="white")
        self.ent_limit.insert(0, "100") 
        self.ent_limit.grid(row=2, column=1, sticky="w", padx=5)

        # Action Buttons
        btn_frame = tk.Frame(control_frame, bg=BG_COLOR)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)

        self.btn_start = tk.Button(btn_frame, text="▶ START SCAN", command=self.start_scan, bg=SUCCESS_COLOR, fg="white", font=("Helvetica", 10, "bold"), borderwidth=0, padx=20, pady=5)
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = tk.Button(btn_frame, text="⏹ STOP", command=self.stop_scan, bg=FAIL_COLOR, fg="white", font=("Helvetica", 10, "bold"), borderwidth=0, padx=20, pady=5, state="disabled")
        self.btn_stop.pack(side="left", padx=10)

    def create_logs(self):
        log_frame = tk.Frame(self.root, bg=BG_COLOR)
        log_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Statistics
        stats_frame = tk.Frame(log_frame, bg=BG_COLOR)
        stats_frame.pack(fill="x", pady=2)
        
        self.lbl_stats = tk.Label(stats_frame, text="Total: 0 | Alive: 0 | Dead: 0", bg=BG_COLOR, fg=FG_COLOR, font=("Consolas", 10, "bold"))
        self.lbl_stats.pack(side="right")
        
        tk.Label(log_frame, text="Live Logs:", bg=BG_COLOR, fg=FG_COLOR, font=("Helvetica", 9)).pack(anchor="w")

        # Scrollable Text Area
        self.txt_log = tk.Text(log_frame, bg="#000000", fg="#00ff00", font=("Consolas", 9), state="disabled", height=15)
        self.txt_log.pack(fill="both", expand=True)
        
        self.txt_log.tag_config("success", foreground=SUCCESS_COLOR)
        self.txt_log.tag_config("fail", foreground=FAIL_COLOR)
        self.txt_log.tag_config("info", foreground="#aaaaaa")
        self.txt_log.tag_config("warn", foreground="#ff9800")

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#111111", pady=8)
        footer_frame.pack(fill="x", side="bottom")
        
        lbl_footer = tk.Label(footer_frame, text=f"{FOOTER_TEXT} | {FOOTER_URL}", bg="#111111", fg="#555555", font=("Helvetica", 8), cursor="hand2")
        lbl_footer.pack()
        lbl_footer.bind("<Button-1>", lambda e: self.log_msg(f"Visit: {FOOTER_URL}", "info"))

    # ==========================================
    # LOGIC FUNCTIONS
    # ==========================================
    def load_file(self):
        filename = filedialog.askopenfilename(title="Select Proxy List", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if filename:
            try:
                with open(filename, "r") as f:
                    self.proxy_list = [line.strip() for line in f if line.strip()]
                self.lbl_file_status.config(text=f"Loaded: {len(self.proxy_list)} proxies", fg=SUCCESS_COLOR)
                self.log_msg(f"Loaded {len(self.proxy_list)} proxies from {os.path.basename(filename)}", "info")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def log_msg(self, message, tag="info"):
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n", tag)
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def show_instructions_window(self):
        # Create a new top-level window (Popup)
        help_win = tk.Toplevel(self.root)
        help_win.title("J Proxies Scanner - Professional Guide")
        help_win.geometry("800x600")
        help_win.configure(bg=BG_COLOR)

        # Title
        tk.Label(help_win, text="GUIDE & BEST PRACTICES", font=("Helvetica", 16, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=10)

        # Scrollable Text Frame
        frame = tk.Frame(help_win, bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=15, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        txt = tk.Text(frame, bg="#252526", fg="#d4d4d4", font=("Consolas", 10), wrap="word", yscrollcommand=scrollbar.set, padx=10, pady=10)
        txt.pack(fill="both", expand=True)
        scrollbar.config(command=txt.yview)

        # Styles
        txt.tag_config("h1", font=("Helvetica", 12, "bold"), foreground=ACCENT_COLOR)
        txt.tag_config("h2", font=("Helvetica", 11, "bold"), foreground="#ffffff")
        txt.tag_config("gold", foreground="#FFD700")  # Gold
        txt.tag_config("silver", foreground="#C0C0C0") # Silver
        txt.tag_config("bronze", foreground="#cd7f32") # Bronze
        txt.tag_config("warn", foreground=FAIL_COLOR)
        txt.tag_config("cmd", background="#000000", foreground="#00ff00")

        # Content Generation
        content = [
            ("STEP 1: SETUP YOUR PROXYCHAINS\n", "h1"),
            ("1. Run the scan with this tool. Working proxies are saved to:\n", "normal"),
            (f"   {os.getcwd()}/{OUTPUT_FILE}\n\n", "cmd"),
            ("2. Open your ProxyChains configuration file:\n", "normal"),
            ("   sudo nano /etc/proxychains4.conf\n", "cmd"),
            ("   (If that file doesn't work, try: /etc/proxychains.conf)\n\n", "warn"),
            ("3. CRITICAL SETTINGS:\n", "h2"),
            ("   • Enable 'dynamic_chain' (remove the #).\n", "normal"),
            ("   • Comment out 'strict_chain' (add a #).\n", "normal"),
            ("   • Scroll to the bottom [ProxyList] section.\n", "normal"),
            ("   • Paste the content of J_Alive_Proxies.txt there.\n\n", "normal"),
            ("-" * 60 + "\n\n", "normal"),

            ("HIERARCHY OF PROXY QUALITY (CHAINING GUIDE)\n", "h1"),
            ("When building your chain, quality matters. Here is the ranking:\n\n", "normal"),

            ("🥇 SOCKS5 (GOLD STANDARD)\n", "gold"),
            ("   • Best for everything. Supports TCP, UDP, Auth, and Remote DNS.\n", "normal"),
            ("   • ALWAYS use a SOCKS5 proxy as the FIRST HOP in your chain.\n", "normal"),
            ("   • This guarantees your traffic enters the tunnel correctly.\n\n", "normal"),

            ("🥈 SOCKS4 (SILVER STANDARD)\n", "silver"),
            ("   • Good for basic browsing. Supports TCP only.\n", "normal"),
            ("   • NO UDP support (Game chat/VoIP might fail).\n", "normal"),
            ("   • Warning: Can leak DNS queries if not configured correctly.\n\n", "normal"),

            ("🥉 HTTP (BRONZE / AVOID)\n", "bronze"),
            ("   • Worst for chaining. Often 'Transparent'.\n", "normal"),
            ("   • DO NOT use these in a ProxyChain. They break the tunnel.\n", "warn"),
            ("   • If you have connection denied errors, remove HTTP proxies first.\n\n", "warn"),
            ("-" * 60 + "\n\n", "normal"),

            ("PRO TIPS FOR SUCCESS\n", "h1"),
            ("• Never start your chain with an HTTP proxy.\n", "warn"),
            ("• If you get 'Denied' errors, the proxy accepting the connection is refusing to pass it on.\n", "normal"),
            ("• Always end your config with a new line.\n\n", "normal"),

            ("FINAL TEST COMMAND\n", "h1"),
            ("Run this to verify your IP is hidden:\n", "normal"),
            ("proxychains curl http://ifconfig.me", "cmd")
        ]

        # Insert content with tags
        txt.config(state="normal")
        for text, tag in content:
            txt.insert("end", text, tag)
        txt.config(state="disabled")

    def check_single_proxy_protocol(self, ip, port, protocol, timeout):
        """Tests a single IP against a single protocol"""
        proxy_url = f"{protocol}://{ip}:{port}"
        proxies = { "http": proxy_url, "https": proxy_url }
        try:
            start = time.time()
            response = requests.get("http://www.google.com", proxies=proxies, timeout=timeout)
            latency = round((time.time() - start) * 1000)
            if response.status_code == 200:
                return (protocol, ip, port, latency)
        except:
            return None
        return None

    def check_proxy_smart(self, proxy_str, selected_protocol, timeout):
        if not self.is_running: return None

        # --- NEW FIXED PARSING LOGIC ---
        parts = proxy_str.split()
        ip = ""
        port = ""
        
        try:
            if len(parts) == 3: # Format: socks5 192.168.1.1 8080 (ProxyChains format)
                ip = parts[1]
                port = parts[2]
            elif len(parts) == 2: # Format: 192.168.1.1 8080 (Space separated)
                ip = parts[0]
                port = parts[1]
            elif ":" in proxy_str: # Format: 192.168.1.1:8080 (Colon separated)
                ip, port = proxy_str.split(":")
            else:
                return None # Unknown format
            
            port = int(port)
        except:
            return None

        # Determine protocols
        protocols_to_test = []
        if selected_protocol == "All":
            protocols_to_test = ["socks5", "socks4", "http"]
        else:
            protocols_to_test = [selected_protocol]

        # Scan
        for proto in protocols_to_test:
            if not self.is_running: break
            result = self.check_single_proxy_protocol(ip, port, proto, timeout)
            if result:
                return result 
        
        return None

    def run_scanner(self):
        protocol_setting = self.protocol_var.get()
        try:
            timeout = float(self.ent_timeout.get())
            limit_str = self.ent_limit.get()
            # If user deleted the limit, default to 1000
            limit = int(limit_str) if limit_str else 1000
        except ValueError:
            messagebox.showerror("Error", "Timeout and Limit must be numbers.")
            self.stop_scan()
            return

        targets = self.proxy_list[:limit]
        total = len(targets)
        alive_count = 0
        dead_count = 0
        
        self.log_msg(f"Starting scan... Mode: {protocol_setting}", "info")
        
        # Initialize Output File
        with open(OUTPUT_FILE, "w") as f:
            f.write(f"# J Proxies Scanner Results - {time.strftime('%Y-%m-%d %H:%M')}\n")
            f.write("# Format compatible with proxychains4.conf\n\n")
            f.write("[ProxyList]\n")

        # Threading Setup
        max_threads = 50 
        active_threads = []
        
        def worker(proxy_item):
            nonlocal alive_count, dead_count
            
            result = self.check_proxy_smart(proxy_item, protocol_setting, timeout)
            
            if result:
                working_proto, ip, port, lat = result
                alive_count += 1
                self.log_msg(f"[+] ALIVE: {working_proto} {ip}:{port} ({lat}ms)", "success")
                
                with open(OUTPUT_FILE, "a") as f:
                    f.write(f"{working_proto}  {ip}  {port}\n")
            else:
                dead_count += 1

            self.root.after(0, lambda: self.lbl_stats.config(text=f"Total: {total} | Alive: {alive_count} | Dead: {dead_count}"))

        # Launch Threads
        for proxy in targets:
            if not self.is_running: break
            
            while len(active_threads) >= max_threads:
                active_threads = [t for t in active_threads if t.is_alive()]
                time.sleep(0.1)
                if not self.is_running: break
            
            t = threading.Thread(target=worker, args=(proxy,))
            active_threads.append(t)
            t.start()

        for t in active_threads:
            t.join()

        self.log_msg(f"Scan Complete. {alive_count} proxies saved to {OUTPUT_FILE}", "success")
        self.stop_scan()

    def start_scan(self):
        if not self.proxy_list:
            messagebox.showwarning("Warning", "Please load a proxy list first.")
            return

        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal", bg=FAIL_COLOR)
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")
        
        self.scan_thread = threading.Thread(target=self.run_scanner)
        self.scan_thread.start()

    def stop_scan(self):
        self.is_running = False
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled", bg="#555555")

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = JProxiesScanner(root)
    root.mainloop()
