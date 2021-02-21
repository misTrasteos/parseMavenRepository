import os
from jinja2 import Environment, FileSystemLoader
import yaml
import shutil

with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

if config['output']['delete']:
    try:
        shutil.rmtree( config['output']['path'] )
    except FileNotFoundError:
        pass

def generate_settings_xml(id, username, password):
    template = env.get_template('settings.xml.j2')
    output = template.render(id= id, username= username, password= password)

    try:
        os.makedirs(config['output']['path'])
    except FileExistsError:
        pass

    with open(config['output']['path'] + os.sep + 'settings.xml', 'wt') as f:
        f.write(output)

def generate_root_pom_xml(modules):
    template = env.get_template('root.pom.xml.j2')
    output = template.render(modules=modules)

    try:
        os.makedirs(config['output']['path'])
    except FileExistsError:
        pass

    with open(config['output']['path'] + os.sep + 'pom.xml', 'wt') as f:
        f.write(output)
        
def generate_module_pom_xml(file, pom_file, repository_id, url, module_name):
    template = env.get_template('module.pom.xml.j2')
    output = template.render(file=file, pomFile=pom_file, repositoryId=repository_id, url=url)

    os.makedirs(config['output']['path'] + os.sep + module_name )

    with open(config['output']['path'] + os.sep + module_name + os.sep + 'pom.xml', 'wt') as f:
        f.write(output)

get_file_by_extension = lambda extension : [filename for filename in jarAndPom if filename.endswith(extension)][0]
get_jar_file = lambda: get_file_by_extension('jar')
get_pom_file = lambda: get_file_by_extension('pom')

get_jar_file_path = lambda: dirpath + os.sep + get_jar_file()
get_pom_file_path = lambda: dirpath + os.sep + get_pom_file()

# jinja2 stuff
fileLoader = FileSystemLoader('templates')
env = Environment(loader=fileLoader)

modules = []

# dirpath is a string, the path to the directory
# dirnames is a list of the names of the subdirectories in dirpath
# filenames is a list of the names of the non-directory files in dirpath.
for dirpath, dirnames, filenames in os.walk( config['sourceRepository'] ):    
    if len(dirnames) == 0: # only leaf directories
        jarAndPom = [filename for filename in filenames if filename.endswith('.jar') or filename.endswith('.pom')]

        # only directories with exactly one jar and one pom. Both of them with the same name
        if len(jarAndPom) == 2 and jarAndPom[0][:-4] == jarAndPom[1][:-4]: 
            moduleName = str(len(modules)).zfill(10)

            module = dict()

            module['name'] = moduleName
            module['sourcePath'] = dirpath
            module['jarFile'] = get_jar_file()
            module['pomFile'] = get_pom_file()
            module['artifactId'] = jarAndPom[0][:-4]
            
            modules.append(module)

            generate_module_pom_xml(file= get_jar_file_path(), pom_file= get_pom_file_path(), repository_id= config['distributionManagement']['id'], url= config['distributionManagement']['url'], module_name= moduleName)

generate_root_pom_xml(modules)
generate_settings_xml(id= config['distributionManagement']['id'], username= config['distributionManagement']['username'], password= config['distributionManagement']['password'])