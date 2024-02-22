############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
##
############################################################

import time

class Variable: 

    """
    Class for defining a variable.

    When creating a variable, you must provide a string for the name
    and optionally a list of values in its domain. 

    The variable has 
    - a name as a string.
    - a permanent domain.

        The permanent domain has a list of all the values.

        If this list is not provided when creating the variable, 
        the variable starts with an empty domain.

        After creating the variable, it is possible to add values to the 
        permanent domain, but it is NOT possible to remove values from the 
        permanent domain.

    - a current domain.

        The current domain ontains of a list of Boolean flags, one for each 
        value in the permanent domain. We use these flags to keep track of 
        which values have been pruned from the current domain.

        Setting a flag to False prunes a value. Setting a flag to True puts 
        the value back into the current domain. You can also get a list of 
        values in the current domain or the size of the current domain.

    - an assigned value.

        This is the assigned value of the variable. 
        When creating the variable, the assigned value is set to be None.
    
        Assigning the variable sets it to the provided value. Unassigning the 
        variable sets this back to None. The assigned value must be in the 
        variable's current domain. If you want to assign a variable to a 
        different value, you must unassign the variable first. 
        
        When a variable is assigned, from the outside, the variable's domain 
        has the assigned value only. Internally, the variable's current domain 
        is not changed. Therefore, pruning and unpruning can work independently 
        of assignment and unassignment. 
    """

    def __init__(self, name, domain=[]):
        '''
            Create a variable object, specifying its name (a string). 
            Optionally specify its permanent domain.
        '''

        # a string for the variable's name
        self.name = name                       

        # the permanent domain is a copy of the provided domain.
        self.dom = list(domain)                 

        # the current domain is a list of boolean flags, 
        # one for each value in the permanent domain.
        self.curdom = [True] * len(domain)      

        # the assignedValue of the variable.
        # initially None (unassigned)
        self.assignedValue = None


    def add_domain_values(self, values):
        '''
            Add additional domain values to the domain
            Removals not supported removals
        '''
        for val in values: 
            self.dom.append(val)
            self.curdom.append(True)

    def domain_size(self):
        '''
            Return the size of the permanent domain
        '''
        return(len(self.dom))


    def domain(self):
        '''
            Return the permanent domain as a list
        '''
        return(list(self.dom))


    ####################################################################
    # methods for pruning and unpruning values in the current domain
    ####################################################################

    def prune_value(self, value):
        '''
            Remove value from the CURRENT domain
            Set the flag for the value to be False.
            This does not change the permanent domain.
        '''

        self.curdom[self.value_index(value)] = False

    def unprune_value(self, value):
        '''
            Restore value to the CURRENT domain
            Set the flag for the value to be True.
            This does not change the permanent domain.
        '''

        self.curdom[self.value_index(value)] = True

    def cur_domain(self):
        '''
            if the variable is assigned, 
            return a list containing the assigned value only.

            otherwise, if the variable is not assigned, 
            return the list of values in the current domain.
        '''

        vals = []
        if self.is_assigned():
            vals.append(self.get_assigned_value())
        else:
            for i, val in enumerate(self.dom):
                if self.curdom[i]:
                    vals.append(val)
        return vals

    def in_cur_domain(self, value):
        '''
            if the variable is assigned, 
            return True if and only if the provided value 
            is the same as the assigned value.

            otherwise if the variable is not assigned,
            return True if the provided value is in the current domain.
        '''

        if not value in self.dom:

            # if the provided value is not in the permanent domain
            # return False
            return False

        if self.is_assigned():

            # if the variable is assigned
            # return if the provided value is the same as the assigned value.
            return value == self.get_assigned_value()

        else:

            # return if the provided value is in the current domain
            return self.curdom[self.value_index(value)]

    def cur_domain_size(self):
        '''
            Return the size of the current domain.
        '''

        if self.is_assigned():
            return 1
        else:
            return(sum(1 for v in self.curdom if v))

    def restore_curdom(self):
        '''
            Reset the current domain to be the same as the permanent domain.
        '''

        for i in range(len(self.curdom)):
            self.curdom[i] = True

    ####################################################################
    # methods for assigning and unassigning the variable
    ####################################################################

    def is_assigned(self):
        '''
            Return true if the variable is assigned
            and return false otherwise.
        '''

        return self.assignedValue != None
    
    def assign(self, value):
        '''
            Set the assignedValue to be the provided value.
            This function does not modify the permanent or current domains.
        '''

        if self.is_assigned():
            print("ERROR: trying to assign variable", self, 
                  "that is already assigned")
            return

        if not self.in_cur_domain(value):
            print("ERROR: trying to assign variable", self, 
                  "but the provided value is not in the variable's domain")
            return

        self.assignedValue = value

    def unassign(self):
        '''
            Set assignedValue to None.
            Prints an error if the variable is not assigned. 
            Used by bt_search. 
        '''

        if not self.is_assigned():
            print("ERROR: trying to unassign variable", self, " not yet assigned")
            return
        self.assignedValue = None

    def get_assigned_value(self):
        '''
            Return assignedValue
            Return None if the variable is not assigned
        '''

        return self.assignedValue

    ####################################################################
    #internal methods
    ####################################################################

    def value_index(self, value):
        '''
            Domain values need not be numbers, so return the index
            in the domain list of a variable value
        '''
        return self.dom.index(value)

    def __repr__(self):
        return("Var-{}".format(self.name))

    def __str__(self):
        return("Var--{}".format(self.name))

    def print_all(self):
        '''
            Also print the variable domain and current domain
        '''
        print("Var--\"{}\": Dom = {}, CurDom = {}\n".format(
            self.name, self.dom, self.curdom))



