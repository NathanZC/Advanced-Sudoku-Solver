def prop_FC(csp, last_assigned_var=None):
    """
    This is a propagator to perform forward checking. 

    First, collect all the relevant constraints.
    If the last assigned variable is None, then no variable has been assigned 
    and we are performing propagation before search starts.
    In this case, we will check all the constraints.
    Otherwise, we will only check constraints involving the last assigned variable.

    Among all the relevant constraints, focus on the constraints with one unassigned variable. 
    Consider every value in the unassigned variable's domain, if the value violates 
    any constraint, prune the value. 

    :param csp: The CSP problem
    :type csp: CSP
        
    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing 
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: The boolean indicates whether forward checking is successful.
        The boolean is False if at least one domain becomes empty after forward checking.
        The boolean is True otherwise.
        Also returns a list of variable and value pairs pruned. 
    :rtype: boolean, List[(Variable, Value)]
    """

    prunings = []

    # Determine relevant constraints
    if last_assigned_var is None:
        relevant_constraints = csp.get_all_cons()
    else:
        relevant_constraints = csp.get_cons_with_var(last_assigned_var)

    # Iterate over relevant constraints
    for constraint in relevant_constraints:
        if constraint.get_num_unassigned_vars() == 1:
            unassigned_var = constraint.get_unassigned_vars()[0]
            for value in unassigned_var.cur_domain():
                if not constraint.check(
                        [value] + [var.get_assigned_value() for var in constraint.get_scope() if var.is_assigned()]):
                    prunings.append((unassigned_var, value))
                    unassigned_var.prune_value(value)

    # Check if any domain is empty
    for var in csp.get_all_vars():
        if var.cur_domain_size() == 0:
            return False, prunings

    return True, prunings


def prop_AC3(csp, last_assigned_var=None):
    """
    This is a propagator to perform the AC-3 algorithm.

    Keep track of all the constraints in a queue (list). 
    If the last_assigned_var is not None, then we only need to 
    consider constraints that involve the last assigned variable.

    For each constraint, consider every variable in the constraint and 
    every value in the variable's domain.
    For each variable and value pair, prune it if it is not part of 
    a satisfying assignment for the constraint. 
    Finally, if we have pruned any value for a variable,
    add other constraints involving the variable back into the queue.

    :param csp: The CSP problem
    :type csp: CSP
        
    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing 
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisifes 
        all the constraints and a list of variable and value pairs pruned. 
    :rtype: boolean, List[(Variable, Value)]
    """
    if last_assigned_var is not None:
        # Initialize the queue with constraints involving the last assigned variable
        queue = csp.get_cons_with_var(last_assigned_var)
    else:
        # Initialize the queue with all constraints
        queue = list(csp.get_all_cons())

    prunings = []

    while queue:
        constraint = queue.pop(0)
        for var in constraint.get_scope():
            for value in var.cur_domain():
                if not is_value_consistent(constraint, var, value):
                    prunings.append((var, value))
                    var.prune_value(value)
                    if var.cur_domain_size() == 0:
                        # If domain is empty, return failure
                        return False, prunings
                    else:
                        # Add related constraints back to the queue
                        for related_constraint in csp.get_cons_with_var(var):
                            if related_constraint != constraint:
                                queue.append(related_constraint)
    return True, prunings


def is_value_consistent(constraint, var, value):
    """
    Check if a value is consistent with the given constraint.
    A value is consistent if it can be part of a satisfying assignment for the constraint.

    :param constraint: The constraint to check
    :type constraint: Constraint
    :param var: The variable to check the value for
    :type var: Variable
    :param value: The value to check
    :type value: int
    :returns: True if the value is consistent, False otherwise
    :rtype: bool
    """
    for other_vars in constraint.get_scope():
        if other_vars != var:
            # Check all combinations of other variable values to see if
            # there exists at least one that satisfies the constraint with the given value.
            for other_val in other_vars.cur_domain():
                if constraint.check([value if v == var else other_val for v in constraint.get_scope()]):
                    return True
    return False



def ord_mrv(csp):
    """
    Implement the Minimum Remaining Values (MRV) heuristic.
    Choose the next variable to assign based on MRV.

    If there is a tie, we will choose the first variable. 

    :param csp: A CSP problem
    :type csp: CSP

    :returns: the next variable to assign based on MRV

    """

    unasgn_vars = csp.get_all_unasgn_vars()

    # If there are no unassigned variables, return None
    if not unasgn_vars:
        return None

    # Find the variable with the minimum remaining values in its domain
    min_domain_size = min(var.cur_domain_size() for var in unasgn_vars)
    for var in unasgn_vars:
        if var.cur_domain_size() == min_domain_size:
            return var

    # In case no variable is found (which shouldn't happen), return None
    return None


def prop_BT(csp, last_assigned_var=None):
    """
    This is a basic propagator for plain backtracking search.

    Check if the current assignment satisfies all the constraints.
    Note that we only need to check all the fully instantiated constraints
    that contain the last assigned variable.

    :param csp: The CSP problem
    :type csp: CSP

    :param last_assigned_var: The last variable assigned before propagation.
        None if no variable has been assigned yet (that is, we are performing
        propagation before search starts).
    :type last_assigned_var: Variable

    :returns: a boolean indicating if the current assignment satisifes all the constraints
        and a list of variable and value pairs pruned.
    :rtype: boolean, List[(Variable, Value)]

    """

    # If we haven't assigned any variable yet, return true.
    if not last_assigned_var:
        return True, []

    # Check all the constraints that contain the last assigned variable.
    for c in csp.get_cons_with_var(last_assigned_var):

        # All the variables in the constraint have been assigned.
        if c.get_num_unassigned_vars() == 0:

            # get the variables
            vars = c.get_scope()

            # get the list of values
            vals = []
            for var in vars: #
                vals.append(var.get_assigned_value())

            # check if the constraint is satisfied
            if not c.check(vals):
                print(c.name)
                return False, []

    return True, []
