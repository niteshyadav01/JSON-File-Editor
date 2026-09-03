# PySide Development Environment Setup

## Requirements

- **MSYS2**
- **Python v3.12.x**

---

## Step 1: Access the System-Installed Python from the MSYS2 Terminal

### Things to Know

You’ll need to know the path where Python is installed on your system.

To make it easier to access the system-installed Python from the MSYS2 terminal, set up alias commands in your `~/.bashrc` file.\
Open the file in any text editor (e.g., `vim`):

```bash
vim ~/.bashrc
```

Add the following lines to define aliases for Python and pip:

```bash
alias sys_python='/path/to/your/system/installed/python/python.exe'
alias sys_pip='/path/to/your/system/installed/python/Scripts/pip.exe'
```

### Note:

Windows paths must be converted to UNIX-style paths for MSYS2.

- Drive letters such as `C:` become `/c/`
- Backslashes `\` are replaced with forward slashes `/`

For example, if Python is installed at:

```
C:\Users\user_name\AppData\Local\Programs\Python\Python312\
```

Then the equivalent UNIX path would be:

```
/c/Users/user_name/AppData/Local/Programs/Python/Python312/
```

---

## Step 2: Create the Project Structure

Here’s the project structure used for development:

```bash
.
├── CMakeLists.txt
├── README.md
├── run                 # Output executables
├── build               # CMake build folder
└── src                 # Source code
    ├── CMakeLists.txt
    ├── gui
    │   ├── win_main.py # Main window class
    │   └── win_main.ui # Main window UI file
    └── main.py         # Application entry point
```

---

## Step 3: Create a Virtual Environment

To create a virtual environment for your project, run the following command in the **project root folder** (outside the `src` directory):

```bash
sys_python -m venv .venv
```

This will create a `.venv` folder in the project root.

---

## Step 4: Activate the Virtual Environment

Activate the virtual environment by running:

```bash
source .venv/Scripts/activate
```

---

## Step 5: Install Required Packages

If you have a `requirements.txt` file with your dependencies, install them using:

```bash
pip install -r requirements.txt
```

---

## Step 6: Build the Project

Create and enter the build directory:

```bash
mkdir build && cd build
```

Then build the project using CMake and Make:

```bash
cmake .. -G "MSYS Makefiles"
make
```

---

## Step 7: Run the Executable

After building, the executable will be located in the `./run/bin` directory.\
You can run it either by double-clicking or from the terminal:

```bash
./app.exe
```

---

## Step 8: Add `PYTHONPATH`

For faster Python execution, add the following `PYTHONPATH` environment variable to your `.venv/Scripts/activate` file:

```bash
export PYTHONPATH=/absolute/path/to/project/root/build/auto_gen/
```

Now you can directly run your app from the source using:

```bash
python src/main.py
```

---

### Note:

You only need to rebuild the project when `.ui` or `.qrc` files are modified since these files require compilation.\
If no changes are made to them, you can directly run:

```bash
python src/main.py
```

