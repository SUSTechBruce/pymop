from pymop import *

STR_TO_PROBLEM = {
    'ackley': Ackley,
    'bnh': BNH,
    'carside': Carside,
    'dtlz1': DTLZ1,
    'dtlz2': DTLZ2,
    'dtlz3': DTLZ3,
    'dtlz4': DTLZ4,
    'dtlz5': DTLZ5,
    'dtlz6': DTLZ6,
    'dtlz7': DTLZ7,
    'griewank': Griewank,
    'knp': Knapsack,
    'kursawe': Kursawe,
    'osy': OSY,
    'rastrigin': Rastrigin,
    'rosenbrock': Rosenbrock,
    'schwefel': Schwefel,
    'sphere': Sphere,
    'tnk': TNK,
    'truss2d': Truss2D,
    'welded_beam': WeldedBeam,
    'zakharov': Zakharov,
    'zdt1': ZDT1,
    'zdt2': ZDT2,
    'zdt3': ZDT3,
    'zdt4': ZDT4,
    'zdt6': ZDT6,
    'g01': G1,
    'g02': G2,
    'g03': G3,
    'g04': G4,
    'g05': G5,
    'g06': G6,
    'g07': G7,
    'g08': G8,
    'g09': G9,
    'g10': G10
}


def get_problem(name, *args, **kwargs):
    return STR_TO_PROBLEM[name.lower()](*args, **kwargs)


def get_problem_from_func(func, xl, xu, n_var=None, func_args={}):
    if xl is None or xu is None:
        raise Exception("Please provide lower and upper bounds for the problem.")
    if isinstance(xl, (int, float)):
        xl = xl * anp.ones(n_var)
    if isinstance(xu, (int, float)):
        xu = xu * anp.ones(n_var)

    # determine through a test evaluation details about the problem
    n_var = xl.shape[0]
    n_obj = -1
    n_constr = 0

    out = {}
    func(xl[None, :], out, **func_args)
    at_least2d(out)

    n_obj = out["F"].shape[1]
    if out.get("G") is not None:
        n_constr = out["G"].shape[1]

    class MyProblem(Problem):
        def __init__(self):
            Problem.__init__(self)
            self.n_var = n_var
            self.n_constr = n_constr
            self.n_obj = n_obj
            self.func = self._evaluate
            self.xl = xl
            self.xu = xu

        def _evaluate(self, x, out, *args, **kwargs):
            func(x, out, *args, **kwargs)

    return MyProblem()
