import pathlib
import binascii
import xml.etree.ElementTree as ET
from utils.log_init import log_set

logger = log_set('Parse_regy')


# FILE_PATH = 'regy_test_0.regy'  # for test use not formal

# def parser_method_test1():
#     # Parse the XML file
#     tree = ET.parse('PC1.5 TxD default MPR.regy')
#     root = tree.getroot()
#
#     # Extract the registry name
#     registry_name = root.find(".//REGISTRY").get("NAME")
#     print(f"Registry Name: {registry_name}")
#
#     # Extract the index and value pairs
#     index_values = {}
#     for val in root.findall(".//VALUE"):
#         index = int(val.get("INDEX"))
#         value = int(val.text)
#         index_values[index] = value
#     print(f"Index Values: {index_values}")
#
#
# def parser_method_test2():
#     # Parse the XML file
#     tree = ET.parse('LTE_B1_test.regy')
#     root = tree.getroot()
#
#     # Extract the registry names and values for B01 and B02
#     registries = {}
#     for registry in root.findall("./CATEGORY/REGISTRY"):
#         registry_name = registry.get("NAME")
#         if "B01" in registry_name or "B02" in registry_name:
#             values = {}
#             for value in registry.findall("./VALUE"):
#                 values[value.get("INDEX")] = value.text.strip()
#             registries[registry_name] = values
#
#     # Print the results
#     for registry_name, values in registries.items():
#         print("Registry Name:", registry_name)
#         print("Values:", values)


def regy_parser(file_name):
    # combine to file_path
    file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    # file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')
    for registry in registries:
        registry_name = registry.get('NAME')
        registry_size = registry.get('SIZE')
        values = registry.findall('.//VALUE')
        values_dict = {}
        for value in values:
            values_dict[int(value.get("INDEX")) - 1] = value.text.strip()
        values_dict['size'] = int(registry_size)
        registries_dict[registry_name] = values_dict

    # show the registries dictionary
    logger.info(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}

    # # to show the registry name and its value text and index
    # for reg_name, values_dict in registries_dict.items():
    #     logger.info(f'Registry namme: {reg_name}')
    #     logger.info(f'Values: {values_dict}')


def regy_parser_v2(file_name):
    # combine to file_path
    file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    # file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')
    for registry in registries:
        registry_name = registry.get('NAME')
        registry_size = int(registry.get('SIZE'))
        values = registry.findall('.//VALUE')

        values_strings = ','.join(
            [(convert_string(decimal_to_hex_twos_complement(int(value.text.strip()), registry_size), registry_size))
             for value in values])
        registries_dict[registry_name] = values_strings

    # show the registries dictionary
    logger.debug(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}


def regy_target_search_parser(file_name, target_name):
    # combine to file_path
    file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    # file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')

    for registry in registries:
        registry_name = registry.get('NAME')
        registry_size = registry.get('SIZE')
        if registry_name == target_name:
            values = registry.findall('.//VALUE')
            values_dict = {}
            for value in values:
                values_dict[int(value.get("INDEX")) - 1] = value.text.strip()
            values_dict['size'] = int(registry_size)
            registries_dict[registry_name] = values_dict
            break
        else:
            continue

    # show the registries dictionary
    logger.info(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}


def regy_target_search_parser_v2(file_name, target_name):
    # combine to file_path
    file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    # file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')

    for registry in registries:
        registry_name = registry.get('NAME')
        registry_size = int(registry.get('SIZE'))
        if registry_name == target_name:
            values = registry.findall('.//VALUE')

            values_strings = ','.join(
                [(convert_string(decimal_to_hex_twos_complement(int(value.text.strip()), registry_size), registry_size))
                 for value in values])
            registries_dict[registry_name] = values_strings
            break
        else:
            continue

    # show the registries dictionary
    logger.info(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}


