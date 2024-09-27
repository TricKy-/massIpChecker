import http.client
import urllib.parse
import json

API_KEY = "YOUR_API_KEY"

api_host = "api.abuseipdb.com"
api_path = "/api/v2/check"


# Function to check reputation for a single IP address
def check_ip_reputation(ip_address):
    params = urllib.parse.urlencode({
        "ipAddress": ip_address,
        "maxAgeInDays": 90  # Adjust the time window for reports if necessary
    })

    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }

    # Create a connection to AbuseIPDB's API
    connection = http.client.HTTPSConnection(api_host)

    try:
        # Send the GET request to the API
        connection.request("GET", api_path + "?" + params, headers=headers)

        # Get the response
        response = connection.getresponse()
        if response.status == 200:
            # Parse the response data
            data = response.read()
            return json.loads(data)
        else:
            print(f"Failed to check IP {ip_address}. Status code: {response.status}")
            return None
    finally:
        # Ensure the connection is closed
        connection.close()


# Function to check the reputation of a list of IPs
def check_multiple_ips(ip_list):
    results = []
    for ip in ip_list:
        print(f"Checking IP: {ip}")
        result = check_ip_reputation(ip)
        if result:
            results.append(result)
    return results


# Function to pretty-print the results
def print_results(results):
    for result in results:
        ip = result['data']['ipAddress']
        abuse_score = result['data']['abuseConfidenceScore']
        total_reports = result['data']['totalReports']
        last_report = result['data']['lastReportedAt']

        print(f"IP Address: {ip}")
        print(f"Abuse Score: {abuse_score}")
        print(f"Total Reports: {total_reports}")
        print(f"Last Reported: {last_report}")
        print("-" * 40)


# Run the script
if __name__ == "__main__":
    # Get IP addresses from the user, separated by spaces
    user_input = input("Enter IP addresses separated by space: ")

    # Split the input into a list of IPs
    ip_addresses = user_input.split()

    # Check and print results for the inputted IP addresses
    results = check_multiple_ips(ip_addresses)
    print_results(results)
