#!/usr/bin/env python
try:
    # For Python 3+
    from urllib.request import urlopen
except ImportError:
    # For Python 2
    from urllib2 import urlopen

import sys, getopt
import json
import os

def usage():
	print "-p : Full path to local copy of 'projects' directory\n-u : URL of 'projects' directory"

def getJson(url):
    try:
        response = urlopen(url)
        data = str(response.read())
    except:
        print '[-] Failed to fetch url '+url
        return None

    try:
        return json.loads(data)
    except:
        print '[-] Invalid json '+url
        return None

try:
	opts, args = getopt.getopt(sys.argv[1:], ":p:u:")
except getopt.GetoptError as err:
	print str(err)
	usage()
	sys.exit(2)

for opt,val in opts:
	if opt in ('-p'):
		projectsJsonDir = val
	elif opt in ('-u'):
		pathToCatalog = val

try:
    if projectsJsonDir and pathToCatalog:
        projectsJson = projectsJsonDir + '/projects.json'
        if os.path.isdir(projectsJsonDir) and os.path.isfile(projectsJson):
            with open(projectsJson, 'r') as projectsFile:
                data=projectsFile.read().replace('\n', '')
            projectsData = json.loads(data)
            groupName = ''
            for key in projectsData.keys():
                groupName = key
            if groupName == '':
                print '[-] projects.json has invalid format'
                sys.exit(2)
        else:
            print '[-] Could not find projects.json file in '+projectsJsonDir+' directory'
            sys.exit(2)
        print '[+] projects.json ('+projectsJsonDir+'/projects.json) parsed successfully'
except:
	print '[-] projects.json ('+projectsJsonDir+'/projects.json) was not parsed successfully'
	sys.exit(2)

projVars = ['projectName','projectStatus', 'projectShortDescription', 'projectDescription', 'projectContacts','projectMembers','projectSlogan', 'projectLogo', 'whoIsNeeded', 'projectTags']
projVarsContacts = ['www','github', 'telegram', 'email', 'twitter']

pageHeader = '''
<html>
<head>
    <!-- Bootstrap core CSS -->
    <link href="'''+pathToCatalog+'''/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap theme -->
    <link href="'''+pathToCatalog+'''/css/bootstrap-theme.min.css" rel="stylesheet">

    <link href="'''+pathToCatalog+'''/jumbotron-narrow.css" rel="stylesheet">
</head>
<title>TITLE_HERE</title>
<br><br><br><br>

<div class="container" role="main">
	<div class="page-header" align=right>
	  <small>'''+groupName+'''</small>
	</div>
'''

pageLinks = '''
	<ul class="nav nav-pills nav-justified"">
		<li role="presentation" PROJECTS_IS_ACTIVE><a href="'''+pathToCatalog+'''/">projects</a></li>
		<li role="presentation" IDEAS_IS_ACTIVE><a href="'''+pathToCatalog+'''/ideas/">ideas</a></li>
		<li role="presentation" SUBMIT_IS_ACTIVE><a href="'''+pathToCatalog+'''/submit/">submit</a></li>
		<li role="presentation" ABOUT_IS_ACTIVE><a href="'''+pathToCatalog+'''/about/">about</a></li>
	</ul>

	<br>
'''

pageFooter = '''
</div>
</body>
</html>
'''

def htmlEscape(str):
   str = str.replace("&","&amp;")
   str = str.replace("<", "&lt;")
   str = str.replace(">", "&gt;")
   return str

def writeToFile(path,content):
    if not os.path.exists(path) or os.path.isfile(path):
        fd = open(path,'w')
        fd.write(content)
        fd.close()

