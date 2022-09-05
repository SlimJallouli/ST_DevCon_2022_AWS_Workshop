
#******************************************************************************
# * @file           : BOTO3_cleanupThing.py
# * @brief          : Cleans up thing created by quickConnect.py
# ******************************************************************************
# * @attention
# *
# * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
# * All rights reserved.</center></h2>
# *
# * This software component is licensed by ST under Ultimate Liberty license
# * SLA0044, the "License"; You may not use this file except in compliance with
# * the License. You may obtain a copy of the License at:
# *                             www.st.com/SLA0044
# *
# ******************************************************************************
import boto3
import boto3.session

PROFILE_NAME = 'default'



def main():

    # Initialize Boto3 resources
    this_session = boto3.session.Session(profile_name=PROFILE_NAME)
    iot = this_session.client('iot')
    thing_name = ''
    
    # Get resources
    thing_found = False
    while not thing_found:
        try:
            thing_name = input("Thing name? \n")
            print("Getting:\n")
            cert_arn_list = iot.list_thing_principals(thingName = thing_name)['principals']
            thing_found = True
        except iot.exceptions.ResourceNotFoundException:
            print("Thing " + thing_name + " not found.\n\n")
    
    
    # Building a Dictionary {certArn: [list, of, policies]}
    certDict = {}
    for cert_arn in cert_arn_list:
        print("\tCertificate Arn - " + cert_arn + "\n")

        policy_list = list(map(lambda p: p['policyName'], iot.list_attached_policies(target = cert_arn)['policies']))
        for policy in policy_list:
            print("\t\tPolicy Name - " + policy + "\n")

        certDict[cert_arn] = policy_list

   
    # Detaching certificates 
    for cert_arn in cert_arn_list:
        print("Detaching certificate from thing " + cert_arn + "...\n")
        iot.detach_thing_principal(
            thingName = thing_name, 
            principal = cert_arn
        )

    
    # Detaching every policy from all the attached certs
    for cert_arn in certDict:
        for policy_name in certDict[cert_arn]:
            print("Detaching " + policy_name + " from " + cert_arn + "...\n")
            iot.detach_policy(
                policyName = policy_name, 
                target = cert_arn
            )


    # Deleting the thing
    print("Deleting thing...\n")
    iot.delete_thing(
        thingName = thing_name
    )

    # Deactivating Revoking and Deleting every Cert
    for cert_arn in certDict:
        cert_id = cert_arn.partition('/')[2]
        print("Deactivating certificate " + cert_id + "...\n")
        iot.update_certificate(
            certificateId = cert_id, 
            newStatus = 'INACTIVE'
        )

        print("Revoking certificate...\n")
        iot.update_certificate(
            certificateId = cert_id, 
            newStatus = 'REVOKED'
        )

        print("Deleting certificate...\n")
        iot.delete_certificate(
            certificateId = cert_id
        )
    
    print("Finished.\n")

if __name__ == "__main__":
    main()