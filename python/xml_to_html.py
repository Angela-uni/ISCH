import os
from lxml import etree

# The folder containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Reach the project's root folder
root_dir = os.path.dirname(script_dir)

# Define paths based on the root folder
xml_file = os.path.join(root_dir, 'theCountOfMonteCristo.xml')
xslt_file = os.path.join(root_dir, 'xml-to-html.xslt')
output_file = os.path.join(root_dir, 'xml_to_html.html')

print("Uploading files...")
dom = etree.parse(xml_file)
style = etree.parse(xslt_file)

transform = etree.XSLT(style)

print("Conversion to HTML in progress...")
result = transform(dom)

# Save the result
with open(output_file, 'wb') as f:
    f.write(etree.tostring(result, pretty_print=True, encoding='UTF-8'))

print(f"Done! The page has been successfully saved in: {output_file}")