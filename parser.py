#!/usr/bin/env python3
import re
from lxml import etree
ns = {'alto':'http://www.loc.gov/standards/alto/ns-v4#'}
in_file_name = 'btv1b52500967c_f78.xml'
out_file_name = 'out.ttl'
out_file = open(out_file_name, 'w', encoding = 'utf-8')
tree = etree.parse(in_file_name)
zone_dic = {}
for otherTag in tree.findall('.//alto:Tags/alto:OtherTag', namespaces=ns):
    zone_dic[otherTag.attrib['ID']] = otherTag.attrib['LABEL']
for textBlock in tree.findall('.//alto:TextBlock', namespaces=ns):
    TB_ID = textBlock.attrib['ID']
    ZONE_TYPE = zone_dic[textBlock.attrib['TAGREFS']]
    TB_HPOS = int(float(textBlock.attrib['HPOS']))
    TB_VPOS = int(float(textBlock.attrib['VPOS']))
    TB_WIDTH = int(float(textBlock.attrib['WIDTH']))
    TB_HEIGHT = int(float(textBlock.attrib['HEIGHT']))
    out_file.write(f''':{TB_ID} a :Zone ;
 crm:P1_is_identified_by [ a crm:E42_Identifier ; crm:P190_has_symbolic_content "{TB_ID}"^^xsd:string ] ;
 :has_zone_type :{ZONE_TYPE} ;
 :hpos "{TB_HPOS}"^^xsd:integer ;
 :vpos "{TB_VPOS}"^^xsd:integer ;
 :width "{TB_WIDTH}"^^xsd:integer ;
 :height "{TB_HEIGHT}"^^xsd:integer ;
''')
    for polygon in textBlock.findall('./alto:Shape/alto:Polygon', namespaces = ns):
        TB_POINTS = re.sub(r'(\d+ \d+)(?= \d)', r'\1,', polygon.attrib['POINTS'])
        out_file.write(f''' :has_shape [ a :Shape ; :has_polygon [ a :Polygon ; geo:as_polygon "POLYGON(({TB_POINTS}))"^^geo:wktLiteral ] ] .

''')
    for  textLine in textBlock.findall('./alto:TextLine', namespaces = ns):
        TL_ID = textLine.attrib['ID']
        BASELINE =re.sub(r'(\d+ \d+)(?= \d)', r'\1,', textLine.attrib['BASELINE'])
        TL_HPOS = int(float(textLine.attrib['HPOS']))
        TL_VPOS = int(float(textLine.attrib['VPOS']))
        TL_WIDTH = int(float(textLine.attrib['WIDTH']))
        TL_HEIGHT = int(float(textLine.attrib['HEIGHT']))
        out_file.write(f''':{TL_ID} a :Line ;
 crm:P1_is_identified_by [ a crm:E42_Identifier ; crm:P190_has_symbolic_content "{TL_ID}"^^xsd:string ] ;
 :P56i_is_found_on :{TB_ID} ;
 :has_baseline [ a :Baseline ; geo:as_linestring "LINESTRING({BASELINE})"^^geo:wktLiteral ] ;
 :hpos "{TL_HPOS}"^^xsd:integer ;
 :vpos "{TL_VPOS}"^^xsd:integer ;
 :width "{TL_WIDTH}"^^xsd:integer ;
 :height "{TL_HEIGHT}"^^xsd:integer ;
''')
        for polygon in textLine.findall('./alto:Shape/alto:Polygon', namespaces = ns):
            TL_POINTS = re.sub(r'(\d+ \d+)(?= \d)', r'\1,', polygon.attrib['POINTS'])
            out_file.write(f''' :has_shape [ a :Shape ; :has_polygon [ a :Polygon ; geo:as_polygon "POLYGON(({TL_POINTS}))"^^geo:wktLiteral ] ] .

''')
        for i, segment in enumerate(textLine.findall('./alto:String', namespaces = ns)):
            #SEG_ID = re.sub(r'_line_', '_seg_', ''.join([TL_ID, '_', str(i)]))
            SEG_CONTENT = segment.attrib['CONTENT']
            SEG_HPOS = int(float(segment.attrib['HPOS']))
            SEG_VPOS = int(float(segment.attrib['VPOS']))
            SEG_WIDTH = int(float(segment.attrib['WIDTH']))
            SEG_HEIGHT = int(float(segment.attrib['HEIGHT']))
            for j, token in enumerate(re.split(r' +', SEG_CONTENT)):
                SEG_ID = re.sub(r'_line_', '_seg_', ''.join([TL_ID, '_', str(j)]))
                out_file.write(f''':{SEG_ID} a :Segment ;
 crm:P1_is_identified_by [ a crm:E42_Identifier ; crmP190_has_symbolic_content "{SEG_ID}"^^xsd:string ] ;
 crm:P56i_is_found_on :{TL_ID} ;
 crm:P128_carries [ a :CharacterSequence ; rdf:value "{token}"^^xsd:string ] ;
 :hpos "{SEG_HPOS}"^^xsd:integer ;
 :vpos "{SEG_VPOS}"^^xsd:integer ;
 :width "{SEG_WIDTH}"^^xsd:integer ;
 :height "{SEG_HEIGHT}"^^xsd:integer .
            
''')
out_file.close()    
