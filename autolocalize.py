#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

import localizable
from googletrans import Translator

if len(sys.argv) != 2:
	print "usage: autolocalize.py File.strings"
	exit(1)

srcLang = "en"
srcFile = sys.argv[1]
srcFilename = os.path.basename(srcFile)
languages = ["zh-CN", "zh-TW", "ja", "ko", "de", "fr", "it", "es", "pt", "ms"]

strings = localizable.parse_strings(filename=srcFile)
translator = Translator()

def header(lang):
	return "/*\n\
  {}\n\
  Generated with autolocalize - https://github.com/mattlawer/autolocalize\n\
  \n\
  Translated from {} to {} on {}.\n\
*/\n\n\n".format(srcFilename, srcLang, lang, time.strftime("%x"))

for l in languages:
	lproj = "{}.lproj".format(l.replace("zh-CN", "zh-Hans").replace("zh-TW", "zh-Hant"))
	print("\33[1;36mgenerating {}\33[0m".format(lproj))
	path = os.path.join(os.getcwd(), lproj)
	if not os.path.exists(path):
		os.makedirs(path)
	
	stringsFile = open(os.path.join(lproj, srcFilename), "w")
	stringsFile.write(header(l)) 
	for stringRef in strings:
		value = stringRef['value']
		comment = "/* {} - {}*/\n".format(stringRef['comment'], value)
		stringsFile.write(comment)
		translated = ""
		try:
			translated = translator.translate(value, src=srcLang, dest=l).text
		except:
			print("\33[1;31merror translating: \33[1;33m{}\33[0m".format(value))
		line = "\"{}\" = \"{}\";\n\n".format(stringRef['key'], translated)
		stringsFile.write(line)
		time.sleep(0.5) # try not to flood google translate
	stringsFile.close() 
