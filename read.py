f = open('/working/static/conf/agent_list.txt', 'r', encoding='UTF-8')

data = f.read()
agent_list = data.split("\n")
print(agent_list)

agent_dict = [
    {"value": en, "label": jp}
    for item in agent_list
    for jp,en in [item.split(",", 1)]
]
print(agent_dict)
f.close()