####################################################################################################################
#
# File:        ambari_service_monitoring.py
# Description: A simple script to monitor services, using Ambari REST API
#              Note: tested on ambari version 2.6.2.0, used in HDP 2.6.5
# Author:      Mostafa Mamdouh
# Created:     Wed May 05 22:17:24 PDT 2021
#
####################################################################################################################


from twitterstreaming import ambari_config
import time
import json
import requests


def ambari_rest(rest_api):
    url = "http://" + ambari_config.AMBARI_DOMAIN + ":" + ambari_config.AMBARI_PORT + rest_api
    r = requests.get(url, auth=(ambari_config.AMBARI_USER_ID, ambari_config.AMBARI_USER_PW))
    return(json.loads(r.text))

def get_service(service, cluster_name):
    rest_api = ambari_config.REST_API + cluster_name + "/services/" + service
    json_data =  ambari_rest(rest_api)
    
    return(json_data)

def get_cluser_name() :
    json_data = ambari_rest(ambari_config.REST_API)
    cluster_name = json_data["items"][0]["Clusters"]["cluster_name"]
    return cluster_name


def main():
    while(True):
        for service in ambari_config.SERVICES:
            cluster_name = get_cluser_name()
            service_dict = get_service(service, cluster_name) # dict
            service_info = service_dict["ServiceInfo"]
            service_key = ['maintenance_state', 'repository_state', 'service_name', 'state']
            service_needed_info = {x:service_info[x] for x in service_key}
            service_alerts = service_dict["alerts_summary"]
            print('=' * 50 + service + '=' * 50)
            if(service_needed_info["state"] != "STARTED"):
                # Do the desired action here (send email, ...) instead of just printing messages
                print("There is an Error, Actions will be set here")
                print(service + " status:")
                print(service_needed_info)
                print("Alerts Summary status:")
                print(service_alerts)
                components = service_dict["components"]
                for component in components:
                    component_rest_api = component["href"].split("8080")[1]
                    component_dict = ambari_rest(component_rest_api)
                    component_info = component_dict["ServiceComponentInfo"]
                    component_keys = ['started_count', 'state', 'total_count', 'unknown_count']
                    component_needed_info = {x:component_info[x] for x in component_keys}
                    print("==" * 20)
                    print(component["ServiceComponentInfo"]["component_name"] + " status:")
                    print(component_needed_info)
            else:
                print("Everything is ok with " + service)
                
        time.sleep(ambari_config.CHECK_EVERY)

if __name__ == "__main__":
    main()

