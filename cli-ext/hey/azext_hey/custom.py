# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import requests

def hey(cmd, keywords):
    print(str(keywords))
    r = requests.get('http://heyapi.trafficmanager.net/cli/' + ' '.join(keywords))
    return r.json()
    
