```markdown
# J Proxies Scanner

**J Proxies Scanner** is a professional, advanced GUI tool designed for security researchers and penetration testers. It uses multi-threading to rapidly scan, verify, and filter SOCKS4, SOCKS5, and HTTP proxies from large lists.

The tool automatically exports working proxies in a format directly compatible with `proxychains4.conf`, streamlining your anonymity workflow.

---

## 🚀 Features

* **High-Performance Multi-Threading:** Scan hundreds of proxies in seconds, not minutes.
* **Modern GUI:** Clean, dark-mode interface built with `tkinter`.
* **Smart Filtering:** Validates connection speed (latency) and anonymity.
* **ProxyChains Ready:** Automatically saves valid proxies to `J_Alive_Proxies.txt` in the correct configuration format.
* **Customizable:** Set your own timeouts, thread limits, and protocols.

---

## 🛠️ Installation

### 1. System Requirements (Linux / Kali)
This tool requires the Python `tkinter` library, which is a system-level dependency.
```bash
sudo apt update
sudo apt install python3-tk

```

### 2. Set Up Virtual Environment

It is best practice to run this tool in its own isolated environment to avoid conflicts.

```bash
# Create the virtual environment
python3 -m venv j-proxies-scanner-env

# Activate the environment
# On Linux/Mac:
source j-proxies-scanner-env/bin/activate
# On Windows:
# j-proxies-scanner-env\Scripts\activate

```

### 3. Install Dependencies

Once your environment is active, install the required Python libraries.

```bash
pip install -r requirements.txt

```

---

## 🖥️ Usage

1. **Download a Proxy List:** Get a raw `.txt` list of proxies (IP:Port) from sources like GitHub.
2. **Run the Tool:**
```bash
python j-proxies-scanner.py

```


3. **Configure & Scan:**
* Click **Load Proxy List** to select your file.
* Select the protocol (e.g., `socks5`).
* Set the **Timeout** (recommended: 3-5 seconds).
* Click **START SCAN**.


4. **Export:**
* The tool will automatically generate `J_Alive_Proxies.txt` with the working proxies.
* Copy the contents of this file into your `/etc/proxychains4.conf`.



---

## 🪟 Run on Windows (J Wrapper)

You can run this tool seamlessly anywhere from your Windows Terminal using **J Wrapper**. This allows for easy integration and execution across different environments.

👉 **Download J Wrapper here:** [https://github.com/jprojectplatform/J-Wrapper](https://github.com/jprojectplatform/J-Wrapper)

---

## 📝 Configuration Output

The output file `J_Alive_Proxies.txt` is formatted specifically for ProxyChains:

```text
[ProxyList]
socks5  192.168.1.50   1080
socks5  45.77.12.11    9050

```

---

<div align="center">
<p>Powered by <strong>J Project Platform</strong></p>
<a href="https://jprojectplatform.com">https://jprojectplatform.com</a>
</div>

```

```
