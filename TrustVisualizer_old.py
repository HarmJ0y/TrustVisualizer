#!/usr/bin/python

##############################################################################
# Author: @harmj0y
#
# Based on: https://github.com/sixdub/DomainTrustExplorer by @sixdub
#
# Description: Usesnetworkx library to transform PowerView's updated 
#              Get-DomainTrustMapping functionality output to graphml
#
# License: BSD 3-clause
##############################################################################

import networkx as nx
import sys, csv

if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print "usage: ./TrustVisualizer.py <trust_file.csv>"
        exit()

    graph = nx.DiGraph()
    intputFile = sys.argv[1]

    with open(intputFile, 'rb') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')

        for row in reader:

            # if we have the header row, skip
            if row[0] == 'SourceName':
                continue

            # csv format:
            #   SourceName,TargetName,TrustType,TrustAttributes,TrustDirection,WhenCreated,WhenChanged
            ecolor = ''
            sourceName = row[0].strip()
            targetName = row[1].strip()
            trustType = row[2].strip()
            trustAttributes = row[3].strip()
            trustDirection = row[4].strip()

            # if the source and destination domains are the same, skip
            if (sourceName == targetName):
                continue

            if (trustType == 'MIT'):
                # black label for MIT trusts
                ecolor ='#000000'

            else:
                if "WITHIN_FOREST" in trustAttributes:
                    # green label for intra-forest trusts
                    ecolor = '#009900'
                elif (trustAttributes == "FOREST_TRANSITIVE"):
                    # blue label for inter-forest trusts
                    ecolor = '#0000CC'
                elif ((trustAttributes == "") or (trustAttributes == "TREAT_AS_EXTERNAL") or (trustAttributes == "FILTER_SIDS")):
                    # red label for external trusts
                    ecolor = '#FF0000'
                else:
                    # violet label for unknown
                    print "[-] Unrecognized trust attributes between %s and %s : %s" % (sourceName, targetName, trustAttributes)
                    ecolor = '#EE82EE'

            # add the domain nodes to the internal graph
            graph.add_node(sourceName, label=sourceName)
            graph.add_node(targetName, label=targetName)

            # add the edges to the graph
            if "Bidirectional" in trustDirection:
                graph.add_edge(sourceName, targetName, color=ecolor)
                graph.add_edge(targetName, sourceName, color=ecolor)
            elif "Outbound" in trustDirection:
                graph.add_edge(targetName, sourceName, color=ecolor)
            elif "Inbound" in trustDirection:
                graph.add_edge(sourceName, targetName, color=ecolor)
            else:
                print "[-] Unrecognized relationship direction between %s and %s : %s" % (sourceName, targetName, trustDirection)

        outputFile = intputFile + ".graphml"
        nx.write_graphml(graph, outputFile)
        print "\n[+] Graphml writte to '%s'" % (outputFile)
        print "\n[*] Note: green = within forest, red = external, blue = forest to forest, black = MIT, violet = unrecognized\n"