# This import is required to import Jupyter notebooks like regular Python files
from notebook_helper import importer

# This imports the student notebook, but does not yet run all the code cells
# The module name needs to matche the student file name, omitting the .ipynb extension
import Homework_8 as hw
import Homework_8_solution as solution

# This is a library for helping write some tests
import cds_testing

import numpy as np
import pandas as pd

import pytest


@pytest.fixture(scope='module', autouse=True)
def run_notebook():
    """This executes the code in the notebook before running the tests."""
    importer.run_cells(hw, raise_on_error=False)
    importer.run_cells(solution, raise_on_error=False)


# This executes the code in the student and solution notebooks before running the tests.
load_student_code = pytest.fixture(cds_testing.load_code, params=[hw], scope='module', autouse=True)
load_solution_code = pytest.fixture(cds_testing.load_code, params=[solution], scope='module', autouse=True)

@pytest.fixture(scope='module', autouse=True)
def expected_shuffled_diffs_10000(run_notebook):
    """
    Since the dataset sample will vary for students based on their student numbers,
    we have to load the shuffled_diffs_10000 for each student number rather than referencing the solution.
    """
    
    student_number = getattr(hw, "student_number", None)

    if student_number is None:
        return None
    
    np.random.seed(hw.student_number)

    return solution.shuffled_diffs(10000)

def test_mh_visit_instability_without_instability_binary_column():
    """Test that the 'mh_visit_instability' dataframe is correctly created in your notebook up to step 3 before creating the `instability_binary` column. 
    """

    # Since the dataframe later gets changed, we verify the correctness for it upto step 3 of the homework.
    # Check that the variable exists in the notebook
    assert hasattr(hw, 'mh_visit_instability'),\
            'We could not find a DataFrame called "mh_visit_instability" in your file.'

    # Make sure that the variable is a pandas dataframe
    assert isinstance(hw.mh_visit_instability, pd.DataFrame),\
        'Your mh_visit_instability variable is incorrectly defined. It should refer to a Pandas dataframe.'


    # Copy the columns required only for task 1c. 
    hw_df_copy = hw.mh_visit_instability.copy()
    soln_df_copy = solution.mh_visit_instability.copy()

    hw_df_copy.drop(columns=['instability_binary'], inplace=True)
    soln_df_copy.drop(columns=['instability_binary'], inplace=True)

    pd.testing.assert_frame_equal(hw_df_copy, soln_df_copy, obj="(Step 3) mh_visit_instability")

def test_student_number():
    """Test that the 'student_number' variable has been defined correctly
    in your notebook.
    """

    assert hasattr(hw, 'student_number'),\
            'We could not find a variable called "student_number" in your file.'

    # Check that the number has been defined as an integer
    assert isinstance(hw.student_number, int),\
        'Your student_number variable should be an integer'


def test_shuffled_diffs_function_exists():

    # Test that the function exists in the student solution and takes in two arguments
    assert "shuffled_diffs" in dir(hw),\
        'The function "shuffled_diffs" is not defined in your notebook.'
    assert hw.shuffled_diffs.__code__.co_argcount == 1, \
        'The function "shuffled_diffs", should have 1 argument, number_of_shuffles (an integer).'

def test_shuffled_diffs_10000(expected_shuffled_diffs_10000):
    """Test that the 'shuffled_diffs_10000' variable has been defined correctly
    in your notebook.
    """

    # To load the data, we need their student number
    # This is just a check. The previous student number test would give them more information about their mistake.
    assert hasattr(hw, 'student_number') and isinstance(hw.student_number, int),\
        'We could not test for the "sub_time_use_data" variable as it is based on the student_number variable, which is incorrectly defined or missing.'


    assert hasattr(hw, 'shuffled_diffs_10000'),\
            'We could not find a variable called "shuffled_diffs_10000" in your file.'

    # Check that the number has been defined as an integer
    assert isinstance(hw.shuffled_diffs_10000, list),\
        'Your shuffled_diffs_10000 variable should be a list.'


    cds_testing.assert_list_equality(student_value=hw.shuffled_diffs_10000, soln_value = expected_shuffled_diffs_10000, var_name='shuffled_diffs_10000')

def test_right_extreme(expected_shuffled_diffs_10000):
    """Test that the 'right_extreme' variable has been defined correctly
    in your notebook.
    """

    # To load the data, we need their student number
    # This is just a check. The previous student number test would give them more information about their mistake.
    assert hasattr(hw, 'student_number') and isinstance(hw.student_number, int),\
        'We could not test for the "right_extreme" variable as it is based on the student_number variable, which is incorrectly defined or missing.'

    assert hasattr(hw, 'right_extreme'),\
            'We could not find a variable called "right_extreme" in your file.'

    # Check that the number has been defined as an integer
    assert isinstance(hw.right_extreme, (int, np.int_)),\
        'Your right_extreme variable should be an integer or a numpy integer.'

    expected_right_extreme = expected_shuffled_diffs_10000 >= solution.median_diff
    expected_right_extreme = expected_right_extreme.sum()

    msg = (
        f"\n"
        f"ISSUE FOUND: The value of your list variable `right_extreme`:\n"
        f"\n"
        f"     {hw.right_extreme}"
        f"\n\n"
        f"is not equal to what we expect:\n"
        f"\n"
        f"     {expected_right_extreme}\n"
    )
    assert hw.right_extreme == expected_right_extreme, msg

