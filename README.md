# MREx Dashboard

Use with CAN. By Chiara.

## Installation

### 1. [Install Python](https://www.python.org/)

### 2. [Create virtual environment](https://docs.python.org/3/library/venv.html#how-venvs-work) (optional)

In the MREx_Dashboard folder in your favourite terminal.

`python -m venv venv`

### 3. [Enter virtual environment](https://docs.python.org/3/library/venv.html#how-venvs-work) (only if you completed step 2)

If you install dependencies into a virtual environment, you should enter the venv each time you want to run the application.

In the MREx_Dashboard folder in your favourite terminal, execute the command according to the following table. If your favourite terminal does not work, try another.

<table>
<thead>
<tr><th><p>Platform</p></th>
<th><p>Shell</p></th>
<th><p>Command to activate virtual environment</p></th>
</tr>
</thead>
<tbody>
<tr><td rowspan="4"><p>POSIX (Mac, Linux)</p></td>
<td><p>bash/zsh</p></td>
<td><p><code><span>$</span> <span>source</span> venv<span>/bin/activate</span></code></p></td>
</tr>
<tr><td><p>fish</p></td>
<td><p><code><span>$</span> <span>source</span> venv<span>/bin/activate.fish</span></code></p></td>
</tr>
<tr><td><p>csh/tcsh</p></td>
<td><p><code><span>$</span> <span>source</span> venv<span>/bin/activate.csh</span></code></p></td>
</tr>
<tr><td><p>pwsh</p></td>
<td><p><code><span>$</span> venv<span>/bin/Activate.ps1</span></code></p></td>
</tr>
<tr><td rowspan="2"><p>Windows</p></td>
<td><p>cmd.exe</p></td>
<td><p><code><span>C:\&gt;</span> venv<span>\Scripts\activate.bat</span></code></p></td>
</tr>
<tr><td><p>PowerShell</p></td>
<td><p><code><span>PS</span> <span>C:\&gt;</span> venv<span>\Scripts\Activate.ps1</span></code></p></td>
</tr>
</tbody>
</table>

### 4. Install dependencies

In the MREx_Dashboard folder in your favourite terminal.

`pip install -r requirements.txt`

### 5. Run the application

In the MREx_Dashboard folder in your favourite terminal.

`python index.py`

Visit the website linked in the terminal.

## TODO

Performance issues:
1. Callbacks running every second even when not using websocket live feed. Note that there should preferably be periodic checks of which files are available on the web server to update the "Remote server" log source selector - but this is not critical.
2. Translating the entire table and generating graphs from scratch every second, especially when log growing quickly over websocket, rather than appending only new log entries.

Note test3.csv seems to not want to update graphs/table.