class Constraint: 

    '''
        Class for defining a constraint.

        When creating a constraint, you must provide a name and 
        a scope, which is an ORDERED list of variables. 
        After creating a constraint, you won't be able to change
        the ordered list of variables.

        After creating a constraint, you can add a list of satisfying tuples。
        The order of variables in each tuple must be the same as
        the order of variables you used to create the constraint.
    '''

    def __init__(self, name, scope): 
        '''
            Consraints are implemented as storing a set of satisfying
            tuples (i.e., each tuple specifies a value for each variable
            in the scope such that this sequence of values satisfies the
            constraints).

            NOTE: This is a very space expensive representation...
            a proper constraint object would allow for representing 
            the constraint with a function.  
        '''

        # a string for the constraint's name
        self.name = name        

        # an ordered list of variables
        # the order of the variables in the scope is critical 
        # to the functioning of the constraint
        self.scope = list(scope)

        # keeps track of all the satisfying tuples for this constraint
        # each key is a list of values for all the variables
        # each value is True
        self.sat_tuples = dict()

        # Get a list of satisfying tuples that contain a particular variable/value pair.
        # The dictionary below helps support GAC propgation. 
        self.sup_tuples = dict()


    def add_satisfying_tuples(self, tuples):
        '''
            Add a list of satisfying tuples to the constraint.
            
            The order of variables in each tuple must be the same as
            the order of variables you used to create the constraint.

            It is not possible to delete a satisfying tuple from a constraint.
        '''
        for x in tuples:

            t = tuple(x)  #create an immutable tuple

            # add the tuple to the dictionary of satisfying tuples
            if not t in self.sat_tuples:
                self.sat_tuples[t] = True

            # put t in as a support for all of the variable values in it
            for i, val in enumerate(t):
                var = self.scope[i]
                if not (var,val) in self.sup_tuples:
                    self.sup_tuples[(var,val)] = []
                self.sup_tuples[(var,val)].append(t)


    def get_scope(self):
        '''
            Return the ordered list of variables
        '''
        return list(self.scope)


    def check(self, vals):
        '''
            Return True if the provided list of values satisfy the constraint
            and return False otherwise.

            Note the list of values are must be ordered in the same order 
            as the list of variables in the constraints scope
        '''
        return tuple(vals) in self.sat_tuples


    def get_num_unassigned_vars(self):
        '''
            Return the number of unassigned variables in the constraint's scope
        '''
        n = 0
        for v in self.scope:
            if not v.is_assigned():
                n = n + 1
        return n


    def get_unassigned_vars(self): 
        '''
            Return a list of unassigned variables in constraint's scope. 
            Note more expensive to get the list than to then number
        '''
        vs = []
        for v in self.scope:
            if not v.is_assigned():
                vs.append(v)
        return vs

    def __str__(self):
        return("{}({})".format(self.name,[var.name for var in self.scope]))




