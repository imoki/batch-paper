import requests
from bs4 import BeautifulSoup
import urllib.parse
from lxml import etree
import re
import sys
import os

downpath = '.\\'
url = 'http://www.koovin.com/?q='
find_url ='http://www.koovin.com'
download_url ='http://www.koovin.com/?a=downloadpdf&'
#/html/body/div[2]/div[1]/div[2]/div[1]/h2/a
#/html/body/div[2]/div[1]/div[2]/div[2]/h2/a
#/html/body/div[2]/div[1]/div[2]/div[10]/h2/a
if __name__ == '__main__':
	os.system("title 批量下载论文")
	os.system("color f0")
	print("模式：")
	print("1	输入关键词，批量下载论文")
	print("2	输入关键词，选择文章，批量下载论文")
	print("输入非以上模式，则退出程序")
	model = input("请选择模式：")
	if model == '1':
		os.system('cls')
		name = input("请输入论文关键词：")
		url = url + name
		reply = requests.get(url)
		#html = etree.HTML(reply.text)	# 获取文本r.content
		soup = BeautifulSoup(reply.text, 'html.parser')
		pageurl_list = []
		for ids in soup.find_all('a'):
			pageurl = ids['href']
			urltmp = re.findall(r'http\:\/\/www.koovin.com\/\?q=',pageurl)
			if urltmp != []:
				#print(pageurl)
				pageurl_list.append(pageurl)
		pageurl = pageurl_list[0:-1]
		#根据关键词直接批量下载
		for url in pageurl:
			pagereply = requests.get(url)
			soup = BeautifulSoup(pagereply.text, 'html.parser')
			for ids in soup.find_all('a'):
				id = ids['href']
				idtmp = re.findall(r'\?a=',id)
				if idtmp != []:
					#id = urllib.parse.quote(id)
					#获取标题
					arcticle_url = find_url + id
					article_reply = requests.get(arcticle_url)
					titlehtml = etree.HTML(article_reply.text)
					title = titlehtml.xpath('//*[@id="resinfo"]//text()')[0].strip()
					title = re.sub(r'[\"\?|\\\/\*<>]','-',title)
					print("[+]获取 ", title)
					#下载连接
					subsoup = BeautifulSoup(article_reply.text, 'html.parser')
					pattern = re.compile(r'a=downloadpdf&(.*?)&doaction=download', re.MULTILINE | re.DOTALL)
					searchscript = subsoup.findAll('script',{'type':'text/javascript'})
					down_id = pattern.findall(str(searchscript))[0]
					realdownloadurl = download_url + down_id +'&doaction=download'
					#下载
					with open(r'./pdf/' + str(title) + '.pdf','wb') as fp:
						download = requests.get(realdownloadurl)
						fp.write(download.content)
						fp.close()
						print("[+]下载成功 ", title, "\n")
	elif model == '2':
		os.system('cls')
		name = input("请输入论文关键词：")
		url = url + name
		reply = requests.get(url)
		#html = etree.HTML(reply.text)	# 获取文本r.content
		soup = BeautifulSoup(reply.text, 'html.parser')
		pageurl_list = []
		for ids in soup.find_all('a'):
			pageurl = ids['href']
			urltmp = re.findall(r'http\:\/\/www.koovin.com\/\?q=',pageurl)
			if urltmp != []:
				#print(pageurl)
				pageurl_list.append(pageurl)
		pageurl = pageurl_list[0:-1]
		#根据关键词，选择文章下载
		realdownloadurl_list = []
		realtitle_list = []
		for url in pageurl:
			pagereply = requests.get(url)
			soup = BeautifulSoup(pagereply.text, 'html.parser')
			i = 0
			downloadurl_list = []
			title_list = []
			for ids in soup.find_all('a'):
				id = ids['href']
				idtmp = re.findall(r'\?a=',id)
				if idtmp != []:
					i = i+1
					#id = urllib.parse.quote(id)
					#获取标题
					arcticle_url = find_url + id
					article_reply = requests.get(arcticle_url)
					titlehtml = etree.HTML(article_reply.text)
					title = titlehtml.xpath('//*[@id="resinfo"]//text()')[0].strip()
					title = re.sub(r'[\"\?|\\\/\*<>]','-',title)
					title_list.append(title)
					print(i, "	", title)
					#下载连接
					subsoup = BeautifulSoup(article_reply.text, 'html.parser')
					pattern = re.compile(r'a=downloadpdf&(.*?)&doaction=download', re.MULTILINE | re.DOTALL)
					searchscript = subsoup.findAll('script',{'type':'text/javascript'})
					down_id = pattern.findall(str(searchscript))[0]
					realdownloadurl = download_url + down_id +'&doaction=download'
					downloadurl_list.append(realdownloadurl)
			choice = input("请输入需要下载文章的序号（用一个空格分隔序号,输入e结束选择）：")
			if choice == 'e':
				break
			choice_list = choice.strip().split(" ")
			os.system('cls')
			for i in choice_list:
				try:
					realdownloadurl_list.append(downloadurl_list[int(i)-1])
					realtitle_list.append(title_list[int(i)-1])
				except:
					print("[-]无序号", i, "，已忽略此项")
			print("")
		#下载
		print("[+] DOWNLOADING...")
		j = 0
		for i in realdownloadurl_list:
			print("[+]获取 ", realtitle_list[j])
			with open(r'./pdf/' + str(realtitle_list[j]) + '.pdf','wb') as fp:
				download = requests.get(i)
				fp.write(download.content)
				fp.close()
				print("[+]下载成功 ", realtitle_list[j], "\n")
			j = j+1
	else:
		sys.exit()