def processProjectJson(pid,pUrl):
    projectData = getJson(pUrl)
    if projectData == None:
        return None
    projectPath = projectsJsonDir+str(pid)

    if not os.path.isdir(projectPath) and not os.path.exists(projectPath):
        os.makedirs(projectPath)
    for pVar in projVars:
        try:
            if not (pVar == 'projectContacts' or pVar== 'projectMembers' or pVar=='whoIsNeeded' or pVar=='projectTags'):
                projectData[pVar] = projectData[pVar]

        except:
			if pVar == 'projectContacts' or pVar== 'projectMembers' or pVar=='whoIsNeeded':
				projectData[pVar] = {}
			else:
				projectData[pVar] = ''

	for pVar in projVarsContacts:
		try:
			projectData['projectContacts'][pVar] = projectData['projectContacts'][pVar]
		except:
			projectData['projectContacts'][pVar] = ''

	for pVar in projectData['projectMembers']:
		for vVal in projVarsContacts:
			try:
				projectData['projectMembers'][pVar][vVal] = projectData['projectMembers'][pVar][vVal]
			except:
				projectData['projectMembers'][pVar][vVal] = ''

    if not not os.path.exists(projectPath+'/project.json'):
        writeToFile(projectPath+'/project.json',json.dumps(projectData))

    return projectData

def buildProjectsPage(data):
	page = ''
	for i,k in enumerate(data):
		page = page + '''
		<div class="panel panel-default">
			<div class="panel-heading"><b>Project: </b><a href="'''+pathToCatalog+'''/'''+str(k)+'''/" title="View project page">'''+data[k]['projectName']+'''</a></div>

			<table class="table">
				<tr>
					<td width="90%"><b>Description: </b>'''+data[k]['projectShortDescription']+'''</td><td width="10%"><img src="'''+data[k]['projectLogo']+'''" width="55px" height="55px"></img>
				</tr>
				<tr>
					<td><b>Status: </b>'''+data[k]['projectStatus']+'''</td>
				</tr>

				<tr>
					<td><b>Tags: </b>'''+', '.join(data[k]['projectTags'])+'''</td>
				</tr>
			</table>
		</div>

		'''

	pageHeaderP = pageHeader.replace('TITLE_HERE','projects')
	pageLinksP = pageLinks.replace('PROJECTS_IS_ACTIVE','class="active"')
	pageLinksP = pageLinksP.replace('IDEAS_IS_ACTIVE','')
	pageLinksP = pageLinksP.replace('SUBMIT_IS_ACTIVE','')
	pageLinksP = pageLinksP.replace('ABOUT_IS_ACTIVE','')
	page = pageHeaderP + pageLinksP + page + pageFooter
	return page


