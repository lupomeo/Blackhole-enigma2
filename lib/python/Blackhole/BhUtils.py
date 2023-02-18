# -*- coding: utf-8 -*-

from re import sub
from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_SKIN
# from Crypto.Cipher import AES
import xml.etree.cElementTree

entities = [
	("&#228;", u"ä"),
	("&auml;", u"ä"),
	("&#252;", u"ü"),
	("&uuml;", u"ü"),
	("&#246;", u"ö"),
	("&ouml;", u"ö"),
	("&#196;", u"Ä"),
	("&Auml;", u"Ä"),
	("&#220;", u"Ü"),
	("&Uuml;", u"Ü"),
	("&#214;", u"Ö"),
	("&Ouml;", u"Ö"),
	("&#223;", u"ß"),
	("&szlig;", u"ß"),


	("&#8230;", u"..."),
	("&#8211;", u"-"),
	("&#160;", u" "),
	("&#34;", u"\""),
	("&#38;", u"&"),
	("&#39;", u"'"),
	("&#60;", u"<"),
	("&#62;", u">"),


	("&lt;", u"<"),
	("&gt;", u">"),
	("&nbsp;", u" "),
	("&amp;", u"&"),
	("&quot;", u"\""),
	("&apos;", u"'"),
]

def nab_strip_html(html):
	# Newlines are rendered as whitespace in html
	html = html.replace('\n', ' ')

	# Multiple whitespaces are rendered as a single one
	html = sub('\s\s+', ' ', html)

	# Replace <br> by newlines
	html = sub('<br(\s+/)?>', '\n', html)

	# Replace <p>, <ul>, <ol> and end of these tags by newline
	html = sub('</?(p|ul|ol)(\s+.*?)?>', '\n', html)

	# Replace <li> by - and </li> by newline
	html = sub('<li(\s+.*?)?>', '-', html)
	html = html.replace('</li>', '\n')

	# And 'normal' stripping
	return nab_strip_pass1(html)

def nab_strip_pass1(html):
	# Strip enclosed tags
	html = sub('<(.*?)>', '', html)

	#	html = html.replace(escaped, unescaped)
	html.replace("&#196;", "Ä")
	html.replace("&#228;", "ä")
	html.replace("&auml;", "ä")
	html.replace("&#252;", "ü")
	html.replace("&uuml;", "ü")
	html.replace("&#246;", "ö")
	html.replace("&ouml;", "ö")
	html.replace("&#196;", "Ä")
	html.replace("&Auml;", "Ä")
	html.replace("&#220;", "Ü")
	html.replace("&Uuml;", "Ü")
	html.replace("&#214;", "Ö")
	html.replace("&Ouml;", "Ö")
	html.replace("&#223;", "ß")
	html.replace("&szlig;", "ß")
	html.replace("&lt;", "<")
	html.replace("&gt;", ">")
	html.replace("&nbsp;", " ")
	html.replace("&amp;", "&")
	html.replace("&quot;", "\"")
	html.replace("&apos;", "'")

	# Return result with leading/trailing whitespaces removed
	#return html.strip()
	return html

def nab_Read_CCCinfoCfg():
	myhost = "127.0.0.1"
	myuser = mypass = ""
	myport = "16001"
	if fileExists("/etc/delcccaminfo"):
		f = open("/etc/delcccaminfo",'r')
		for line in f.readlines():
			line = line.strip()
			if line.find('HOST ADDRESS:') != -1:
				myhost = line[13:]
			elif line.find('WEBINFO USERNAME:') != -1:
				myuser = line[17:]
			elif line.find('WEBINFO PASSWORD:') != -1:
				mypass = line[17:]
			elif line.find('WEBINFO LISTEN PORT:') != -1:
				myport = line[20:]

		f.close()

	myurl = "http://" + myhost + ":" + myport
	if myuser and mypass:
		myurl = "http://" + myuser + ":" + mypass + "@" + myhost + ":" + myport

	return [myhost, myuser, mypass, myport, myurl]

