import requests
from bs4 import BeautifulSoup
import re

def clean_address(address):
    """
    Adds a space between the street name and city in the address.
    """
    # Use regex to insert a space before the city starts (assuming city starts with a capital letter)
    # that directly follows a lowercase letter or number without a space
    cleaned_address = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', address)
    return cleaned_address

def get_team_location(team_name):
    """
    Fetches the location (address) of a team from the NVSL website.

    Args:
        team_name (str): The name of the team (e.g., "Annandale").
    
    Returns:
        str: The address of the team if found, or a message indicating it wasn't found.
    """
    base_url = "https://www.mynvsl.com/teams"

    # Determine the starting letter of the team name for filtering
    starting_letter = team_name[0].upper()
    url = f"{base_url}#{starting_letter}"

    # Send a GET request to the teams page with the specific letter filter
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch the teams page. Status code: {response.status_code}"

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the list corresponding to the current letter
    team_list = soup.find("ul", {"class": f"list-1 set-{starting_letter}"})
    if not team_list:
        return f"No teams found starting with '{starting_letter}'."

    # Iterate through each team entry in the list
    teams = team_list.find_all("li")
    for team in teams:
        name_tag = team.find("a")
        if name_tag and name_tag.text.strip().lower() == team_name.lower():
            # Extract the team's page URL
            team_url = "https://www.mynvsl.com" + name_tag["href"]

            # Visit the team's page to extract the address
            return fetch_team_address(team_url)

    return f"Team '{team_name}' not found on the NVSL website."


def fetch_team_address(team_url):
    """
    Fetches the address of a team from its specific NVSL page.

    Args:
        team_url (str): The URL of the team's page.

    Returns:
        str: The address of the team if found, or a message indicating it wasn't found.
    """
    response = requests.get(team_url)
    if response.status_code != 200:
        return f"Failed to fetch the team's page. Status code: {response.status_code}"

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate the address in the profile page
    address_heading = soup.find("h4", string="ADDRESS")
    if address_heading:
        address_tag = address_heading.find_next("p", {"class": "intro"})
        if address_tag:
            return f"\"{clean_address(address_tag.text.strip())}\""

    return "Address not found on the team's page."


# Example usage
if __name__ == "__main__":
    team_name = input("Enter a team name")
    location = get_team_location(team_name)
    print(location)
