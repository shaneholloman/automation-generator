# VSCode and Conda Environment Package Installation Guide

1. **Activate your Conda environment**

    ```sh
    conda activate automation-generator
    ```

2. **Verify the active Python interpreter**

    ```sh
    which python
    python --version
    ```

   Ensure this points to your Conda environment's Python

3. **Install packages using Conda (preferred method)**

    ```sh
    conda install pynput pyautogui
    ```

4. **If packages are not available via Conda, use pip with one of these methods:**
   a. Full path to pip:

    ```sh
    /home/shadmin/miniconda/envs/automation-generator/bin/pip install pynput pyautogui
    ```

   b. Use Python's pip module:

    ```sh
    python -m pip install pynput pyautogui
    ```

5. **Verify package installation**

    ```sh
    conda list | grep -E "pynput|pyautogui"
    ```

6. **Update VSCode Python Interpreter**
   - Open Command Palette (Ctrl+Shift+P)
   - Type "Python: Select Interpreter"
   - Choose the interpreter path that includes "automation-generator"

7. **Restart VSCode**
   Close and reopen VSCode completely

8. **Test imports in VSCode**
   Open a Python file and try importing the packages:

    ```python
    import pynput
    import pyautogui
    ```

## Best Practices and Tips

1. **Always verify your environment is activated:**

    ```sh
    conda info --envs
    ```

   Look for the asterisk (*) next to your environment name.

2. **Check your Python version after activation:**

    ```sh
    python --version
    ```

3. **Verify which pip you're using:**

    ```sh
    which pip
    ```

   Ensure it points to your Conda environment.

4. **Prefer `conda install` when possible** for better dependency management within the Conda ecosystem.

5. **Create a shell function for using the correct pip:**
   Add this to your `.bashrc` or `.zshrc`:

    ```bash
    conda_pip() {
        "${CONDA_PREFIX}/bin/pip" "$@"
    }
    ```

   Then use: `conda_pip install package_name`

6. **Use `python -m pip` instead of just `pip`** to ensure you're using the pip associated with the current Python interpreter.

7. **If issues persist, check VSCode's Python extension settings** and ensure it's using the correct environment path.

Remember: Always ensure you're working in the correct environment before installing packages or running your code!
