import requests
from bs4 import BeautifulSoup
import os

# Function to fetch problem URLs and names
def fetch_problem_links(page_num):
    url = f"https://toph.co/problems/all?start={25 * page_num}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all problem links
    problem_links = soup.find_all('a', href=True)
    problems = []

    # Only keep the links that match the pattern
    for link in problem_links:
        href = link['href']
        if href.startswith('/p/'):
            problem_name = href.split('/p/')[1]
            problems.append(problem_name)

    return problems

# Function to save problem names to a text file and create cpp files
def save_problems_to_file_and_create_cpp(problems):
    # Removing duplicates and sorting
    unique_problems = sorted(set(problems))

    # Save to problemList.txt in the desired format
    with open('problemList.txt', 'w') as f:
        for problem in unique_problems:
            # Writing the formatted output
            f.write(f"Please transcribe and solve problem <b>{problem}</b> from <b>toph</b>. Problem statement is here: https://toph.co/p/{problem}\n")

    # Create a folder for C++ files if it doesn't exist
    if not os.path.exists('cpp_problems'):
        os.makedirs('cpp_problems')

    # Create a .cpp file for each problem
    for problem in unique_problems:
        file_path = os.path.join('cpp_problems', f"{problem}.cpp")
        with open(file_path, 'w') as f:
            f.write(f"// Solution for {problem}\n")

# Main function to scrape all pages
def scrape_all_problems():
    all_problems = []
    
    # Loop through pages (76 pages as described)
    for page_num in range(76):
        print(f"Scraping page {page_num + 1}...")
        problems = fetch_problem_links(page_num)
        all_problems.extend(problems)
    
    # Save problems to a file and create C++ files
    save_problems_to_file_and_create_cpp(all_problems)
    print("Scraping complete. Check problemList.txt and cpp_problems/ directory.")

# Run the scraper
if __name__ == "__main__":
    scrape_all_problems()
