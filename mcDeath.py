#! /usr/bin/python

import os, pexpect

#Open and read the HeroicDeath data log
deathFile = open('/home/sa/bukkit/plugins/HeroicDeath/death_data.log', 'r')
deathFileLines = deathFile.readlines()
deathFileLines = deathFileLines[4:]

#Function to find the most common element in any given list
def mostCommon(llist):
  countDict = {}
  for element in llist:
    if element in countDict:
      countDict[element] = countDict[element] + 1
    else:
      countDict[element] = 1
  countElementTupleList = []
  for element in countDict.keys():
    countElementTupleList.append((countDict[element], element))
  countElementTupleList.sort()
  return countElementTupleList[-1]

#Find online players
#import pwd, os
#uid = pwd.getpwnam('sa')[2]
#os.setuid(uid)

#s=MCServer.Server()
#onlinePlayers = s.players()


#Compile the dictionary storing everyones deaths
deathDict = {}
for line in deathFileLines:
  splitList = line.split('|')
  name = splitList[0]
  position = splitList[4][6:]
  time = splitList[5]
  if splitList[3] == 'ENTITY_ATTACK':
    cause = splitList[1]
  else:
    cause = splitList[3]
  if name in deathDict:
    deathDict[name].append((cause, position, time))
  else:
    deathDict[name] = [(cause, position, time)]
    
#Sort the list according to who died the most
finalList = sorted([(len(deathDict[i]), i, mostCommon(deathDict[i][0])[1]) for i in deathDict.keys()], reverse=1)

#Write out ugly HTML
htmlDoc = open('/opt/lampp/htdocs/index.html', 'w')
htmlDoc.write('<h1>Death Leaderboard (Deaths since ' + deathFileLines[0].split('|')[5][:10] + ')</h1><em>Updated every 2 minutes</em><br><br>')
htmlDoc.write('<table cellpadding="5px"><tr><td><b>Name</b></td><td><b>Number Of Deaths</b></td><td><b>Latest Death</b></td><td><b>Most Common Death</b></td><td><b>List of all Deaths</b></td></tr>')
for i in finalList:
  htmlDoc.write('<tr><td>' + i[1] + '</td><td>' + str(i[0]) + '</td><td>' + str(deathDict[i[1]][-1][0]) + '</td><td>' + i[2] + '</td><td><a href="alldeaths/'+i[1]+'.html">All Deaths</a></td></tr>')
  allDeathsFile = open('/opt/lampp/htdocs/alldeaths/'+i[1]+'.html', 'w')
  ii=0
  allDeathsFile.write('<b>All Deaths for ' + i[1] + '</b><br>')
  for deathType in deathDict[i[1]]:
   ii=ii+1
   allDeathsFile.write(str(ii) +'. '+ deathType[0] + ' at coordinates: ' + deathType[1] + ' on ' + deathType[2] + '<br>')
  allDeathsFile.close()
htmlDoc.write('</table>')
htmlDoc.write('<br><h2><a href="http://jj.ax.lt:8123">|Game Map|</a></h2>')
htmlDoc.write('<br><h2>Players online in the last 2 minutes: ' + 'onlinePlayers' + '</h2>')
htmlDoc.close()
