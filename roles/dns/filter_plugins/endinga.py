"""
filter plugin file for ipaddr filters: ending
"""

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

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
        input_string:
            description:
            - Input string
            type: str
            required: True
        end_string:
            description:
            - Ending string
            type: str
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
      - Returns the ending format of an IP address.
"""

@pass_environment
def _ending(*args, **kwargs):
    """This filter is designed to return the ending format of an IP address"""

    keys = ["input_string", "end_string"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)

    try:
        if isinstance(data["input_string"], str):
            pass
        else:
            raise AnsibleFilterError(
                "Unrecognized type <{0}> for ending filter <{1}>".format(
                    type(data["input_string"]),
                    "input_string",
                ),
            )
    except (TypeError, ValueError):
        raise AnsibleFilterError(
            "Unrecognized type <{0}> for ending filter <{1}>".format(type(data["input_string"]), "input_string"),
        )

    try:
        if isinstance(data["end_string"], str):
            pass
        else:
            raise AnsibleFilterError(
                "Unrecognized type <{0}> for ending filter <{1}>".format(
                    type(data["end_string"]),
                    "end_string",
                ),
            )
    except (TypeError, ValueError):
        raise AnsibleFilterError(
            "Unrecognized type <{0}> for ending filter <{1}>".format(type(data["end_string"]), "end_string"),
        )

    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="ending")
    valid, errors, updated_data = aav.validate()

    if not valid:
        raise AnsibleFilterError(errors)
    return ending(**updated_data)


def ending(input_string, end_string):
    if input_string.endswith(end_string):
        return str(input_string)
    else:
        return "{0}{1}".format(str(input_string), end_string)


class FilterModule(object):
    """Ending manipulation filters"""

    filter_map = {
        "ending": _ending
    }

    def filters(self):
        """ending filter"""
        return self.filter_map
