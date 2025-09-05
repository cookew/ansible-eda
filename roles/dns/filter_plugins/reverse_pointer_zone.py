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
    short_description: To convert IP addresses to a reverse DNS zone format.
    description:
        - Converts an IPv4 or IPv6 address to the reverse DNS zone format.
    options:
        ip:
            description:
            - ip address
            type: str
            required: True
        cidr:
            description:
            - cidr for the dns zone
            type: int
            required: True
    notes:
"""

EXAMPLES = r"""
#### Examples
# Reverse DNS Zone filter plugin with different queries.
  ansible.builtin.debug:
    msg:
      - "{{ '42:42:42:42:42:42:42:42' | reverse_pointer_zone(64) }}"
      - "{{ '42:42:42:42:42:42::42' | reverse_pointer_zone(56) }}"
      - "{{ '42:42:42:42:42:42::' | reverse_pointer_zone(48) }}"
      - "{{ '42:42:42:42:42::42' | reverse_pointer_zone(64) }}"
      - "{{ '42:42:42:42::42:42' | reverse_pointer_zone(72) }}"
      - "{{ 'fd42::' | reverse_pointer_zone(64) }}"
      - "{{ 'fd42:42::42:42:42:42' | reverse_pointer_zone(64) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(8) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(12) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(16) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(20) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(24) }}"
      - "{{ '42.42.42.42' | reverse_pointer_zone(28) }}"

# TASK [dns : Stuff] *******************************************************************************************************************************
# ok: [worker-3.cluster-1.wcooke.me -> localhost] =>
#   msg:
#   - 2.4.0.0.2.4.0.0.2.4.0.0.2.4.0.0.ip6.arpa
#   - 0.0.2.4.0.0.2.4.0.0.2.4.0.0.ip6.arpa
#   - 2.4.0.0.2.4.0.0.2.4.0.0.ip6.arpa
#   - 2.4.0.0.2.4.0.0.2.4.0.0.2.4.0.0.ip6.arpa
#   - 0.0.2.4.0.0.2.4.0.0.2.4.0.0.2.4.0.0.ip6.arpa
#   - 0.0.0.0.0.0.0.0.0.0.0.0.2.4.d.f.ip6.arpa
#   - 0.0.0.0.0.0.0.0.2.4.0.0.2.4.d.f.ip6.arpa
#   - 42.in-addr.arpa
#   - 42.42.in-addr.arpa
#   - 42.42.in-addr.arpa
#   - 42.42.42.in-addr.arpa
#   - 42.42.42.in-addr.arpa
#   - 42.42.42.42.in-addr.arpa
"""

RETURN = """
  data:
    type: str
    description:
    - Returns the reverse pointer DNS zone format of an IP address.
"""

@pass_environment
def _reverse_pointer_zone(*args, **kwargs):
    """This filter is designed to return the reverse pointer dns zone format of an IP address"""

    keys = ["ip", "cidr"]
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

    try:
        if isinstance(data["cidr"], int):
            pass
        else:
            raise AnsibleFilterError(
                "Unrecognized type <{0}> for reverse_pointer filter <{1}>".format(
                    type(data["cidr"]),
                    "cidr",
                ),
            )
    except (TypeError, ValueError):
        raise AnsibleFilterError(
            "Unrecognized type <{0}> for reverse_pointer filter <{1}>".format(type(data["cidr"]), "cidr"),
        )

    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="reverse_pointer")
    valid, errors, updated_data = aav.validate()

    if not valid:
        raise AnsibleFilterError(errors)
    return reverse_pointer_zone(**updated_data)


def reverse_pointer_zone(ip, cidr):
    if ipaddress.ip_address(ip).version == 4:
        split_count = int((32 - int(cidr)) / 8)
    elif ipaddress.ip_address(ip).version == 6:
        split_count = int((128 - int(cidr)) / 4)
    else:
        raise AnsibleFilterError('Unrecognized IP address version.')
    return ipaddress.ip_address(ip).reverse_pointer.split(".", split_count)[-1]


class FilterModule(object):
    """Reverse pointer manipulation filters"""

    filter_map = {
        "reverse_pointer_zone": _reverse_pointer_zone
    }

    def filters(self):
        """reverse_pointer filter"""
        return self.filter_map
