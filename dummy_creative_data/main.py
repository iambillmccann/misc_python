import random
import json
import sys
from datetime import datetime

# Lists of common first names and last names
first_names = ["John", "Jane", "Michael", "Mary", "James", "Patricia", "Robert", "Jennifer", "William", "Linda"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

def generate_user():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    legal_name = f"{first_name} {last_name}"
    stage_name = "Ima Dummy"
    phone_number = f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    banking_data = json.dumps({"bank": "Bank Name", "account": str(random.randint(100000, 999999))}) if random.choice([True, False]) else "NULL"
    email = f"user_{random.randint(10000, 99999)}@example.com"
    biography = "This is a sample biography." if random.choice([True, False]) else "NULL"
    primary_profile_id = "NULL"
    currency = "USD"
    current_balance = round(random.uniform(0, 10000), 4)
    from_rate = round(random.uniform(0, 100), 4)
    to_rate = round(random.uniform(100, 200), 4)
    is_negotiable = random.choice([True, False])
    is_id_verified = random.choice([True, False])
    is_social_verified = random.choice([True, False])
    id_vid = f"VID_{random.randint(10000, 99999)}" if random.choice([True, False]) else "NULL"
    recommendations = json.dumps({"rec1": "Good", "rec2": "Excellent"}) if random.choice([True, False]) else "NULL"
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return (first_name, last_name, f"('{legal_name}', '{email}', '{phone_number}', '{first_name}', '{last_name}', '{stage_name}', {biography}, {banking_data}, {primary_profile_id}, NULL, '{currency}', {current_balance}, {from_rate}, {to_rate}, false, true, {is_negotiable}, {is_id_verified}, {is_social_verified}, true, false, true, true, {id_vid}, NULL, {recommendations}, '{created_date}')")

def generate_creative(first_name, last_name):
    creative_name = f"{last_name}, {first_name}"
    image_url = f"http://example.com/image_{random.randint(100000, 999999)}.jpg" if random.choice([True, False]) else "NULL"
    creative_data = json.dumps({"type": "Art", "description": "Sample creative data"}) if random.choice([True, False]) else "NULL"

    return f"('{creative_name}', {image_url}, {creative_data}, NULL)"

def main():
    num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    with open("insert_data.sql", "w") as file:
        for _ in range(num_records):
            first_name, last_name, user_insert = generate_user()
            file.write(f"INSERT INTO user (legalName, email, phoneNumber, firstName, lastName, stageName, biography, bankingData, primaryProfileId, primaryCreativeId, currency, currentBalance, fromRate, toRate, isArtist, isCreative, isNegotiable, isIDVerified, isSocialVerified, isActive, isDeactivated, allowSms, termsApproved, IDVid, careerMode, recommendations, createdDate) VALUES {user_insert};\n")
            file.write("SET @last_user_id = LAST_INSERT_ID();\n")

            creative_insert = generate_creative(first_name, last_name)
            file.write(f"INSERT INTO creative (name, imageURL, creativeData, userId) VALUES {creative_insert};\n")
            file.write("SET @last_creative_id = LAST_INSERT_ID();\n")

            # Update the primaryCreativeId in the user table
            file.write("UPDATE user SET primaryCreativeId = @last_creative_id WHERE id = @last_user_id;\n")

            # Update the userId in the creative table
            file.write("UPDATE creative SET userId = @last_user_id WHERE id = @last_creative_id;\n")

if __name__ == "__main__":
    main()
