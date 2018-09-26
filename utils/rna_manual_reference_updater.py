# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# ##### RNA MANUAL REFERENCES #####
#
# This file geneates a file that maps RNA strings to online URL's
# for the context menu documentation access
#
# To make international, we made a script,
# pointing the manuals to the proper language,
# specified in the 'User Preferences Window' by the users.
# Some Languages have their manual page, using a prefix or
# being preceded by their respective reference, for example:
#
# manual/ --> manual/ru/
#
# The table in the script, contains all of the languages we have in the
# Blender manual website, for those other languages that still
# does not have a team of translators,
# and/or don't have a manual for their languages we commented the lines below,
# you should add them to the language table when they have a proper manual,
# or added to the Blender UI  translation table.
#
# URL is the: url_manual_prefix + url_manual_mapping[#id]

import os
import sphobjinv
import urllib.request

# Download the objects.inv file
urlretrieve = urllib.request.urlretrieve
urlretrieve("https://docs.blender.org/manual/en/dev/objects.inv", "objects.inv")

# Decode objects.inv
objects = sphobjinv.readfile('objects.inv')
objects_data = sphobjinv.decode(objects)
sphobjinv.writefile('objects.tmp', objects_data)  # TODO leave in memory
os.remove("objects.inv")


# Write the fire
filepath = os.path.join("rna_manual_reference.py")
file = open(filepath, "w", encoding="utf-8")
fw = file.write

fw("# Do not edit this file.")
fw(" This file is auto genereated from rna_manual_reference_updater.py\n\n")
fw("import bpy\n\n")
fw("url_manual_prefix = \"https://docs.blender.org/manual/en/dev/\"\n\n")
fw("language = \"\"\n")
fw("if bpy.context.user_preferences.system.use_international_fonts:\n")
fw("    language = bpy.context.user_preferences.system.language\n")
fw("    if language == 'DEFAULT':\n")
fw("        import os\n")
fw("        language = os.getenv('LANG', '').split('.')[0]\n\n")
fw("LANG = {\n")
# fw("    \"ar_EG":         \"ar",\n")
# fw("    \"bg_BG":         \"bg",\n")
# fw("    \"ca_AD":         \"ca",\n")
# fw("    \"cs_CZ":         \"cz",\n")
fw("    \"de_DE\":        \"de\",\n")  # German
# fw("    \"el_GR":         \"el",\n")
fw("    \"ru_RU\":        \"ru\",\n")  # Russian
# fw("    \"sr_RS":         \"sr",\n")
# fw("    \"sv_SE":         \"sv",\n")
# fw("    \"tr_TR":         \"th",\n")
# fw("    \"uk_UA":         \"uk",\n")
fw("    \"es\":           \"es\",\n")  # Spanish
# fw("    \"fi_FI":         \"fi",\n")
fw("    \"fr_FR\":        \"fr\",\n")  # French
# fw("    \"id_ID":         \"id",\n")
fw("    \"it_IT\":        \"it\",\n")  # Italian
fw("    \"ja_JP\":        \"ja\",\n")  # Japanese
fw("    \"ko_KR\":        \"ko\",\n")  # Korean
# fw("    \"nl_NL":         \"nl",\n")
# fw("    \"pl_PL":         \"pl",\n")
fw("    \"pt_PT\":        \"pt\",\n")  # Portuguese
fw("    \"pt_BR\":        \"pt\",\n")  # Portuguese - for until we have a pt_BR version
fw("    \"zh_CN\":        \"zh.cn\",\n")  # Chinese - Should be changed to "zh_cn" but there is a bug in sphinx-intl
fw("    \"zh_TW\":        \"zh.tw\",\n")  # Taiwanese Chinese
fw("}.get(language)\n\n")
fw("if LANG is not None:\n")
fw("    url_manual_prefix = url_manual_prefix.replace(\"manual/en\", \"manual/\" + LANG)\n\n")
fw("url_manual_mapping = (\n")


# Logic to manipulate strings from objects.inv
with open("objects.tmp", encoding="utf8") as obj_tmp:
    lines = [l for l in obj_tmp if (l.startswith("bpy.types") or l.startswith("bpy.ops"))]
    lines.sort(key=lambda l: l.find(" "), reverse=True)  # Finding first space will return length of rna path...
    for line in lines:
        split = line.split(" ")
        fw("\t(\"" + split[0] + "*\", \"" + split[3] + "\"),\n")

fw(")\n")

os.remove("objects.tmp")