class CSP:
    '''
        Class for defining a constraint satisfaction problem.

        Class for packing up a set of variables into a CSP problem.
        Contains various utility routines for accessing the problem.
        The variables of the CSP can be added later or on initialization.
        The constraints must be added later
    '''

    def __init__(self, name, vars=[]):
        '''
            Create a CSP object with a name as a string
            and optionally a list of variables
        '''

        self.name = name

        # a list to store variables
        self.vars = []         

        # a list to store constraints
        self.cons = []

        # a dictionary that allows us to look up the constraints for a variable
        self.vars_to_cons = dict()

        # add each variable to the list
        # also add each variable as a key in the vars_to_cons dictionary.
        for v in vars:
            self.add_var(v)
        

    def add_var(self, v):
        '''
            Add a variable to this CSP. 

            Given a variable,
            add it to the list of variables (vars) and
            add it as a key in the vars_to_cons dictionary.

            Print an error if v is not a Variable object
            or v is already in the CSP.
        '''
        if not type(v) is Variable:
            print("ERROR: Trying to add non variable ", v, " to CSP object")
        elif v in self.vars: 
            print("ERROR: Trying to add variable ", v, " to CSP object that already has it")
        elif v in self.vars_to_cons:
            print("ERROR: Trying to add variable ", v, " to CSP object that already has it")
        else:
            self.vars.append(v)
            self.vars_to_cons[v] = []


    def add_constraint(self, c):
        '''
            Add a constraint to this CSP. 

            Print an error if c is not a Constraint object 
            or if a variable in c's scope is not in the CSP.
        '''
        if not type(c) is Constraint:
            print("ERROR: Trying to add non constraint ", c, " to CSP object")
        elif c in self.cons: 
            print("ERROR: Trying to add constraint ", c, " to CSP object that already has it")
        else:
            for v in c.scope:
                if not v in self.vars_to_cons:
                    print("ERROR: Trying to add constraint ", c, " with unknown variables to CSP object")
                    return
                self.vars_to_cons[v].append(c)
            self.cons.append(c)


    def get_all_vars(self):
        '''
            return list of variables in the CSP
        '''
        return list(self.vars)


    def get_all_cons(self):
        '''
            return a list of all constraints in the CSP
        '''
        return self.cons

        
    def get_cons_with_var(self, var):
        '''
            return a list of constraints that have var in their scopes
        '''
        return list(self.vars_to_cons[var])


    def get_all_unasgn_vars(self):
        '''
            return a list of unassigned variables in the CSP
        '''
        return [v for v in self.vars if not v.is_assigned()]


    def print_all(self):
        print("CSP ", self.name)
        print("   Variables = ", self.vars)
        print("   Constraints = ", self.cons)


    def print_soln(self):
        print("CSP", self.name, " Assignments = ")
        for v in self.vars:
            print(v, " = ", v.get_assigned_value(), "    ")
        print("")




