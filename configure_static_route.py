from ncclient import manager
import xmltodict
import json
import yaml
from jinja2 import Template

with open('inventory.yml') as f:
    inventory = f.read()

inventory_dict = yaml.load(inventory)
# print(json.dumps(inventory_dict,indent=4))

device_list = inventory_dict['CORE']

netconf_template = Template(open('static_route_template.xml').read())

for device in device_list:
    host = device['host']
    route_list = device['static_route']

    print('----------------------------------------')
    print(f'Configuring Static Route on {host}')
    print('----------------------------------------')

    netconf_payload = netconf_template.render(route_list=route_list)

    # print(netconf_payload)

    # send the payload to the host
    with manager.connect(host=host, port='830',
                         username='cisco', password='cisco',
                         hostkey_verify=False) as m:

        netconf_reply = m.edit_config(netconf_payload, target='running')
        print(netconf_reply)
