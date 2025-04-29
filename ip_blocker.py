import boto3

wafv2 = boto3.client('wafv2', region_name='us-east-2')

def blockip(ip_set_id, file_path):

    ip_set_name = 'Blocked-IPs'
    ip_set_scope = 'REGIONAL'
    newIPs = set()

    # Read the IP address from the file
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                cleanIPs = f"{stripped_line}/32"
                newIPs.add(cleanIPs)

    response = wafv2.get_ip_set(
        Name=ip_set_name,
        Scope=ip_set_scope,
        Id=ip_set_id,
    )

    current_addresses = set(response['IPSet']['Addresses'])
    lock_token = response['LockToken']

    update_addresses = current_addresses.union(newIPs)

    if update_addresses != current_addresses:
        updateResponse = wafv2.update_ip_set(
            Name=ip_set_name,
            Scope=ip_set_scope,
            Id=ip_set_id,
            Addresses=list(update_addresses),
            LockToken=lock_token
        )
        print("IP set updated. New total blocked IPs:", len(update_addresses))

    else:
        print("No new IPs to add. Current total blocked IPs:", len(current_addresses))


blockip('###', '/Volumes/HUNTER/PortiaSoftware/anomalous_ip.txt')
