# import json
# import sys
# from handler import main

# if __name__ == "__main__":
#     dict_param = json.loads(sys.argv[1])

#     response = main(dict_param, None)
#     print(response)

import json
from handler import main  # Assuming the Lambda code is saved in a file named `handler.py`

if __name__ == "__main__":
    # Simulated WebSocket input event
    simulated_event = {
        "requestContext": {
            "connectionId": "Eqk2Ie_lvHcCFQQ=",  # Simulated WebSocket connection ID
            "domainName": "ijiklmdla1.execute-api.us-west-2.amazonaws.com",
            "stage": "dev",
        },
        "body": json.dumps({
            "data": {
                "question": "Recommend me one package to predict toxicity"
            }
        })
    }

    # Call the Lambda function handler
    response = main(simulated_event, None)

    # Print the response for verification
    print(json.dumps(response, indent=2))
