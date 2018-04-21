import random
from psychopy import visual, event, core
import dot_experiment
from bams.learners import ActiveLearner
from bams.query_strategies import (
    # BALD,
    HyperCubePool,
    RandomStrategy,
)


NDIM = 1
POOL_SIZE = 500
BUDGET = 10
BASE_KERNELS = ["PER", "LIN"]
DEPTH = 1

win = visual.Window(
size=[500, 500],
units="pix",
fullscr=False
)
answer_text = visual.TextStim(win)

def scale_up(threshold, dim):
    """Rescale up to actual values"""
    out = int(dim * threshold)
    return out

def scale_down(threshold, dim):
    """Rescale 0 =< output =< 1"""
    out = float(dim/threshold) if threshold else 0.0
    return out

def oracle(x):
    """Run a psychopy experiment by scaling up the features so they can be used as input.
    Then scale down the output for the active learner.
    """
    n_dots = 100
    # Scale up
    print(x[0])
    n_dots = scale_up(n_dots, float(x[0]))
    print(n_dots)
    guess = dot_experiment(win, answer_text, n_dots)
    score = (int(guess)/n_dots)
    return score


learner = ActiveLearner(
    query_strategy=RandomStrategy(pool=HyperCubePool(NDIM, POOL_SIZE)),
    budget=BUDGET,
    base_kernels=BASE_KERNELS,
    max_depth=DEPTH,
    ndim=NDIM,
)

while learner.budget > 0:
    x = learner.next_query()
    y = learner.query(oracle, x)
    learner.update(x, y)
    print(learner.posteriors)
    print(learner.map_model)