def decimal_to_hex_twos_complement(num, size):
    """
    This is used for transfer negative and positive value to what LSI format is
    """
    bit_length = size * 8  # 1 byte = 1 size = 2 nibbles = 8 bits
    twos_complement = (1 << bit_length) + num
    hex_representation = hex(twos_complement & (2 ** bit_length - 1))[2:].zfill(bit_length // 4)
    return hex_representation


def convert_string(string, size):
    """
    This feature is used for register value transferred to at command use
    """
    # Convert the hex string to an integer
    n = int(string, 16)

    # Convert the integer to a byte array
    b = n.to_bytes(size, 'little')

    # Convert the byte array to a string
    # result = ",".join(["{:02x}".format(x) for x in b])
    result = ",".join([f"{x:02x}" for x in b])

    return result


def regy_write_test(file_name, target_name):  # this is prototype that is not used for others
    # combine to file_path
    # file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    # file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use
    file_path = pathlib.Path.cwd() / pathlib.Path(file_name)

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')

    for registry in registries:
        registry_name = registry.get('NAME')
        registry_size = registry.get('SIZE')
        if registry_name == target_name:
            values = registry.findall('.//VALUE')
            values[4].text = str(30)
            values[3].text = str(30)
            values[2].text = str(30)
            values[1].text = str(10)
            values[0].text = str(1)
            break
        else:
            continue

    # show the registries dictionary
    tree.write('output__.regy', encoding='utf-8', xml_declaration=True)


def regy_replace(file_name_base, file_name_changing, output_path):
    # Step 1: Parse the base XML file and need changing file
    original_xml_path = file_name_base
    tree_base = ET.parse(original_xml_path)
    root_base = tree_base.getroot()
    tree_changing = ET.parse(file_name_changing)
    root_changing = tree_changing.getroot()

    # Step 2: Find wanted name in regy that wants to change
    target_name_list = []
    registries_changings = root_changing.findall('.//REGISTRY')
    for registries_changing in registries_changings:
        target_name_list.append(registries_changing.get("NAME"))

    # Step 3: Search Base regy file and change the values for every specific NV
    for base_registry in root_base.findall(".//REGISTRY"):
        if base_registry.get("NAME") in target_name_list:
            base_name = base_registry.get("NAME")
            base_values = base_registry.findall(".//VALUE")
            specific_nv_parsed = root_changing.findall(f".//REGISTRY[@NAME='{base_name}']")[0]
            changing_values = specific_nv_parsed.findall(".//VALUE")

            for base_value_index in range(len(base_values)):
                base_values[base_value_index].text = changing_values[base_value_index].text

    # Step 4: Export to a new XML file with spaces for indentation
    new_regy_path = pathlib.Path(output_path) / pathlib.Path("New_Merged.regy")
    tree_base.write(new_regy_path, encoding='utf-8', xml_declaration=True)

    logger.info("New regy file generated successfully.")


def regy_extract(base_file_path, separate_file_path, output_path):
    # Step 1: Parse the original XML file
    original_xml_path = base_file_path
    target_name_list = read_separate_nv(separate_file_path)
    tree = ET.parse(original_xml_path)
    root = tree.getroot()

    # Step 2: Extract the desired items
    desired_items = []
    for category in root.findall(".//CATEGORY"):
        new_category = ET.Element("CATEGORY")
        new_category.set("NAME", category.get("NAME"))

        # for registry in category.findall(".//REGISTRY[@NAME='CAL.LTE.TX_PA_Range_Map_Rise_TX0_B27']"):
        for registry in category.findall(".//REGISTRY"):
            if registry.get("NAME") in target_name_list:
                new_registry = ET.Element("REGISTRY")
                new_registry.set("NAME", registry.get("NAME"))
                new_registry.set("TYPE", registry.get("TYPE"))
                new_registry.set("SIZE", registry.get("SIZE"))
                new_registry.set("STACKCOUNT", registry.get("STACKCOUNT"))

                for value in registry.findall(".//VALUE"):
                    new_value = ET.Element("VALUE")
                    new_value.set("INDEX", value.get("INDEX"))
                    new_value.text = value.text
                    new_registry.append(new_value)

                new_category.append(new_registry)

        if len(new_category) > 0:
            desired_items.append(new_category)

    # Step 3: Create a new XML structure
    new_root = ET.Element("NODE")
    for item in desired_items:
        new_root.append(item)

    # Step 4: Export to a new XML file with spaces for indentation
    prettify(new_root)
    new_xml_path = pathlib.Path(output_path) / pathlib.Path("new_separate.regy")
    tree = ET.ElementTree(new_root)
    tree.write(new_xml_path, encoding='utf-8', xml_declaration=True)

    print("New XML file generated successfully.")


def read_separate_nv(separat_file_path):
    target_name_list = []
    with open(separat_file_path, 'r') as f:
        for nv_name in f.readlines():
            target_name_list.append(nv_name.strip())

    return target_name_list



def prettify(elem, level=0):
    """Recursively adds spaces for indentation."""
    indent = " " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = "\n" + indent + " "
        if not elem.tail or not elem.tail.strip():
            elem.tail = "\n" + indent
        for elem in elem:
            prettify(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = "\n" + indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = "\n" + indent


def main():
    # from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
    # test = AtCmd()
    # file_name = 'temp_offset.regy'
    # target_name = '!LTERF.TX.USER DSP MPR OFFSET TX0 B01'
    # regy_dict = regy_target_search_parser(file_name, target_name)
    # for nv_name, regy_value in list(regy_dict.items()):
    #     for nv_index, nv_value in regy_value.items():
    #         test.set_google_nv(nv_name, nv_index, nv_value)
    # regy_parser(file_name)
    # xx = decimal_to_hex_twos_complement(-46, 2)
    # yy = convert_string(xx, 2)
    # print(xx)
    # print(yy)
    # print(yy.from_bytes(yy, byteorder='little', signed=True))
    # print(int("ffd2", 16))
    # regy_write_test('sw_point.regy', "CAL.LTE.TX_PA_Range_Map_Rise_TX0_B27")

    regy_replace('KM4_Common_RF_v0p1.regy',
                      'UHB_ PA Range MAP_ES2.regy')

    # print(decimal_to_hex_twos_complement(-5, 4))
    # print(convert_string(decimal_to_hex_twos_complement(-5, 4), 4))


if __name__ == '__main__':
    main()
