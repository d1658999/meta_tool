import pathlib
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
    # file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use
    file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')
    for registry in registries:
        registry_name = registry.get('NAME')
        values = registry.findall('.//VALUE')
        values_dict = {}
        for value in values:
            values_dict[int(value.get("INDEX"))-1] = value.text.strip()
        registries_dict[registry_name] = values_dict

    # show the registries dictionary
    logger.info(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}

    # # to show the registry name and its value text and index
    # for reg_name, values_dict in registries_dict.items():
    #     logger.info(f'Registry namme: {reg_name}')
    #     logger.info(f'Values: {values_dict}')


def regy_target_search_parser(file_name, target_name):
    # combine to file_path
    # file_path = pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # formal use
    file_path = pathlib.Path.cwd().parent / pathlib.Path('regy_file_parse') / pathlib.Path(file_name)  # test use

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract the registry name
    registries_dict = {}
    registries = root.findall('.//REGISTRY')

    for registry in registries:
        registry_name = registry.get('NAME')
        if registry_name == target_name:
            values = registry.findall('.//VALUE')
            values_dict = {}
            for value in values:
                values_dict[int(value.get("INDEX")) - 1] = value.text.strip()
            registries_dict[registry_name] = values_dict
            break
        else:
            continue

    # show the registries dictionary
    logger.info(registries_dict)

    return registries_dict  # key is NV name, values are the dict of {index: value.text}


def main():
    # from equipments.series_basis.modem_usb_serial.serial_series import AtCmd
    # test = AtCmd()
    # file_name = 'regy_test_0.regy'
    # target_name = '!LTERF.TX.USER DSP MPR OFFSET TX0 B01'
    # regy_dict = regy_target_search_parser(file_name, target_name)
    # for nv_name, regy_value in list(regy_dict.items()):
    #     for nv_index, nv_value in regy_value.items():
    #         test.set_google_nv(nv_name, nv_index, nv_value)
    pass


if __name__ == '__main__':
    main()