class BT:

    """
    A class to perform backtracking search. 

    To solve a CSP, create a BT object with the CSP object,
    then call the bt_search function with a propagator 
    to perform plain backtracking, forward checking, 
    or AC3.

    This class also keeps track of some statistics
    such as the number of variable assignments made, 
    the number of values pruned, and the runtime.
    """

    def __init__(self, csp):
        '''csp == CSP object specifying the CSP to be solved'''

        self.csp = csp
        self.unasgn_vars = list() #used to track unassigned variables

        # Keep track of some statistics
        self.nDecisions = 0 #nDecisions is the number of variable 
                            #assignments made during search
        self.nPrunings  = 0 #nPrunings is the number of value prunings during search
        self.runtime = 0

        self.TRACE = False

        
    def trace_on(self):
        '''Turn search trace on'''
        self.TRACE = True


    def trace_off(self):
        '''Turn search trace off'''
        self.TRACE = False


    def clear_stats(self):
        '''Initialize counters'''
        self.nDecisions = 0
        self.nPrunings = 0
        self.runtime = 0


    def print_stats(self):
        print("Search made {} variable assignments and pruned {} variable values".format(
            self.nDecisions, self.nPrunings))

    def restoreValues(self, prunings):
        '''
            Unprune some values from some variables' domains

            prunings: a list of (variable, value) pairs
        '''
        for var, val in prunings:
            var.unprune_value(val)

    def restore_all_variable_domains(self):
        '''
            Reinitialize all variable domains

            Unassign all the variables, and
            reset their current domains to their permanent domains.
        '''
        for var in self.csp.vars:
            if var.is_assigned():
                var.unassign()
            var.restore_curdom()

        
    def bt_search(self, propagator, var_ord=None, val_ord=None):
        '''
            Try to solve the CSP with a propagator function 
            and optionally a function for choosing the next variable to assign 
            and a function to choosing an order of values to try. 
            Print out the end result. 
            This is a wrapper function to bt_recurse.

            The propagator functino returns status, prunings
            status is True or False.
                returns False if it has detected a deadend and needs to backtrack.
                returns True if we can continue. 
            prunings is a list of (Variable, Value) pairs that were pruned.
                bt_search needs this information in order to restore these values 
                when it undoes a variable assignment.

            var_ord is a function that returns the next variable to be assigned.

            val_ord is a function that returns the values in some order.
        '''

        # initialize statistics
        self.clear_stats()
        stime = time.process_time()

        # reset the domains of all the variables to their permanent domains
        self.restore_all_variable_domains()
        
        # create a list of the unassigned variables
        self.unasgn_vars = []
        for v in self.csp.vars:
            if not v.is_assigned():
                self.unasgn_vars.append(v)

        # perform propagation before assigning any variables.
        status, prunings = propagator(self.csp) 
        self.nPrunings = self.nPrunings + len(prunings)

        if self.TRACE:
            print(len(self.unasgn_vars), " unassigned variables at start of search")
            print("Prunings before any variable assignments: ", prunings)

        if status == False:
            print("CSP {} detected contradiction at root".format(self.csp.name))
        else:
            # perform recursive search
            status = self.bt_recurse(propagator, var_ord, val_ord, 1) 

        self.restoreValues(prunings)

        if status == False:

            # unable to solve the CSP
            print("CSP {} has no solutions".format(self.csp.name))
        if status == True:

            # print out the CSP's solutions
            endtime = time.process_time()
            print("CSP {} solved. CPU Time used = {}".format(self.csp.name, endtime - stime))
            self.csp.print_soln()

        print("bt_search finished")
        self.print_stats()



    def bt_recurse(self, propagator, var_ord, val_ord, level):
        '''
            Recursive function to perform backtracking search.

            Return true if a solution is found. 
            Return false if we need to backtrack.
        '''

        if self.TRACE:
            print('  ' * level, "bt_recurse level ", level)
           
        if not self.unasgn_vars:
            # All the variables have been assigned.
            # Solution found!
            return True

        else:
            
            # Determine which variable to assign next. 
            if var_ord:
              var = var_ord(self.csp)
            else:
              var = self.unasgn_vars[0]
            self.unasgn_vars.remove(var) # remove var from the list of unassigned vars

            if self.TRACE:
                print('  ' * level, "bt_recurse var = ", var)

            # Determine which value to try next.
            if val_ord:
              value_order = val_ord(self.csp,var)
            else:
              value_order = var.cur_domain()

            # Try the values in order
            for val in value_order:

                if self.TRACE:
                    print('  ' * level, "bt_recurse trying", var, "=", val)

                # Assign the value
                var.assign(val)
                self.nDecisions = self.nDecisions + 1

                # Prune values using the propagator
                status, prunings = propagator(self.csp, var)
                self.nPrunings = self.nPrunings + len(prunings)

                if self.TRACE:
                    print('  ' * level, "bt_recurse prop status = ", status)
                    print('  ' * level, "bt_recurse prop pruned = ", prunings)

                if status == True:
                    # Perform recursive call
                    if self.bt_recurse(propagator, var_ord, val_ord, level+1):
                        return True

                # Reached a deadend. Restore pruned values and unassign the variable.
                if self.TRACE:
                    print('  ' * level, "bt_recurse restoring ", prunings)
                self.restoreValues(prunings)
                var.unassign()

            # Add var to the list of unassigned vars
            self.unasgn_vars.append(var)
            return False # Backtrack

