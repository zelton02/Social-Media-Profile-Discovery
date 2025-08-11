import csv
import os
from apify_client import ApifyClient

# Try to load environment variables from local.env if python-dotenv is available
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, "local.env"))
except Exception:
    pass

# Apify API Token from environment
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN") or os.getenv("APIFY_TOKEN")

def find_social_media_with_apify(name, email):
    """
    Uses the Apify Social Media Finder actor to discover social media profiles
    by treating the 'name' as a potential username.
    """
    print(f"Searching for social media profiles for {name} (potential username) using Apify...")
    if not APIFY_API_TOKEN:
        print("APIFY_API_TOKEN not set; skipping Apify lookup.")
        return {}
    try:
        client = ApifyClient(APIFY_API_TOKEN)
        run_input = {
            "profileNames": [name], # Use 'name' as a potential username
            "socials": ["askfm", "discord", "facebook", "github", "instagram", "linkedin", "medium", "pinterest", "steam", "threads", "tiktok", "twitch", "youtube"], # Using exact allowed values for tri_angle/social-media-finder
        }
        
        # Run the Apify actor
        run = client.actor("tri_angle/social-media-finder").call(run_input=run_input)

        profiles = {}
        # Iterate over the items in the actor's default dataset
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if "url" in item and "platform" in item:
                platform_name = item["platform"].capitalize()
                profiles[platform_name] = item["url"]
        return profiles
    except Exception as e:
        print(f"An error occurred with Apify: {e}")
        return {}

def process_users(input_csv_path, output_csv_path, perform_api_calls=True):
    users_data = []
    original_fieldnames = []

    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        original_fieldnames = reader.fieldnames
        for row in reader:
            users_data.append(row)

    social_media_platforms = ["Facebook", "Twitter", "Instagram", "Twitch", "Youtube", "Tiktok"]
    # Ensure all social media columns exist in fieldnames
    new_fieldnames = list(original_fieldnames)
    for platform in social_media_platforms:
        if platform not in new_fieldnames:
            new_fieldnames.append(platform)

    for user_data in users_data:
        name = user_data.get("Name")
        email = user_data.get("Email")

        if not name or not email:
            print(f"Skipping row due to missing Name or Email: {user_data}")
            # Ensure all new_fieldnames are present in user_data, even if empty
            for field in new_fieldnames:
                user_data.setdefault(field, "")
            continue

        if perform_api_calls:
            # Check if any social media link is missing or needs updating
            found_profiles = find_social_media_with_apify(name, email)
            for platform, url in found_profiles.items():
                # Ensure the platform is one we track and update if current value is empty or the placeholder
                # The key here is to ensure that the platform name from Apify matches the CSV column name exactly.
                # Also, update if the current value is empty or contains the specific placeholder.
                if platform in social_media_platforms and (not user_data.get(platform) or user_data.get(platform) == "https://www.facebook.com/share"):
                    user_data[platform] = url
                    print(f"Found {platform} profile for {name}: {url}")
        
        # Ensure all new_fieldnames are present in user_data, even if empty
        for field in new_fieldnames:
            user_data.setdefault(field, "")

    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(users_data)
    print(f"Processed data saved to {output_csv_path}")

if __name__ == "__main__":
    project_root = PROJECT_ROOT
    input_file = os.path.join(project_root, "upload", "GankNow-CopyofSampleLeadList-Sheet1.csv")
    output_file = os.path.join(project_root, "social_media_profiles_updated.csv")
    # To run without API calls (for testing file writing):
    # process_users(input_file, output_file, perform_api_calls=False)
    # To run with API calls (for actual discovery):
    perform_api_calls = bool(APIFY_API_TOKEN)
    if not perform_api_calls:
        print("No APIFY_API_TOKEN found; running without API calls.")
    process_users(input_file, output_file, perform_api_calls=perform_api_calls)

