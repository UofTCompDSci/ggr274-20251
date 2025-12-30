from notebook_helper import importer
import Lab_8 as hw
import Lab_8_solution as soln
import pytest

import cds_testing

# This line creates a pytest fixture that runs all code cells in hw.
# The scope='module' and autouse=True arguments ensure that the code is run once
# when this module is executed.
load_student_code = pytest.fixture(cds_testing.load_code, params=[hw], scope='module', autouse=True)
load_soln_code = pytest.fixture(cds_testing.load_code, params=[soln], scope='module', autouse=True)

EXPECTED_VARS = {
    # Task 1
    'promoted_males': {},
    'promoted_females': {},
    'observed_diff': {},
    
    # Task 2
    'bias_sex_shuffle': {},
    'promoted_males_shuffled': {},
    'promoted_females_shuffled': {},
    'prop_males_shuffled': {},
    'prop_females_shuffled': {},
    'diff_sim': {},
    
    # Task 3
    'sim_results': {},
    
    # Task 5
    'pvalue': {}
}

test_variable_names = cds_testing.make_variable_names_test(hw, EXPECTED_VARS)
# test_answer_equality = cds_testing.make_answer_equality_test(hw, soln, EXPECTED_VARS)
