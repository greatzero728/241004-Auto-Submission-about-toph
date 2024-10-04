# Auto Submission for Toph Problems

This project automates the process of scraping problem lists from [Toph](https://toph.co/problems/all) and submitting C++ code solutions. The workflow consists of fetching problem links, generating C++ files, and automatically submitting solutions to the platform.

![Scraping the problem list of Toph](https://github.com/greatzero728/241004-Auto-Submission-about-toph/blob/main/Final%20Result/gif/1%20Scarping%20the%20problem%20list%20of%20toph.gif)
![Auto Submission in Toph 1](https://github.com/greatzero728/241004-Auto-Submission-about-toph/blob/main/Final%20Result/gif/2%20Auto%20Submission%20in%20toph%201.gif)
![Auto Submission in Toph 2](https://github.com/greatzero728/241004-Auto-Submission-about-toph/blob/main/Final%20Result/gif/2%20Auto%20Submission%20in%20toph%202.gif)

## Installation

### Environment Setup

1. **Install Python**

   Make sure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install pip**

   If you haven't installed pip, follow these steps:
   
   - Download `get-pip.py` using the following link: [get-pip.py](https://bootstrap.pypa.io/get-pip.py).
   - Open Command Prompt and navigate to the directory where `get-pip.py` is saved.
   - Run the following command:
     ```bash
     python get-pip.py
     ```

3. **Install Required Modules**

   Use pip to install the necessary modules:
   ```bash
   pip install requests beautifulsoup4 python-dotenv selenium
   ```

## Usage

1. **Scrape Problem List**

   The `getProblemList.py` script fetches problem URLs from Toph and generates a list of problems in `problemList.txt`. It also creates empty C++ files for each problem in the `cpp_problems` directory.

   To run the script, execute:
   ```bash
   python getProblemList.py
   ```

   After execution, you will find:
   - `problemList.txt`: Contains all URLs of the problems on Toph.
   - `cpp_problems/`: Directory containing empty `.cpp` files for each problem.

2. **Create Toph Account**

   Ensure you have a Toph account. You will need to add your username and password to a `.env` file in the root directory:
   ```plaintext
   TOPH_USERNAME=your_username
   TOPH_PASSWORD=your_password
   WAIT_TIME=5  # Adjust as needed
   CHECK_RESULT=2  # Adjust as needed
   ```

3. **Automatic Submission**

   Run the `autoSubmission.py` script to start the submission process:
   ```bash
   python autoSubmission.py
   ```

   The script will check the submission directory for `.cpp` files, move the first available file to the `cpp_problems` directory, submit it, and then check the result at intervals defined by `CHECK_RESULT`.

## Workflow Overview

1. **Scraping**: The scraper fetches problem links from Toph and stores them in a text file.
2. **File Creation**: For each problem, an empty C++ file is created in the `cpp_problems` directory.
3. **Submission**: The script logs into Toph, submits the C++ files, and checks the results periodically.

## Conclusion

This automation tool simplifies the process of solving problems on Toph by handling the scraping and submission for you. Customize the waiting times and other parameters in the `.env` file as needed.

For any issues or contributions, feel free to open an issue or submit a pull request.