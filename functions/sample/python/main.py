#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    authenticator = IAMAuthenticator('F7FM6RvKB5x-p7mUNYAvwRTi5FymO9PbhHNWANwkE8wW')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://7048706c-0b51-4bcb-8bec-0e969192e656-bluemix.cloudantnosqldb.appdomain.cloud")
    
    response = service.post_find(
        db='reviews',
        selector={'dealership': {'$eq': int(dict["dealerId"])}},
    ).get_result()
    
    try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }
