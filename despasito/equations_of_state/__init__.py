"""

Create an EOS class from options taken from factory design pattern.

"""

# Add imports here
from importlib import import_module
import logging

#from despasito import method_stat

logger = logging.getLogger(__name__)

def eos(eos="saft.gamma_mie", **input_dict):
    """
    Interface between the user and our library of equations of state (EOS).

    Input the name of a desired EOS and a factory design pattern with a dictionary will search available classes to allow easy implementation of new EOS.

    Parameters
    ----------
    input_dict : dict, Optional
        A dictionary of inputs for the desired EOS. See specific EOS documentation for required inputs.

        - eos : str - Input should be in the form EOSfamily.EOSname (e.g. saft.gamme_mie). Note that the name of the class is EOSfamily_EOSname.
                
    Returns
    -------
    instance : obj
        An instance of the defined EOS class to be used in thermodynamic computations.
    """

#    if "numba" in input_dict:
#        method_stat.disable_numba = False
#        del input_dict["numba"]
#    if "cython" in input_dict:
#        method_stat.disable_cython = False
#        del input_dict["cython"]
#    if "python" in input_dict:
#        method_stat.disable_python = False
#        del input_dict["python"]

    factory_families = ["saft"] # eos families in this list have a general object with a factory to import relevent modules

    logger.info("Using EOS: {}".format(eos))

    try:
        eos_fam, eos_type = eos.split('.')
    except:
        raise Exception("Input should be in the form EOSfamily.EOSname (e.g. saft.gamme_mie).")

    class_name = "EosType"
    try:
        if eos_fam in factory_families:
            eos_module = import_module('.' + eos_fam, package="despasito.equations_of_state." + eos_fam)
            input_dict['saft_name'] = eos_type
        
        else:
            eos_module = import_module('.' + eos_type, package="despasito.equations_of_state." + eos_fam)
        eos_class = getattr(eos_module, class_name)
    except (AttributeError):
        raise ImportError("Based on your input, '{}', we expect the class, {}, in a module, {}, found in the package, {}, which indicates the EOS family.".format(eos, class_name, eos_type, eos_fam))
    instance = eos_class(**input_dict)

    logger.info("Created {} eos object".format(eos))

    return instance

