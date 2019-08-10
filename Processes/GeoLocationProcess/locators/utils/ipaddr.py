from requests import get


# Returns the public IP(IPV4) address obtained through ipify.org
def get_ip_address():
    return get("https://api.ipify.org").text
