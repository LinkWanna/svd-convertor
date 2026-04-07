from typing import Any
from xml.etree import ElementTree as ET

from .utils import clean_text, parse_bool, parse_int, to_hex


def _text(node: ET.Element, tag: str) -> str | None:
    child = node.find(tag)
    if child is None:
        return None
    return clean_text(child.text)


def _parse_enum_values(field_node: ET.Element) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    enum_root = field_node.find("enumeratedValues")
    if enum_root is None:
        return result

    for enum_value in enum_root.findall("enumeratedValue"):
        value = parse_int(_text(enum_value, "value"))
        item: dict[str, Any] = {
            "name": _text(enum_value, "name"),
            "description": _text(enum_value, "description"),
            "value": to_hex(value),
        }
        result.append(item)

    return result


def _parse_fields(register_node: ET.Element) -> list[dict[str, Any]]:
    fields_root = register_node.find("fields")
    if fields_root is None:
        return []

    result: list[dict[str, Any]] = []
    for field_node in fields_root.findall("field"):
        bit_offset = parse_int(_text(field_node, "bitOffset"))
        bit_width = parse_int(_text(field_node, "bitWidth"))

        result.append(
            {
                "name": _text(field_node, "name"),
                "description": _text(field_node, "description"),
                "offset": bit_offset,
                "width": bit_width,
                "access": _text(field_node, "access"),
                "enumeratedValues": _parse_enum_values(field_node),
            }
        )

    return result


def _parse_register(register_node: ET.Element, base_address: int) -> dict[str, Any]:
    address_offset = parse_int(_text(register_node, "addressOffset")) or 0
    absolute_address = base_address + address_offset

    size = parse_int(_text(register_node, "size"))
    reset_value = parse_int(_text(register_node, "resetValue"))

    return {
        "name": _text(register_node, "name"),
        "displayName": _text(register_node, "displayName"),
        "description": _text(register_node, "description"),
        "addressOffset": to_hex(address_offset, width=4),
        "absoluteAddress": to_hex(absolute_address, width=8),
        "size": size,
        "access": _text(register_node, "access"),
        "resetValue": to_hex(reset_value),
        "fields": _parse_fields(register_node),
    }


def _parse_registers(peripheral_node: ET.Element, base_address: int) -> list[dict[str, Any]]:
    registers_root = peripheral_node.find("registers")
    if registers_root is None:
        return []

    registers: list[dict[str, Any]] = []
    for register_node in registers_root.findall("register"):
        registers.append(_parse_register(register_node, base_address=base_address))

    return registers


def _parse_interrupts(peripheral_node: ET.Element) -> list[dict[str, Any]]:
    interrupts: list[dict[str, Any]] = []
    for interrupt_node in peripheral_node.findall("interrupt"):
        value = parse_int(_text(interrupt_node, "value"))
        interrupts.append(
            {
                "name": _text(interrupt_node, "name"),
                "description": _text(interrupt_node, "description"),
                "value": value,
            }
        )
    return interrupts


def _parse_peripheral(peripheral_node: ET.Element) -> dict[str, Any]:
    base_address = parse_int(_text(peripheral_node, "baseAddress")) or 0

    return {
        "name": _text(peripheral_node, "name"),
        "description": _text(peripheral_node, "description"),
        "groupName": _text(peripheral_node, "groupName"),
        "derivedFrom": peripheral_node.attrib.get("derivedFrom"),
        "baseAddress": to_hex(base_address, width=8),
        "interrupts": _parse_interrupts(peripheral_node),
        "registers": _parse_registers(peripheral_node, base_address=base_address),
    }


def parse_svd(path: str) -> dict[str, Any]:
    tree = ET.parse(path)
    root = tree.getroot()

    cpu_node = root.find("cpu")
    cpu: dict[str, Any] = {}
    if cpu_node is not None:
        cpu = {
            "name": _text(cpu_node, "name"),
            "revision": _text(cpu_node, "revision"),
            "endian": _text(cpu_node, "endian"),
            "mpuPresent": parse_bool(_text(cpu_node, "mpuPresent")),
            "fpuPresent": parse_bool(_text(cpu_node, "fpuPresent")),
            "nvicPrioBits": parse_int(_text(cpu_node, "nvicPrioBits")),
            "vendorSystickConfig": parse_bool(_text(cpu_node, "vendorSystickConfig")),
        }

    peripherals_root = root.find("peripherals")
    peripherals: list[dict[str, Any]] = []
    if peripherals_root is not None:
        for peripheral_node in peripherals_root.findall("peripheral"):
            peripherals.append(_parse_peripheral(peripheral_node))

    result: dict[str, Any] = {
        "device": {
            "name": _text(root, "name"),
            "version": _text(root, "version"),
            "description": _text(root, "description"),
            "addressUnitBits": parse_int(_text(root, "addressUnitBits")),
            "width": parse_int(_text(root, "width")),
            "size": to_hex(parse_int(_text(root, "size"))),
            "resetValue": to_hex(parse_int(_text(root, "resetValue"))),
            "resetMask": to_hex(parse_int(_text(root, "resetMask"))),
            "cpu": cpu,
        },
        "peripherals": peripherals,
    }

    return result
