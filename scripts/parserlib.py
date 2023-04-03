import logging
import sys, os


LOGGER = logging.getLogger(__name__)

import macleod.parsing.parser as Parser
import macleod.Filemgt

default_dir = macleod.Filemgt.read_config('system', 'path')
default_prefix = macleod.Filemgt.read_config('cl', 'prefix')


#This here is one simple function that will fulfill all your parsing and converting needs!
#Returns nothing
#Filepath: A string to the filepath of the file or folder to be converted
#format: The format to be converted into. If set to "None" it'll just print the clif file.
#enum: Do you want it to enumerate axioms? Only relevant for LaTeX output.
#output: Boolean. Do you want it to write an output file (True) or just print (False)
#resolve: do you want it to resolve imports
#nocond: do u want it to keep conditionals (True) or switch to disjunctions (False)
#base: path to directory with ontology files. Only relevant if resolve is on
#sub: path to directory with import files. Only relevant if resolve is on

def parse_clif(filepath, format=None, OWL_version="Full", enum=False, output=False, resolve=False, nocond=False, base=None, sub=None, ffpcnf=False, clip=False):
 # Parse out the ontology object then print it nicely
    default_basepath = macleod.Filemgt.get_ontology_basepath()
    if sub is None:
        sub = default_basepath[0]
    if base is None:
        base = default_basepath[1]

    # setting global variable to preserve (or not) conditionals connectives
    print("ELIMINATING CONDITIONALS " + str(nocond))
    global conditionals
    conditionals = not(nocond)

    # TODO need to substitute base path
    full_path = filepath

    if os.path.isfile(full_path):
        logging.getLogger(__name__).info("Starting to parse " + filepath)
        convert_file(full_path, format, sub, base, resolve)

    elif os.path.isdir(full_path):
        tempfolder = macleod.Filemgt.read_config('converters', 'tempfolder')
        ignores = [tempfolder]
        cl_ending = macleod.Filemgt.read_config('cl', 'ending')
        #logging.getLogger(__name__).info("Traversing folder " + folder)

        for directory, subdirs, files in os.walk(full_path):
            if any(ignore in directory for ignore in ignores):
                pass
            else:
                for single_file in files:
                    if single_file.endswith(cl_ending):
                        file = os.path.join(directory, single_file)
                        logging.getLogger(__name__).info("Parsing CLIF file " + file)
                        convert_file(file, format, sub, base, resolve, nocond, output=output, enum=enum)

    else:
        logging.getLogger(__name__).error("Attempted to parse non-existent file or directory: " + full_path)


def convert_file(file, format, sub, base, resolve, preserve_conditionals = None, output=False, enum=None):

    global conditionals

    # need to check whether to set or reset the global variable
    if preserve_conditionals is not None:
        conditionals = preserve_conditionals

    ontology = Parser.parse_file(file, sub, base, resolve, preserve_conditionals = conditionals)

    if ontology is None:
        # some error occurred while parsing CLIF file(s)
        exit(-1)

    if format is None:
        print(ontology)
    elif format.lower() == "ffpcnf":
        print(ontology.to_ffpcnf())
        return ontology
    
    elif format.lower() == "tptp":
        print(ontology.to_tptp())
        if output:
            filename = ontology.write_tptp_file()
            logging.getLogger(__name__).info("Produced TPTP file " + filename)
            return filename

    elif format.lower() == "owl":
        # argument full has been used to store the OWL Profile
        onto = ontology.to_owl(owlType(type))

        print("\n-- Translation --\n")
        print(onto.tostring())

        if output:
            # producing OWL file
            filename = ontology.write_owl_file()
            logging.getLogger(__name__).info("Produced OWL file " + filename)

    elif format.lower() == "ladr":
        print(ontology.to_ladr())

        if output:
            filename = ontology.write_ladr_file()
            logging.getLogger(__name__).info("Produced LADR file " + filename)
            return filename

    elif format.lower() == "latex":
        if output:
            filename = ontology.write_latex_file(enum)
            logging.getLogger(__name__).info("Produced LaTeX file " + filename)
            return filename
        else:
            print(ontology.to_latex())
    

    else:
        print(ontology)


#takes a string describing the OWL version and returns the proper Owl.Profile object
#if type is None, will return OWL2_FULL
def owlType(type):
    from macleod.dl.owl import Owl
    # argument full is used to store the OWL Profile
    if type == "dl":
        return Owl.Profile.OWL2_DL
    elif type == "el":
        return Owl.Profile.OWL2_EL
    elif type == "ql":
        return Owl.Profile.OWL2_QL
    elif type == "rl":
        return Owl.Profile.OWL2_RL
    else:
        return Owl.Profile.OWL2_FULL