def test_left_extreme(expected_shuffled_diffs_10000):
    """Test that the 'left_extreme' variable has been defined correctly
    in your notebook.
    """
    # To load the data, we need their student number
    # This is just a check. The previous student number test would give them more information about their mistake.
    assert hasattr(hw, 'student_number') and isinstance(hw.student_number, int),\
        'We could not test for the "left_extreme" variable as it is based on the student_number variable, which is incorrectly defined or missing.'

    assert hasattr(hw, 'left_extreme'),\
            'We could not find a variable called "left_extreme" in your file.'

    assert isinstance(hw.left_extreme, (int, np.int_)),\
        'Your left_extreme variable should be an integer or a numpy integer.'

    expected_left_extreme = expected_shuffled_diffs_10000 < -1*solution.median_diff
    expected_left_extreme = expected_left_extreme.sum()

    msg = (
        f"\n"
        f"ISSUE FOUND: The value of your list variable `left_extreme`:\n"
        f"\n"
        f"     {hw.left_extreme}"
        f"\n\n"
        f"is not equal to what we expect:\n"
        f"\n"
        f"     {expected_left_extreme}\n"
    )
    assert hw.left_extreme == expected_left_extreme, msg


def test_pvalue(expected_shuffled_diffs_10000):
    """Test that the 'pvalue' variable has been defined correctly
    in your notebook.
    """

    # To load the data, we need their student number
    # This is just a check. The previous student number test would give them more information about their mistake.
    assert hasattr(hw, 'student_number') and isinstance(hw.student_number, int),\
        'We could not test for the "pvalue" variable as it is based on the student_number variable, which is incorrectly defined or missing.'


    assert hasattr(hw, 'pvalue'),\
            'We could not find a variable called "pvalue" in your file.'

    # Check that the number has been defined as an integer
    assert isinstance(hw.pvalue, (float, np.float64)),\
        'Your pvalue variable should be a float or a numpy float.'


    expected_right_extreme = expected_shuffled_diffs_10000 >= solution.median_diff
    expected_right_extreme = expected_right_extreme.sum()
    expected_left_extreme = expected_shuffled_diffs_10000 < -1*solution.median_diff
    expected_left_extreme = expected_left_extreme.sum()
    expected_pvalue = (expected_left_extreme + expected_right_extreme)/10000

    msg = (
        f"\n"
        f"ISSUE FOUND: The value of your list variable `pvalue`:\n"
        f"\n"
        f"     {hw.pvalue}"
        f"\n\n"
        f"is not equal to what we expect:\n"
        f"\n"
        f"     {expected_pvalue}\n"
    )
    assert hw.pvalue == expected_pvalue, msg


def test_nullhypothesis_distribution_plot(expected_shuffled_diffs_10000):
    """Test that the 'nullhypothesis_distribution_plot' plot has been created correctly
    in your notebook.
    """

    # To load the data, we need their student number
    # This is just a check. The previous student number test would give them more information about their mistake.
    assert hasattr(hw, 'student_number') and isinstance(hw.student_number, int),\
        'We could not test for the "pvalue" variable as it is based on the student_number variable, which is incorrectly defined or missing.'


    assert hasattr(hw, 'pvalue'),\
            'We could not find a variable called "pvalue" in your file.'

    # Check that the number has been defined as an integer
    assert isinstance(hw.pvalue, (float, np.float64)),\
        'Your pvalue variable should be a float or a numpy float.'

    expected_right_extreme = expected_shuffled_diffs_10000 >= solution.median_diff
    expected_right_extreme = expected_right_extreme.sum()
    expected_left_extreme = expected_shuffled_diffs_10000 < -1*solution.median_diff
    expected_left_extreme = expected_left_extreme.sum()
    expected_pvalue = (expected_left_extreme + expected_right_extreme)/10000

    msg = (
        f"\n"
        f"ISSUE FOUND: The value of your list variable `pvalue`:\n"
        f"\n"
        f"     {hw.pvalue}"
        f"\n\n"
        f"is not equal to what we expect:\n"
        f"\n"
        f"     {expected_pvalue}\n"
    )
    assert hw.pvalue == expected_pvalue, msg

EXPECTED_VARS = {
    # Step 1
    'marg_neighbourhoods': {},
    'instability_df': {},
    # Step 2
    'mental_health_neighbourhoods': {},
    'mh_visit_rates': {},
    # Step 4
    'mh_visit_instability': {},
    'instability_binary_frequencies': {},
    # Step 5
    'median_table': {},
    'median_diff': {}
}

test_variable_names = cds_testing.make_variable_names_test(hw, EXPECTED_VARS)
test_answer_equality = cds_testing.make_answer_equality_test(hw, solution, EXPECTED_VARS)
