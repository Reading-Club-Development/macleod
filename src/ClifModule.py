'''
Created on 2012-03-07
Refactored on 2013-03-16

@author: Torsten Hahmann
'''
import os, filemgt, process, clif, commands

class ClifModule(object):

    module_name = ''
    
    depth = 0
    
    """set of all imported module names """
    imports = set([])
    
    """ set of all parent module names"""
    parents = set([])
    
    clif_file_name = ''
    
    """Location of the clif input file that has undergone preprocessing"""
    clif_processed_file_name = ''
    
    p9_file_name = None
    
    # the distinction between nonlogical_symbols and nonlogical_variables assumes that a single symbol is not used as both in different sentences
    nonlogical_symbols = set([])
    nonlogical_variables = set([])
        
    '''
    classdocs
    '''
    def __init__(self,name,depth):
        '''
        Constructor
        '''
        self.module_name = self.get_simple_module_name(module = name)
        print '+++\nprocessing module: ' + self.module_name
        # remove any obsolete URL prefix as specified in the configuration file
        if self.module_name.endswith(filemgt.read_config('cl','ending')):
            self.module_name = os.path.normpath(self.module_name.replace(filemgt.read_config('cl','ending'),''))
        
        # stores the depth of the import hierarchy
        self.depth = depth
        
        # add the standard ending for CLIF files to the module name
        self.clif_file_name = filemgt.get_full_path(self.module_name, ending=filemgt.read_config('cl','ending'))

        self.clif_processed_file_name = filemgt.get_full_path(self.module_name, 
                                                              folder= filemgt.read_config('converters','tempfolder'), 
                                                              ending = filemgt.read_config('cl','ending'))

        print self.clif_file_name
        print self.clif_processed_file_name
        
        
        clif.remove_all_comments(self.clif_file_name,self.clif_processed_file_name)
        
        self.imports =  [self.get_simple_module_name(i) for i in clif.get_imports(self.clif_processed_file_name)]
        
        print self.imports
        
        self.compute_nonlogical_symbols(self.clif_processed_file_name)

        self.parents = set([])
        
        # push nonlogical symbols and variables upwards (VERY LAST STEP)
#        if isinstance(parent, ClifModule):
#            parent.nonlogical_symbols.append[self.nonlogical_symbols]
#            parent.nonlogical_variables.append[self.nonlogical_variables]

    def get_simple_module_name (self,module=None):
        if not module:
            module= self.module_name
        import re
        prefix = re.compile(re.escape(filemgt.read_config('cl','prefix')), re.IGNORECASE)
        prefix.sub('', module)
        return os.path.normpath(module)
    
    def get_full_module_name (self,module=None):
        if not module: 
            module= self.module_name
        import re
        prefix = re.compile(re.escape(filemgt.read_config('cl','prefix')), re.IGNORECASE)
        prefix.sub('', module)
        return os.path.normpath(module)
                
    def add_parent (self,name,depth):
        #print "adding parent: " + str(name) + ' (' + str(depth) + ')' + ' to ' + self.module_name
        self.parents.add(self.get_full_module_name(name))
        # update the depth
        if depth>=self.depth:
            self.depth=depth+1
            #print "new depth = " + str(self.depth)
        
    def get_parents (self):
        return self.parents
            
    def get_imports (self):
        """returns the set of immediate imports."""
        return self.imports
        
    def get_nonlogical_symbols (self):
        return self.nonlogical_symbols
    
    def get_depth (self):
        return self.depth
                
    def __repr__ (self):
        return (self.module_name 
                + ' (depth=' + str(self.depth) 
                + ', parents: ' + str(self.parents) + ')')  



    # extract all nonlogical symbols (predicate and function symbols) from the preprocessed clif file
    def compute_nonlogical_symbols (self,input_file_name):
        

        cl_file = open(input_file_name, 'r')
        line = cl_file.readline()
        while line:
            self.nonlogical_symbols |= clif.get_logical_symbols_from_single_line(line)
            self.nonlogical_variables |= clif.get_quantified_variables_from_single_line(line)
            line = cl_file.readline()

        cl_file.close()
        
        self.nonlogical_symbols -= self.nonlogical_variables
        print "Nonlogical symbols: " + str(self.nonlogical_symbols)
        print "Variables: " + str(self.nonlogical_variables)
        

    @staticmethod
    def compare(x, y):
        """ Compares two ClifModules to sort them first by depth (increasing) and then by name."""
        if x.get_depth() > y.get_depth():
           return 1
        elif x.get_depth() == y.get_depth():
           if x.get_simple_module_name() > y.get_simple_module_name(): return 1
           else: return -1
        else:  #x < y
           return -1

    def get_p9_file_name (self):
        """get the filename of the LADR translation of the module and translate the ClifModule if not yet done so."""
        if not self.p9_file_name:   # do the translation
            self.p9_file_name =  filemgt.get_full_path(self.module_name, 
                                                       folder=filemgt.read_config('ladr','folder'), 
                                                       ending=filemgt.read_config('ladr','ending'))
            cmd = commands.get_clif_to_ladr_cmd(self)
            process.executeSubprocess(cmd)
            print "CREATED LADR TRANSLATION: " + self.p9_file_name
             
        return self.p9_file_name
    
        
if __name__ == '__main__':
    import sys
    # global variables
    options = sys.argv
    m = ClifModule(options[1],0)
    print m.convert_to_ladr()