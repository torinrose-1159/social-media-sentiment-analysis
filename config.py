from configparser import ConfigParser

def config(section, filename):
    # Create a parser
    parser = ConfigParser()
    # Read the config file
    parser.read(filename)
    secrets = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            secrets[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file".format(section, filename))
    return secrets