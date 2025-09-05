"""
filter plugin file for ipaddr filters: reverse_pointer
"""

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

import ipaddress

__metaclass__ = type

try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment

DOCUMENTATION = """
    name: reverse_pointer
    author: William Cooke
    version_added: "2.10.0"
    short_description: To convert IP addresses to a reverse DNS format.
    description:
        - Converts an IPv4 or IPv6 address to the reverse DNS format.
    options:
        ip:
            description:
            - list of subnets or individual address or any other values input for ipv4 plugin
            type: str
            required: True
    notes:
"""

EXAMPLES = r"""
#### Examples
# IPv4 filter plugin with different queries.
- name: Set value as input list
  ansible.builtin.set_fact:
    value:
      - 192.24.2.1
      - host.fqdn
      - ::1
      - ''
      - 192.168.32.0/24
      - fe80::100/10
      - 42540766412265424405338506004571095040/64
      - true

- name: IPv4 filter to filter Ipv4 Address
  debug:
    msg: "{{ value | ansible.utils.ipv4 }}"

- name: convert IPv4 addresses into IPv6 addresses.
  debug:
    msg: "{{ value | ansible.utils.ipv4('ipv6') }}"

- name: convert IPv4 addresses into IPv6 addresses.
  debug:
    msg: "{{ value | ansible.utils.ipv4('address') }}"

# PLAY [Ipv4 filter plugin with different queries.] ******************************************************************
# TASK [Set value as input list] ***************************************************************************************
# ok: [localhost] => {"ansible_facts": {"value": ["192.24.2.1", "host.fqdn", "::1", "", "192.168.32.0/24",
# "fe80::100/10", "42540766412265424405338506004571095040/64", true]}, "changed": false}
# TASK [IPv4 filter to filter Ipv4 Address] *******************************************************************
# ok: [localhost] => {
#     "msg": [
#         "192.24.2.1",
#         "192.168.32.0/24"
#     ]
# }
#
# TASK [convert IPv4 addresses into IPv6 addresses.] **********************************************************
# ok: [localhost] => {
#     "msg": [
#         "::ffff:192.24.2.1/128",
#         "::ffff:192.168.32.0/120"
#     ]
# }
#
# TASK [convert IPv4 addresses into IPv6 addresses.] **********************************************************
# ok: [localhost] => {
#     "msg": [
#         "192.24.2.1"
#     ]
# }
"""

RETURN = """
  data:
    type: str
    description:
    - Returns the reverse pointer format of an IP address.
"""

@pass_environment
def _reverse_pointer(*args, **kwargs):
    """This filter is designed to return the reverse pointer format of an IP address"""

    keys = ["ip"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)

    try:
        if isinstance(data["ip"], str):
            pass
        else:
            raise AnsibleFilterError(
                "Unrecognized type <{0}> for reverse_pointer filter <{1}>".format(
                    type(data["ip"]),
                    "ip",
                ),
            )
    except (TypeError, ValueError):
        raise AnsibleFilterError(
            "Unrecognized type <{0}> for reverse_pointer filter <{1}>".format(type(data["ip"]), "ip"),
        )

    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="reverse_pointer")
    valid, errors, updated_data = aav.validate()

    if not valid:
        raise AnsibleFilterError(errors)
    return reverse_pointer(**updated_data)


def reverse_pointer(ip):
    return ipaddress.ip_address(ip).reverse_pointer


class FilterModule(object):
    """Reverse pointer manipulation filters"""

    filter_map = {
        "reverse_pointer": _reverse_pointer
    }

    def filters(self):
        """reverse_pointer filter"""
        return self.filter_map
