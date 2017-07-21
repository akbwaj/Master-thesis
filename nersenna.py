#This program extracts an author's name from this document
from nltk.tag import SennaNERTagger
import os
import re
nertagger=SennaNERTagger('/home/bhardwaj/Documents/zipped folders/senna')

XMLfolder=('/home/bhardwaj/Documents/Conference Dataset/ICDAR Downloads Test/ICDAR2015/papers/XML/')
year='2015'
for file in os.listdir(XMLfolder):
	name=[]
	country=''
	keywords=[]

	abspath=os.path.join(XMLfolder,file)
	print abspath
	f=open(abspath,'r')
	for line in f:
		if ('<country>') in line:
			country= line[9:-11]
			print country
			break
		#print line
		newline= re.sub(r'[,]',' , ',line)
		newline= re.sub(' \.','.',newline)
		#print newline
		#to remove all non-ascii charaters from the line
		#print re.sub(r'\W+',' ',line)
		s= nertagger.tag(newline.decode('utf8').split())
		#print s

		
		for idx, x in enumerate(s):
			firstname=''
			intermediatename=''
			lastname=''
			word=''
			#print idx,x
			if x[1]== 'B-PER':
				firstname= x[0]
				#print firstname
				#print s
				try:
					if s[idx+1][1]=='I-PER':
						intermediatename= s[idx+1][0]
						word=(firstname+' '+intermediatename)
						#print s
						try:
							if s[idx+2][1]=='E-PER':
								lastname=s[idx+2][0]
								word=(firstname+' '+intermediatename+' '+lastname)
								#print word
							elif s[idx+2][1]=='I-PER':
								lastname=s[idx+2][0]
								word=(firstname+' '+intermediatename+' '+lastname)
								#print word
						except IndexError:
							word=(firstname+' '+intermediatename)
							#print 'NI'
					elif s[idx+1][1]=='E-PER':
						lastname=s[idx+1][0]
						word=firstname+' '+lastname
						#print word
				except IndexError:
					word=firstname
					#print 'NI'
				#print 'here '+word
				if (word not in name and word !=''):
					name.append(word)
			else:
				continue
	if name:
		for n in name:
			print n.encode('utf8')
	f.close()
	f= open('15countryauthor.csv','a')
	f.write(country+','+year+','+ str(name)+'\n')
	f.close()
	

	#Code for extraction of keywords
	##################################
	##################################
	# f2=open(abspath,'r')
	# string = f2.read()
	# title=re.findall(r'<title>(.*?)</title>',string,re.DOTALL)
	# string=re.findall(r'<abstract>(.*?)</abstract>',string,re.DOTALL)
	# string1 =title[0] + string[0]
	# print string1
	# f2.close()