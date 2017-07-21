#This python code takes in a folder path of documents and generates a corresponding XML file
#with head,title,year,county,abstract,references tag

import os
import subprocess 
from subprocess import PIPE
from difflib import SequenceMatcher
import editdistance

def similar(a,b):
	return SequenceMatcher(a,b).get_matching_blocks()

def findNewSimi(title,head):
	if(head.find(" ")<=head.find("\n")):
		head=head.replace(" ","",1)
	else:
		head=head.replace("\n","",1)
	val=similar(title,head)
	return (val,head)

#storefolder path in f
folder= "/home/bhardwaj/Documents/Conference Dataset/ICDAR Downloads Test/1993/pdfs/"
countryfile="/home/bhardwaj/Documents/code for ICDAR paper 2017/paper code/country.txt"
year='1993'

for subdir,dirs,files in os.walk(folder):
	for file in files:
		if not os.path.exists(folder+'PDFToTXT/'):
			os.makedirs(folder+'PDFToTXT')
		p=os.path.join(subdir, file)
		print p
		#result=subprocess.Popen(['pdftotext',p,folder+'PDFToTXT/'+file+'.txt'],stdout=PIPE,stderr=PIPE)
		result=subprocess.Popen(['java','-jar','docears-pdf-inspector.jar','-text','-title' ,p],stdout=PIPE,stderr=PIPE)
		resultstring= result.communicate()[0]
		#if not os.path.exists(folder+'PDFInspector/'):
			#os.makedirs(folder+'PDFInspector')
		#result=subprocess.Popen(['java','-jar','docears-pdf-inspector.jar','-title',p],stdout=PIPE,stderr=PIPE)
		#text= result.communicate()[0]
		# title= text.split('|')[0]
		# body=text.split('|')[1]
		# head=body.lower().split('abstract')[0]
		# print head
		f=open(folder+'PDFToTXT/'+file+'.txt','wb')
		#f.write('<title> '+ result.communicate()[0]+' </title>')
		#f.write('<body> '+ str(result.communicate()[0])+' </body>')
		f.write(str(resultstring))
		# f.write('title :' + title+'\n')
		# f.write('body :' +body)
		#f.close()
	break

count_of_abstract=1
count_of_ref=1
b=False
country=''
head=''
abstract=''
references=''
ref_flag=False
countrylist=[line.rstrip('\n') for line in open(countryfile)]
while '' in countrylist:
	countrylist.remove('')



for subdir,dirs,files in os.walk(folder+'PDFToTXT'):
	for file in files:
		if not os.path.exists(folder+'XML/'):
			os.makedirs(folder+'XML/')
		abs_filepath=os.path.join(subdir,file)
		print abs_filepath
		with open(abs_filepath,'rb') as ins:
			references=''
			b=False
			ref_flag=False
			head=''
			country=''
			abstract=''
			abstract_line=0
			for i,line in enumerate(ins):
				if(b==False):
					head=head+line

				if (b==False and ('abstract' in line.lower() or (editdistance.eval('abstract',line.lower()))<=5 or 'introduction' in line.lower())):
					print 'abstract line'+line,i 
					
					abstract_line=i
					count_of_abstract=count_of_abstract+1
					print 'count of abstract '+str(count_of_abstract)
					b=True
					head= head[:head.rfind('\n')]
					head= head[:head.rfind('\n')]
					#print head
					for x in countrylist:
						if x.lower() in head.lower():
							country=x
							print country
							break

				if b==True and i>abstract_line and i<abstract_line+20:
					print 'abstract line'+line
					abstract=abstract+line

				if ((editdistance.eval('references',line.lower())<=6) or (editdistance.eval('bibliography',line.lower())<=6)):
					count_of_ref=count_of_ref+1
					ref_flag=True
					print 'Count of references '+str(count_of_ref)
					#print i,line

				if(ref_flag==True):
					references=references+line
		if(b==False):
			print 'Abstract not found in: '+abs_filepath

		print 'ABSTRACT is here:  ***'+abstract
		print head
		print year
		print country
		print references
		f=open(folder+'XML/'+file,'wb')
		f.write('<year> '+year+' </year>\n')
		f.write('<head> '+head+' </head>\n')
		f.write('<country> '+country+' </country>\n')
		f.write('<abstract> '+abstract+' </abstract>\n')
		f.write('<References> '+references+' </References>\n')
		f.close()
		
		if(ref_flag==False):
			print 'Reference not found in: '+abs_filepath
		if country=='':
			print 'country not found in: '+abs_filepath