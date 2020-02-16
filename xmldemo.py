#coding: utf-8
import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
# print(root.tag)
# print(root.attrib)

# for child in root:
#     print(child.tag, child.attrib)

# print(root[0][1].text)


# for neighbor in root.iter('neighbor'):
#     print(neighbor.attrib)


# for country in root.findall('country'):
#     rank = country.find('rank').text
#     name = country.get('name')
#     print(name, rank)

for c in root.findall("."):
    print(c)
