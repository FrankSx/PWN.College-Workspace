import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to sanitize folder names
def sanitize_folder_name(name):
    # Replace special characters, spaces, and hyphens with underscores
    sanitized = "".join(c if c.isalnum() or c in ('_') else '_' for c in name.replace(" ", "_").replace("-", "_"))
    return sanitized.strip()

# Function to create folder structure for a module
def create_folder_structure(base_url, dojo_name, module_name, module_url):
    # Sanitize the dojo and module names for folder names
    sanitized_dojo_name = sanitize_folder_name(dojo_name)
    sanitized_module_name = sanitize_folder_name(module_name)

    # Create the main dojo folder
    dojo_folder = os.path.join(sanitized_dojo_name, sanitized_module_name)
    os.makedirs(dojo_folder, exist_ok=True)

    # Fetch the HTML content of the module page
    module_page_url = urljoin(base_url, module_url)
    module_response = requests.get(module_page_url)
    module_soup = BeautifulSoup(module_response.text, 'html.parser')

    # Find all challenges in the module
    challenges = module_soup.find_all('div', class_='accordion-item')

    # Create level folders and add descriptions
    for challenge in challenges:
        # Get the challenge name from the challenge
        challenge_name = challenge.find('h4', class_='accordion-item-name challenge-name')
        if challenge_name:
            challenge_name = challenge_name.text.strip()
        else:
            challenge_name = "Unknown Challenge"

        # Sanitize the challenge name for folder names
        sanitized_challenge_name = sanitize_folder_name(challenge_name)

        # Create the challenge folder
        challenge_folder = os.path.join(dojo_folder, sanitized_challenge_name)
        os.makedirs(challenge_folder, exist_ok=True)

        # Create description.md file
        description = challenge.find('div', class_='embed-responsive')
        if description:
            description = description.text.strip()
        else:
            description = "No description available."
        with open(os.path.join(challenge_folder, 'description.md'), 'w') as f:
            f.write(f"# {challenge_name}\n\n")
            f.write(f"**Description**: {description}\n")
            f.write(f"<<--**--..__..--Created-By-FrankSx--..__..--**-->>\n")

        # Create an empty executable Python file
        python_file_path = os.path.join(challenge_folder, f"{sanitized_challenge_name}.py")
        with open(python_file_path, 'w') as f:
            pass  # Create an empty file

        # Make the Python file executable
        os.chmod(python_file_path, 0o755)

    print(f"Module '{sanitized_module_name}' created successfully with {len(challenges)} challenges.")
    print(f"Folder structure:")
    print(f"  {dojo_folder}/")
    for challenge in challenges:
        challenge_name = challenge.find('h4', class_='accordion-item-name challenge-name')
        if challenge_name:
            challenge_name = challenge_name.text.strip()
        else:
            challenge_name = "Unknown Challenge"
        sanitized_challenge_name = sanitize_folder_name(challenge_name)
        print(f"    {sanitized_challenge_name}/")
        print(f"      description.md")
        print(f"      {sanitized_challenge_name}.py")
    print(f"<<--**--..__..--Created-By-FrankSx--..__..--**-->>")
    print(f"<<--**--..__..--PWN~COLLEGE--..__..--**-->>\n")

# Function to fetch dojos and their modules
def fetch_dojos_and_modules(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all dojos
    dojos = soup.find_all('a', class_='text-decoration-none')

    for dojo in dojos:
        dojo_url = dojo['href']  # Get the URL from the anchor tag
        dojo_name = dojo.find('h4')
        if dojo_name:
            dojo_name = dojo_name.text.strip()  # Get the dojo name
        else:
            dojo_name = "Unknown Dojo"
        print(f"Dojo Name: {dojo_name}, Dojo URL: {dojo_url}")

        # Fetch the HTML content of the Dojo page
        dojo_page_url = urljoin(base_url, dojo_url)
        dojo_response = requests.get(dojo_page_url)
        dojo_soup = BeautifulSoup(dojo_response.text, 'html.parser')

        # Find the modules section
        modules_section = dojo_soup.find('h2', class_='row', string='Modules')
        if modules_section:
            # Find the modules list
            modules_list = modules_section.find_next('ul')
            modules = modules_list.find_all('a', class_='text-decoration-none')

            for module in modules:
                module_name = module.find('h4', class_='card-title')
                if module_name:
                    module_name = module_name.text.strip()
                else:
                    module_name = "Unknown Module"
                module_url = module['href']  # Get the module URL
                print(f"  Module Name: {module_name}, Module URL: {module_url}")

                # Create folder structure for the module
                create_folder_structure(base_url, dojo_name, module_name, module_url)

# Main execution
if __name__ == "__main__":
    print(f"<<--**--..__..--PWN~COLLEGE WorkSpace--..__..--**-->>\n")
    BASE_URL = "https://pwn.college/dojos"
    fetch_dojos_and_modules(BASE_URL)