import yaml

with open('config.yml','r') as f:
	doc = yaml.load(f)

txt = doc["Welcome_message"]
print txt
