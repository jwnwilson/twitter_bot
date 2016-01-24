import requests
import json
import argparse


parser = argparse.ArgumentParser(description='Get hash tag battle results')
parser.add_argument('-b', '--id',
                    help='ID of hash tag battle to retreive')
parser.add_argument('-i', '--ip', default='localhost',
                    help='Set the ip address of the service to send the post request to and display the results')
parser.add_argument('-v','--verbose', action='store_true')

args = parser.parse_args()

def battle_request(id, ip="localhost"):
    """
    create a POST request for battle results via our very limited 'API'
    :param id: battle id to retrieve data for
    :return: json string
    """
    post_data = {"id":id}
    battle_data = requests.post("http://%s:8000/hash_tag_battle/" % ip, data=post_data)
    return battle_data.text

if __name__ == "__main__":
    if args.ip and args.id:
        print battle_request(args.id, ip=args.ip)
    else:
        print "Please enter --id args"
