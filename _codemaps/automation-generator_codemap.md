# automation-generator

> CodeMap Source: Local directory: `/home/shadmin/_github/automation-generator` By: shaneholloman

This markdown document provides a comprehensive overview of the directory structure and file contents. It aims to give viewers (human or AI) a complete view of the codebase in a single file for easy analysis.

## Document Table of Contents

The table of contents below is for navigational convenience and reflects this document's structure, not the actual file structure of the repository.

<!-- TOC -->

- [automation-generator](#automation-generator)
  - [Document Table of Contents](#document-table-of-contents)
  - [Repo File Tree](#repo-file-tree)
  - [Repo File Contents](#repo-file-contents)
    - [kickstart.sh](#kickstartsh)
    - [vscode-conda-troubleshooting.md](#vscode-conda-troubleshootingmd)
    - [README.MD](#readmemd)
  - [How to Use This Tool](#how-to-use-this-tool)
    - [commands/action-watch.sh](#commandsaction-watchsh)
    - [commands/install-python-dependencies.sh](#commandsinstall-python-dependenciessh)
    - [commands/action-perform.ps1](#commandsaction-performps1)
    - [commands/install-python-dependencies.ps1](#commandsinstall-python-dependenciesps1)
    - [commands/action-watch.ps1](#commandsaction-watchps1)
    - [src/action\_perform.py](#srcaction_performpy)
    - [src/action\_watch.py](#srcaction_watchpy)
    - [src/logs/input\_log.csv](#srclogsinput_logcsv)

<!-- /TOC -->

## Repo File Tree

This file tree represents the actual structure of the repository. It's crucial for understanding the organization of the codebase.

```tree
.
├── _codemaps/
├── commands/
│   ├── action-perform.ps1
│   ├── action-perform.sh
│   ├── action-watch.ps1
│   ├── action-watch.sh
│   ├── install-python-dependencies.ps1
│   └── install-python-dependencies.sh
├── src/
│   ├── logs/
│   │   └── input_log.csv
│   ├── action_perform.py
│   └── action_watch.py
├── README.MD
├── kickstart.sh
└── vscode-conda-troubleshooting.md

4 directories, 12 files
```

## Repo File Contents

The following sections present the content of each file in the repository. Large and binary files are acknowledged but their contents are not displayed.

### kickstart.sh

```bash
#!/bin/bash

# Define the GitHub account or organization name
githubAccount="shaneholloman" # Change this to your personal account name if needed

# Initialize a new git repository
git init -b main

# Get the name of the current repository from the top-level directory
repoName=$(basename "$(git rev-parse --show-toplevel)")

# Create a new repository on GitHub using the gh CLI
gh repo create "$repoName" --public -y

# Add the remote repository
git remote add origin https://github.com/$githubAccount/"$repoName".git

# Add all files in the current directory to the git repository
git add .

# Commit the changes
git commit -m "Initial commit"

# Push the changes to GitHub
git push -u origin main

# Define an associative array where the key is the name of the secret and the value is the secret value
declare -A secrets
secrets=(
  ["DOCKERHUB_TOKEN"]="$DOCKERHUB_TOKEN"
  ["DOCKERHUB_USERNAME"]="$DOCKERHUB_USERNAME"
  ["GALAXY_API_KEY"]="$GALAXY_API_KEY"
  # Add more secrets here as needed
)

# Check if environment variables exist
missingVars=()
for key in "${!secrets[@]}"; do
  if [ -z "${secrets[$key]}" ]; then
    missingVars+=("$key")
  fi
done

if [ ${#missingVars[@]} -ne 0 ]; then
  ## Print 2 blank lines here to make the output easier to read
  echo ""
  echo ""
  echo "The following environment variables are missing:"
  for var in "${missingVars[@]}"; do
    echo "$var"
  done
  echo "Please add them to your .bashrc file and run 'source ~/.bashrc'"
  exit 1
fi

# Loop through each secret to set it for the current repository
for key in "${!secrets[@]}"; do
  value=${secrets[$key]}
  command="echo -n $value | gh secret set $key --repo=$githubAccount/$repoName"
  eval "$command"
done

# Tag and push after setting the secrets
commitMessage="tagging first version"
tagVersion="2.0.0"
tagMessage="An Ansible role model template only"

git commit --allow-empty -m "$commitMessage"
git tag -a $tagVersion -m "$tagMessage"

# Ask the user if the current git tag and message are correct
## Print 2 blank lines here to make the output easier to read
echo ""
echo ""
echo "The current git tag is $tagVersion with the message '$tagMessage'. Is this correct? (yes/no)"
read -r answer

if [ "$answer" != "${answer#[Yy]}" ]; then
  git push origin $tagVersion
else
  echo "Please edit the git tag and message in this script."
fi
```

### vscode-conda-troubleshooting.md

````markdown
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
````

### README.MD

```markdown
# Automation Generator

This tool allows you to automate actions based on mouse clicks and keyboard inputs.

## Prerequisites

Make sure you have the latest version of Python installed on your machine.

To install the required dependencies, run the following command:

```sh
sh commands/install-python-dependencies.sh
```

## How to Use This Tool

1. Start the watch mode by running the following command. This command will activate the program to monitor mouse clicks and keyboard typing.

    ```sh
    sh commands/action-watch.sh
    ```

2. Perform the actions you want to automate. The program will track your mouse clicks and keyboard inputs.

3. To stop the watch mode and store the recorded actions, press the ESC key along with a mouse click. This action will trigger the program to save the information in a log file.

4. To execute the stored actions, run the following command. This command will read the stored actions from the log file and perform the steps that were previously done by the user.

    ```sh
    sh commands/action-perform.sh
    ```

```

### commands/action-perform.sh

```bash
#!/bin/bash

echo 'Action started'
python src/action_perform.py
echo 'Action finished'
```

### commands/action-watch.sh

```bash
#!/bin/bash

rm src/logs/input_log.csv
touch src/logs/input_log.csv
echo 'Watching actions...'
echo 'Press ESC + mouse click to stop'
python src/action_watch.py
echo 'Automation stored successfully'
```

### commands/install-python-dependencies.sh

```bash
#!/bin/bash

pip install pynput pyautogui
```

### commands/action-perform.ps1

```powershell
Write-Output 'Action started'
python src/action_perform.py
Write-Output 'Action finished'
```

### commands/install-python-dependencies.ps1

```powershell
pip install pynput pyautogui
```

### commands/action-watch.ps1

```powershell
Remove-Item src/logs/input_log.csv -ErrorAction Ignore
New-Item -ItemType File -Path src/logs/input_log.csv | Out-Null
Write-Output 'Watching actions...'
Write-Output 'Press ESC + mouse click to stop'
python src/action_watch.py
Write-Output 'Automation stored successfully'
```

### src/action_perform.py

```python
"""
This module performs actions based on logged input from a CSV file.
It simulates mouse clicks and key presses using pyautogui.
"""

import ast
import csv
import time

import pyautogui

with open("src/logs/input_log.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        is_mouse_click, MOUSE_BUTTON, mouse_coord, key_pressed, time_passed = row
        time.sleep(float(time_passed))
        if is_mouse_click == "True":
            x, y = ast.literal_eval(mouse_coord)
            MOUSE_BUTTON = str.replace(MOUSE_BUTTON, "Button.", "")
            if MOUSE_BUTTON == "left":
                pyautogui.click(x, y)
            else:
                pyautogui.rightClick()
        else:
            pyautogui.press(str.replace(key_pressed, "Key.", ""))
```

### src/action_watch.py

```python
"""
This module records mouse clicks and keyboard presses, logging them to a CSV file.
It uses pynput to listen for input events and csv to write the log.
"""

import csv
import time
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener


class InputLogger:
    """
    A class to log mouse and keyboard inputs to a CSV file.
    """

    def __init__(self, log_file):
        """
        Initialize the InputLogger.

        Args:
        log_file (str): Path to the log file
        """
        self.log_file = log_file
        self.exit_program = False
        self.last_action_time = None

    def log_mouse_click(self, x, y, button, pressed):
        """
        Log mouse click events to the CSV file.

        Args:
        x (int): X-coordinate of the mouse click
        y (int): Y-coordinate of the mouse click
        button (pynput.mouse.Button): The mouse button that was clicked
        pressed (bool): True if the button was pressed, False if released

        Returns:
        bool: False if the program should exit, True otherwise
        """
        if self.exit_program:
            return False
        action_time = time.time()
        duration = action_time - self.last_action_time if self.last_action_time else 0
        self.last_action_time = action_time
        if pressed:
            with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([True, button, (x, y), None, duration])
        return True

    def log_key_press(self, key):
        """
        Log key press events to the CSV file.

        Args:
        key (pynput.keyboard.Key): The key that was pressed

        Returns:
        bool: False if the program should exit, True otherwise
        """
        action_time = time.time()
        duration = action_time - self.last_action_time if self.last_action_time else 0
        self.last_action_time = action_time
        with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            pressed_key = ""
            try:
                pressed_key = key.char
            except AttributeError:
                if key == key.esc:
                    self.exit_program = True
                    return False
                pressed_key = key
            writer.writerow([False, None, None, pressed_key, duration])
        return True

    def start(self):
        """
        Start the input listeners.
        """
        with MouseListener(
            on_click=self.log_mouse_click
        ) as mouse_listener, KeyboardListener(
            on_press=self.log_key_press
        ) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


def main():
    """
    Main function to set up and start the input logger.
    """
    logger = InputLogger("src/logs/input_log.csv")
    logger.start()


if __name__ == "__main__":
    main()
```

### src/logs/input_log.csv

```csv
True,Button.left,"(1562, 623)",,0
True,Button.left,"(1055, 772)",,0.9121556282043457
False,,,Key.shift,1.0290884971618652
False,,,#,0.20736908912658691
False,,,Key.space,0.521090030670166
False,,,t,0.4154789447784424
False,,,y,0.25797533988952637
False,,,p,0.21470189094543457
False,,,i,0.3297412395477295
False,,,n,0.32128238677978516
False,,,g,0.6414966583251953
False,,,Key.space,0.4049208164215088
False,,,s,0.8100907802581787
False,,,o,0.17745590209960938
False,,,m,0.23967218399047852
False,,,e,0.2581596374511719
False,,,Key.space,0.2358705997467041
False,,,t,0.2543070316314697
False,,,h,0.25884056091308594
False,,,i,0.3786613941192627
False,,,n,0.30744218826293945
False,,,g,0.48172688484191895
True,Button.left,"(1596, 579)",,8.067446231842041
True,Button.left,"(1344, 668)",,1.6752357482910156
False,,,Key.ctrl,2.8742198944091797
```

> This concludes the repository's file contents. Please review thoroughly for a comprehensive understanding of the codebase.