def buildContacts(contactsData,elemList):
	pContacts = []
	for pContact in elemList:
		if contactsData[pContact] != '':
			if pContact == 'email':
				pContacts.append('<a href="mailto:'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			elif pContact== 'twitter':
				pContacts.append('<a href="https://twitter.com/'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			elif pContact== 'github':
				pContacts.append('<a href="https://github.com/'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')
			else:
				pContacts.append('<a href="'+htmlEscape(contactsData[pContact])+'">'+pContact+'</a>')

	return pContacts

def buildProjectPage(id,data):

	page = '''
	<div class="panel panel-default">
		<div class="panel-heading"><b>Project: </b><a href="/projects/'''+htmlEscape(str(id))+'''">'''+htmlEscape(data['projectName'])+'''</a><img src="'''+htmlEscape(data['projectLogo'])+'''" width="25px" height="25px" align="right"></img></div>

		<table class="table">
			<tr>
				<td><b>Slogan: </b>'''+htmlEscape(data['projectSlogan'])+'''</td>
			</tr>
			<tr>
				<td><b>Description: </b>'''+htmlEscape(data['projectDescription'])+'''</td>
			</tr>
			<tr>
				<td><b>Status: </b>'''+htmlEscape(data['projectStatus'])+'''</td>
			</tr>

			<tr>
				<td width="70%"><b>Tags: </b>'''+htmlEscape(', '.join(data['projectTags']))+'''</td>
			</tr>

		</table>
	</div>

	<div class="panel panel-default">
		<div class="panel-heading"><b>Project needs</b></div>
		<table class="table">
	'''

	for i in data['whoIsNeeded']:
		page = page + '''
			<tr>
			   <td><b>'''+htmlEscape(i)+'''</b> - '''+htmlEscape(data['whoIsNeeded'][i])+'''</td>
			</tr>

	'''

	page = page + '''
			<tr>
			   <td><b>You</b> - because you are a part of community</td>
			</tr>
		</table>

	</div>
	<div class="panel panel-default">
		<div class="panel-heading"><b>Contacts</b></div>

		<table class="table">
	'''

	pContacts = buildContacts(data['projectContacts'],projVarsContacts)

	if len(pContacts)>0:
		page = page + '<tr><td>Project related: '+' | '.join(pContacts)+'</td></tr>'
	else:
		page = page + '<tr><td>Project related: none</td></tr>'


	for pVar in projectData['projectMembers']:
		pContacts = buildContacts(data['projectMembers'][pVar],projVarsContacts)
		page = page + '<tr><td>'+htmlEscape(pVar)+': '+' | '.join(pContacts)+'</td></tr>'

	page = page + '''
		</table>
	</div>
	'''

	pageHeaderP = pageHeader.replace('TITLE_HERE',data['projectName'])
	pageLinksP = pageLinks.replace('PROJECTS_IS_ACTIVE','')
	pageLinksP = pageLinksP.replace('IDEAS_IS_ACTIVE','')
	pageLinksP = pageLinksP.replace('SUBMIT_IS_ACTIVE','')
	pageLinksP = pageLinksP.replace('ABOUT_IS_ACTIVE','')
	page = pageHeaderP + pageLinksP + page + pageFooter
	return page

def buildStaticPage(path,static):
    if not os.path.exists(path+'/'+static+'/'):
        os.mkdir(path+'/'+static+'/')
    if not os.path.exists(path+'/'+static+'/index.html'):
        if static != 'submit':
            page = '''
            	<div class="panel panel-default">
            		<div class="panel-heading"><b>'''+static+'''</b></div>
                        <div class="panel-body">
                            Please edit this page with your favorite edit tool! (vim, of course vim)
                        </div>
                    </div>
                </div>
            '''
        else:
            page = '''
            	<div class="panel panel-default">
            		<div class="panel-heading"><b>'''+static+'''</b></div>
                        <div class="panel-body">
                            Please edit this page with your favorite edit tool! (vim, of course vim)
                        </div>
                    </div>
                </div>
            '''

        pageHeaderP = pageHeader.replace('TITLE_HERE',static)
        pageLinksP = pageLinks.replace('PROJECTS_IS_ACTIVE','')
        if static=='about':
            pageLinksP = pageLinksP.replace('ABOUT_IS_ACTIVE','class="active"')
        else :
            pageLinksP = pageLinksP.replace('ABOUT_IS_ACTIVE','')
        if static=='submit':
            pageLinksP = pageLinksP.replace('SUBMIT_IS_ACTIVE','class="active"')
        else:
            pageLinksP = pageLinksP.replace('SUBMIT_IS_ACTIVE','')
        if static=='ideas':
            pageLinksP = pageLinksP.replace('IDEAS_IS_ACTIVE','class="active"')
        else:
            pageLinksP = pageLinksP.replace('IDEAS_IS_ACTIVE','')

        page = pageHeaderP + pageLinksP + page + pageFooter
        writeToFile(path+static+'/index.html',page)



projectsPage = {}
print 'Group Name : '+groupName
print '[+] Processing projects'

for i in projectsData[groupName]:
    projectUrl = projectsData[groupName][i]
    projectId = i
    print ' | '+str(projectId)+' : '+projectUrl
    projectData = processProjectJson(projectId, projectUrl)
    if projectData == None:
        if os.path.exists(projectsJsonDir+str(projectId)+'/project.json'):
            with open(projectsJsonDir+str(projectId)+'/project.json', 'r') as projectFile:
                dataf=projectFile.read().replace('\n', '')
                projectData = json.loads(dataf)
        else:
            print '[-] Failed to build page for project '+projectUrl
            continue
    print ' | Generating index page for project \''+projectData['projectName']+'\''
    projectPage = buildProjectPage(projectId,projectData)
    writeToFile(projectsJsonDir+str(projectId)+'/index.html',projectPage)
    projectsPage[projectId] = {'projectName' : projectData['projectName'], 'projectStatus' : projectData['projectStatus'], 'projectShortDescription' : projectData['projectShortDescription'], 'projectLogo' : projectData['projectLogo'],'projectTags' : projectData['projectTags']}


print '[+] Done'
print '[~] Generating projects index page'
projectsIndexHtml = buildProjectsPage(projectsPage)
writeToFile(projectsJsonDir+'/index.html',projectsIndexHtml)
for staticPage in ['about','ideas','submit']:
    buildStaticPage(projectsJsonDir,staticPage)

print '[+] Done'
