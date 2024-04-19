import boto3

def get_user_group_policies(username, iam):
    # Fetch the groups the user belongs to
    groups = iam.list_groups_for_user(UserName=username)['Groups']
    policies = []

    # Fetch policies attached to these groups
    for group in groups:
        # Get managed policies
        attached_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
        policies.extend([policy['PolicyName'] for policy in attached_policies])

        # Optionally, fetch inline policies if they exist
        inline_policies = iam.list_group_policies(GroupName=group['GroupName'])['PolicyNames']
        policies.extend(inline_policies)

    return policies

def main():
    # Initialize a session using your management account
    session = boto3.Session(profile_name='default')
    iam = session.client('iam')

    # User whose policies we want to find
    username = 'rashurmatov@vbrato.io'.strip()

    # Get policies associated with the user through their groups
    policies = get_user_group_policies(username, iam)
    print(f"Policies associated with user '{username}':")
    for policy in policies:
        print(policy)

if __name__ == "__main__":
    main()