def nab_Write_CCCinfoCfg(mycfg):

	out = open("/etc/delcccaminfo", "w")
	strview = 'HOST ADDRESS:' + mycfg[0] + '\n'
	out.write(strview)
	strview = 'WEBINFO USERNAME:' + mycfg[1] + '\n'
	out.write(strview)
	strview = 'WEBINFO PASSWORD:' + mycfg[2] + '\n'
	out.write(strview)
	strview = 'WEBINFO LISTEN PORT:' + mycfg[3] + '\n'
	out.write(strview)
	out.close()

def DeliteGetSkinPath ():
	myskinpath = resolveFilename(SCOPE_CURRENT_SKIN, "")
	if myskinpath == "/usr/share/enigma2/":
		myskinpath = "/usr/share/enigma2/skin_default/"

	return myskinpath


def nab_Detect_Machine():
	machine = "dm8000"
	if fileExists("/etc/bhmachine"):
		f = open("/etc/bhmachine",'r')
		machine = f.readline().strip()
		f.close()
	return machine

def BhU_get_Version():
	ver = "1.0.0"
	if fileExists("/etc/bhversion"):
		f = open("/etc/bhversion",'r')
		ver = f.readline().strip()
		ver = ver.replace('BlackHole ', '')
		f.close()
	return ver

def BhU_check_proc_version():
	ver = ""
	if fileExists("/proc/blackhole/version"):
		f = open("/proc/blackhole/version",'r')
		ver = f.readline().strip()
		f.close()
	return ver


def BhU_checkSkinVersion(skinfile):
	version = "3.0.6"
	authors = ["Army", "Matrix10", "capa", "Ev0", "Thomas67"]
	ret = "Sorry this skin is not compatible with the current Black Hole image version."
	curversion = int(version.replace('.',''))
	fullfile = "/usr/share/enigma2/" + skinfile
	checkver = False
	checkauth = False
	if fileExists(fullfile):
		f = open(fullfile)
		for line in f.readlines():
			if line.find('black hole version:') != -1:
				parts = line.strip().split(':')
				ver = int(parts[1].strip().replace('.',''))
				if ver >= curversion:
					checkver = True
			elif line.find('skin author:') != -1:
				parts = line.strip().split(':')
				auth = parts[1].strip()
				for a in authors:
					if a == auth:
						checkauth = True
		f.close()
	if checkver == True:
		if checkauth == True:
			ret = "passed"

	return ret

def BhU_find_hdd():
	hdd = ""
	hdds = ['sda', 'sdb', 'sdc',  'sdd', 'sde', 'sdf']
	for device in hdds:
		filename = "/sys/block/%s/removable" % (device)
		if fileExists(filename):
			if file(filename).read().strip() == "0":
				hdd = device
				break
	return hdd


#def make_Delite_cipher():
#	key = 'AGA6A3A2ACA1A8A5A6A9A9A4A'
#	key += '6AGA3AFA3A6AEA1AEA2A7AC'
#	key = key.replace('A', '0')
#	key = key.replace('G', 'D')
#
#	def key_as_binary( key ):
#        	assert len(key) % 2 == 0
#        	binary_key = []
#        	for index in xrange(0,len(key),2):
#			binary_key.append( chr(int(key[index:index+2],16)) )
#		return ''.join( binary_key )
#
#	binary_key = key_as_binary( key )
#	cipher = AES.new(binary_key, AES.MODE_CBC)
#	return cipher

#def load_Nab_Crypted_skin(mpath, filename, dom_skins):
#	filenameb = filename.replace('skin.xml', 'skin.bin')
#	cipher = make_Delite_cipher()
#    	f = open(filenameb,'rb')
#        crypted_data = f.read()
#	f.close()
#	xml_data = cipher.decrypt( crypted_data )
#        out = open(filename, "wb")
#	zero_index = xml_data.find( '\0' )
#	if zero_index != -1:
#		xml_data = xml_data[:zero_index]
#	fd_index = xml_data.find( '\xfd' )
#	if fd_index != -1:
#		xml_data = xml_data[:fd_index]
#	out.write( xml_data )
#	out.close()
#	ret = (mpath, xml.etree.cElementTree.parse(filename).getroot())
#	out = open(filename, "wb")
#	out.write( "<skin>\n\tSorry this skin is crypted to protect the author copyright.\n\ \n</skin>\n" )
#	out.close()
#	dom_skins.append(ret)







