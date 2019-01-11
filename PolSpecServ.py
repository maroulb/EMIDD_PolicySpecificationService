"""
Policy Specification Service.

is used to specify privacy preferences or generalized usage policies to external datasets
"""
from flask import Flask, request, Response, jsonify, render_template, current_app, url_for, redirect
import requests
import json
import os
import yappl

app = Flask(__name__)

PolProvServURL = os.environ['pol_prov_url']

def getRoot(graph):
    keys = graph.keys()
    values = []
    grValues = graph.values()
    for grValue in grValues:
        for i in range(len(grValue)):
            values.append(grValue[i])
    for key in keys:
        if key in values:
            pass
        else:
            root = key
    return root


def getDefinition(item):
    if item in purposeDefinitions:
        return purposeDefinitions[item]
    if item in utilizerDefinitions:
        return utilizerDefinitions[item]
    return item


def getValDic(graph, node):
    valDic = []
    for value in graph[node]:
        levDic = {}
        levDic['text'] = value
        levDic['def'] = getDefinition(value)
        if len(graph[value]) > 0:
            levDic['nodes'] = getValDic(graph, value)
        valDic.append(levDic)
    return valDic


def graph2tree(graph):
    tree = []
    rootDic = {}
    root = getRoot(graph)
    rootDic['text'] = root
    rootDic['def'] = getDefinition(root)
    rootDic['nodes'] = getValDic(graph, root)
    tree.append(rootDic)
    return tree


def getPolicyName(id):
    name = policyMappings[str(id)]
    return name


def getPolicyId(name):
    for id, sensorname in policyMappings.iteritems():
        if sensorname == name:
            return id


@app.route('/playground', methods=['GET', 'POST'])
def playground():
    if request.method == 'POST':
        utilizer = request.form['newPermUti']
        purpose = request.form['newPermPur']
        consent = request.form.get('policy')
        return render_template('playground.html', utilizer=utilizer, purpose=purpose, consent=consent)
    return render_template('playground.html')


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        if request.form['firstChoice'] == 'Create New':
            return redirect(url_for('createNew'))
        elif request.form['firstChoice'] == 'Show Existing':
            return redirect(url_for('getMyPolicies'))
        else:
            pass
    return render_template('start.html')


@app.route('/policies/', methods=['GET', 'POST'])
def getMyPolicies():
    """GET and show all usage preferences."""
    myPolicies = open('config/myPolicies.txt', 'r')
    myPolicies = myPolicies.readlines()
    IDs = []
    for line in iter(myPolicies):
        IDs.append(str(line))
    names = []
    for ID in IDs:
        names.append(getPolicyName(int(ID)))
    if request.method == 'POST':
        id = request.form['id']
        return redirect(url_for('showDetails', id=getPolicyId(id)))
    return render_template('policies.html', IDs=names)


@app.route('/policies/<id>', methods=['GET', 'POST'])
def showDetails(id):
    myPolicies = open('config/myPolicies.txt', 'r')
    myPolicies = myPolicies.readlines()
    IDs = []
    for line in iter(myPolicies):
        IDs.append(str(line))
    names = []
    for ID in IDs:
        names.append(getPolicyName(int(ID)))
    if request.method == 'POST':
        id = request.form['id']
        return redirect(url_for('showDetails', id=id))
    r = requests.get(PolProvServURL + str(id))
    policy = json.loads(r.text)
    policy = yappl.parse(json.dumps(policy))
    ID = policy.getId()
    rules = policy.getPreference()
    return render_template('policies_details.html', ID=getPolicyName(ID), rules=rules, IDs=names)


@app.route('/policies/new', methods=['GET', 'POST'])
def createNew():
    myPolicies = open('config/myPolicies.txt', 'r')
    myPolicies = myPolicies.readlines()
    IDs = []
    for line in iter(myPolicies):
        IDs.append(str(line))
    ruleID = 'new'
    names = []
    for ID in IDs:
        names.append(getPolicyName(int(ID)))
    if request.method == 'POST':
        polID = request.form['newRule']
        return render_template('create_de.html', purTree=purposeTree, utiTree=utilizerTree, polID=polID, ruleID=ruleID, traTree=transformationTree)
    return render_template('sensors.html', IDs=names)


@app.route('/policies/create', methods=['GET', 'POST'])
def createNewRule():
    if request.method == 'POST':
        polID = request.form['newRule']
        return render_template('create_de.html', purTree=purposeTree, utiTree=utilizerTree, polID=polID, traTree=transformationTree)
    return render_template('create-de.html', purTree=purposeTree, utiTree=utilizerTree, traTree=transformationTree)


@app.route('/policies/verify', methods=['GET', 'POST'])
def verifyNewRule():
    if request.method == 'POST':
        rule = request.form.get('createdRule')
        rule = json.loads(rule)
        rules = []
        rules.append(rule)
        ID, ruleId = (request.form['newRuleButton']).split(',')
        return render_template('verify.html', ID=ID, ruleId=ruleId, rules=rules)
    return 'oooops'


@app.route('/policies/verified', methods=['GET', 'POST'])
def verifiedRule():
    if request.method == 'POST':
        ID, ruleId = request.form['confirmButton'].split(',')
        rule = request.form.get('createdRule')
        rule = json.loads(rule)

        permittedPurpose = rule['purpose']['permitted']
        excludedPurpose = rule['purpose']['excluded']
        permittedUtilizer = rule['utilizer']['permitted']
        excludedUtilizer = rule['utilizer']['excluded']

        transformation = []
        transRule = {}
        transRule['attribute'] = str(ID)
        transRule['tr_func'] = rule['transformation']

#        return 'ID: ' + str(getPolicyId(ID)) + ' PermPur: ' + str(transRule)
        return redirect(url_for('showDetails', id=getPolicyId(ID)))
    return 'oooops'


@app.route('/policies/update', methods=['POST'])
def updateRule():
    if request.method == 'POST':
        polID, ruleID = (request.form['updateButton']).split(',')
        return render_template('update.html', purTree=purposeTree, utiTree=utilizerTree, polID=polID, ruleID=ruleID, traTree=transformationTree)
    return render_template('update.html', purTree=purposeTree, utiTree=utilizerTree, traTree=transformationTree)


if __name__ == '__main__':
    #  TODO: catch errors regarding missing config files etc.
    purposeDefinitions = open('config/purposeDefinitions.json', 'r')
    purposeDefinitions = purposeDefinitions.read()
    purposeDefinitions = json.loads(purposeDefinitions)
    utilizerDefinitions = open('config/utilizerDefinitions.json', 'r')
    utilizerDefinitions = utilizerDefinitions.read()
    utilizerDefinitions = json.loads(utilizerDefinitions)
    purposeGraph = open('config/purposeGraph.json', 'r')
    purposeGraph = purposeGraph.read()
    purposeGraph = json.loads(purposeGraph)
    purposeTree = graph2tree(purposeGraph)
    utilizerGraph = open('config/utilizerGraph.json', 'r')
    utilizerGraph = utilizerGraph.read()
    utilizerGraph = json.loads(utilizerGraph)
    utilizerTree = graph2tree(utilizerGraph)
    transformationGraph = open('config/transformationGraph.json', 'r')
    transformationGraph = transformationGraph.read()
    transformationGraph = json.loads(transformationGraph)
    transformationTree = graph2tree(transformationGraph)
    policyMappings = open('config/policyMappings.json', 'r')
    policyMappings = policyMappings.read()
    policyMappings = json.loads(policyMappings)
    app.run()