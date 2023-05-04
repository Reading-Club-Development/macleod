import logging
import sys, os


LOGGER = logging.getLogger(__name__)

import Macleod.Filemgt as Filemgt

import Macleod.scripts.parser as parser

import Macleod.Ontology as Ontology

#print(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../")


default_dir = Filemgt.read_config('system', 'path')
default_prefix = Filemgt.read_config('cl', 'prefix')


#Function to check the consistency of ontologies in the Common Logic Interchange Format (.clif).'
    #filepath: path to the file or folder of files to be checked.
    #method: string determining how to check
        #"simple" for a simple consistency check
        #"full" for a full resursive consistency check in case the entire ontology is not provably consistent
        #"module" to check each module individually
    #output: Bool. Do you want it to write to an output file
    #resolve: Bool. auto resolve imports?
    #stats: bool. Do you want detailed stats (including definitions) about the ontology?
    #nontrivial: bool. Instantiate all predicates to check for nontrivial consistency?
    #base: Path to directory containing ontology files (basepath; only relevant when option --resolve is turned on; can also be set in configuration file
    #sub: String to replace with basepath found in imports, only relevant when option --resolve is turned on
def main(filepath, method="simple", output=True, resolve=False, stats=True, nontrivial=False, base=None, sub=None):


    LOGGER.info('Called script check_consistency')
    # Setup the command line arguments to the program


    # Parse out the ontology object then print it nicely
    default_basepath = Filemgt.get_ontology_basepath()
    if sub is None:
        sub = default_basepath[0]
    if base is None:
        base = default_basepath[1]

    # TODO need to substitute base path
    full_path = filepath

    if os.path.isfile(full_path):
        logging.getLogger(__name__).info("Starting to parse " + full_path)
        # Creation of the ModuleSet is from the old deprecated approach
        #m = ClifModuleSet(full_path)
        derp, clif = consistent(full_path, method, sub, base, resolve, False, output, stats, nontrivial)

    elif os.path.isdir(full_path):
        logging.getLogger(__name__).info("Starting to parse all CLIF files in folder " + full_path)
        # TODO need function for checking consistency of a folder
        # convert_folder(full_path, args=args)
    else:
        logging.getLogger(__name__).error("Attempted to check consistency of non-existent file or directory: " + full_path)



def consistent(filename, method, sub, base, resolve, conds, output, stats, nontrivial):

    ontology = parser.convert_file(filename, "None", sub, base, resolve, conds, output=output)
    

    if resolve:
        ontology.resolve_imports()

    ontology.analyze_ontology()

    if stats:
        ontology.get_explicit_definitions()

    if nontrivial:
        ontology.add_nontrivial_axioms()

    if method == "simple":
        # Run the parsing script first to translate to TPTP and LADR
        # as part of the args, it is communicated whether to resolve the ontology or not

        (return_value, fastest_reasoner) = ontology.check_consistency()

        if return_value == Ontology.CONSISTENT:
            if nontrivial:
                print(fastest_reasoner.name + " proved nontrivial consistency of " + ontology.name)
            else:
                print(fastest_reasoner.name + " proved consistency of " + ontology.name)
            print("Results saved to " + fastest_reasoner.output_file)
        exit(0)
    elif method == "full":
        # TODO not yet working again
        # Run the parsing script first to translate to TPTP and LADR
        ontology = parser.convert_file(filename, "None", sub, base, resolve, conds, output=output)
        ontology.check_consistency()
        #results = m.run_full_consistency_check(abort=True, abort_signal=ClifModuleSet.CONSISTENT)
        exit(-1)
    elif method == "module":
        # TODO not yet working again
        #results = m.run_consistency_check_by_subset(abort=True, abort_signal=ClifModuleSet.CONSISTENT)
        exit(-1)




#Below is apparently what module was supposed to do
    # the following code block is about preseting the results from multiple modules
    # if len(results)==0:
    #     logging.getLogger(__name__).info("+++ CONSISTENCY CHECK TERMINATED: NO MODULES FOUND IN " +str(m.get_imports()) +"\n")
    # else:
    #     for (r, value, _) in results:
    #         if value==-1:
    #             logging.getLogger(__name__).info("+++ CONSISTENCY CHECK TERMINATED: INCONSISTENCY FOUND IN " +str(r) +"\n")
    #             return (False, m)
    #     result_sets = [r[0] for r in results]
    #     result_sets.sort(key=lambda x: len(x))
    #     #print result_sets[0]
    #     #print results
    #     #print "+++++" + str(value)
    #     if results[0][1]==1:
    #         logging.getLogger(__name__).info("+++ CONSISTENCY CHECK TERMINATED: PROVED CONSISTENCY OF " +str(result_sets[0]) +"\n")
    #         return (True, m)
    #     else:
    #         logging.getLogger(__name__).info("+++ CONSISTENCY CHECK TERMINATED: NO RESULT FOR CONSISTENCY OF " +str(result_sets[0]) +"\n")
    #         if len(result_sets)>1:
    #             for (r, value, _) in results:
    #                 if value==1:
    #                     logging.getLogger(__name__).info("+++ CONSISTENCY CHECK TERMINATED: PROVED CONSISTENCY OF SUBONTOLOGY " +str(r[0]) +"\n")
    # return (None, m)

