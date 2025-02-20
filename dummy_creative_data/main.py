#
# Randomly generates dummy data for the user and creative tables in the database.
#
import random
import json
import sys
from datetime import datetime

# Lists of common first names, last names, style names, roles, instruments, and genres
first_names = [
    "John",
    "Jane",
    "Michael",
    "Mary",
    "James",
    "Patricia",
    "Robert",
    "Jennifer",
    "William",
    "Linda",
]
last_names = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
]
style_names = [
    "adventurer",
    "avataaars",
    "big-ears",
    "big-smile",
    "bottts",
    "croodles",
    "lorelei",
    "micah",
    "notionists",
    "open-peeps",
    "personas",
    "thumbs",
]
roles_list = [
    "Songwriter",
    "Producer",
    "Musician",
    "Background Vocalist",
    "Mixing Engineer",
]
instruments_list = [
    "Accordion",
    "Bagpipe",
    "Banjo",
    "Bongo drum",
    "Bugle",
    "Castanets",
    "Glockenspiel",
    "Guitar",
    "Harp",
    "Saxophone",
    "Triangle",
    "Zither",
]
genres_list = [
    "Alternative",
    "Ambient",
    "Blues",
    "Country",
    "Folk",
    "Heavy Metal",
    "Hip Hop/Rap",
    "K Pop",
    "Pop",
    "Rock",
]


def generate_user():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    user_id = f"user_{random.randint(10000, 99999)}"
    legal_name = f"{first_name} {last_name}"
    stage_name = "Ima Dummy"
    phone_number = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    email = f"{user_id}@example.com"
    primary_profile_id = "NULL"
    currency = "USD"
    current_balance = round(random.uniform(0, 10000), 4)
    from_rate = round(random.uniform(0, 100), 4)
    to_rate = round(random.uniform(100, 200), 4)
    is_negotiable = random.choice([True, False])
    is_id_verified = random.choice([True, False])
    is_social_verified = random.choice([True, False])
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (
        first_name,
        last_name,
        f"('{user_id}', '{legal_name}', '{email}', '{phone_number}', '{first_name}', '{last_name}', '{stage_name}', NULL, NULL, {primary_profile_id}, NULL, '{currency}', {current_balance}, {from_rate}, {to_rate}, false, true, {is_negotiable}, {is_id_verified}, {is_social_verified}, true, false, true, true, NULL, NULL, NULL, '{created_date}')",
    )


def generate_creative(first_name, last_name):
    creative_name = f"{last_name}, {first_name}"
    style_name = random.choice(style_names)
    image_url = f"https://api.dicebear.com/7.x/{style_name}/png"
    roles = random.sample(roles_list, random.randint(0, 5))
    roles_data = [{"role": role, "active": True} for role in roles]
    instruments = random.sample(instruments_list, random.randint(0, 6))
    genres = random.sample(genres_list, random.randint(0, 3))
    creative_data = {
        "bio": "",
        "email": None,
        "roles": roles_data,
        "genres": genres,
        "social": [
            {
                "data": {"url": "", "identifier": "", "isPlatformVerified": False},
                "platform": "instagram",
            },
            {
                "data": {"url": "", "identifier": "", "isPlatformVerified": False},
                "platform": "youtube",
            },
            {
                "data": {"url": "", "identifier": "", "isPlatformVerified": False},
                "platform": "tiktok",
            },
            {
                "data": {"url": "", "identifier": "", "isPlatformVerified": False},
                "platform": "twitter",
            },
        ],
        "toRate": None,
        "allowSms": False,
        "currency": None,
        "fromRate": None,
        "legalName": None,
        "stageName": None,
        "instruments": instruments,
        "phoneNumber": "+1909170991",
        "isIDVerified": None,
        "isNegotiable": None,
        "isSocialVerified": None,
    }

    return f"('{creative_name}', '{image_url}', '{json.dumps(creative_data)}', NULL)"


def main():
    num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 50

    with open("insert_data.sql", "w") as file:
        for _ in range(num_records):
            first_name, last_name, user_insert = generate_user()
            file.write(
                f"INSERT INTO user (userId, legalName, email, phoneNumber, firstName, lastName, stageName, biography, bankingData, primaryProfileId, primaryCreativeId, currency, currentBalance, fromRate, toRate, isArtist, isCreative, isNegotiable, isIDVerified, isSocialVerified, isActive, isDeactivated, allowSms, termsApproved, IDVid, careerMode, recommendations, createdDate) VALUES {user_insert};\n"
            )
            file.write("SET @last_user_id = LAST_INSERT_ID();\n")

            creative_insert = generate_creative(first_name, last_name)
            file.write(
                f"INSERT INTO creative (name, imageURL, creativeData, userId) VALUES {creative_insert};\n"
            )
            file.write("SET @last_creative_id = LAST_INSERT_ID();\n")

            # Update the primaryCreativeId in the user table
            file.write(
                "UPDATE user SET primaryCreativeId = @last_creative_id WHERE id = @last_user_id;\n"
            )

            # Update the userId in the creative table
            file.write(
                "UPDATE creative SET userId = @last_user_id WHERE id = @last_creative_id;\n"
            )


if __name__ == "__main__":
    main()
