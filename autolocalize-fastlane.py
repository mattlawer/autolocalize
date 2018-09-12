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
	print "usage: autolocalize-fastlane.py /path/to/fastlane/metadata"
	exit(1)

srcLang = "en"
srcFolderLang = "en-US"
tolocalize = ["name", "subtitle", "promotional_text", "description", "release_notes", "keywords"]
metadataPath = sys.argv[1]
srcFolder = os.path.join(metadataPath, srcFolderLang)
languages = ["zh-CN", "zh-TW", "ja", "ko", "de", "fr", "it", "es", "pt", "ms"]

translator = Translator()

for l in languages:
	lang = l.replace("zh-CN", "zh-Hans").replace("zh-TW", "zh-Hant").replace("fr", "fr-FR").replace("es", "es-ES").replace("pt", "pt-BR").replace("de", "de-DE")
	print("\33[1;36mgenerating {}\33[0m".format(lang))
	destFolder = os.path.join(metadataPath, lang)
	if not os.path.exists(destFolder):
		os.makedirs(destFolder)
	
	for filename in tolocalize:
		srcPath = os.path.join(srcFolder, filename+".txt")
		destPath = os.path.join(destFolder, filename+".txt")
		print(srcPath)
		print(destPath)
		srcFile = open(srcPath, "r")
		destFile = open(destPath, "w")
		try:
			translated = translator.translate(srcFile.read(), src=srcLang, dest=l).text
			destFile.write(translated)
		except:
			print("\33[1;31merror translating: \33[1;33m{}\33[0m".format(srcFile.read()))
		time.sleep(0.5) # try not to flood google translate
		srcFile.close() 
		destFile.close() 
