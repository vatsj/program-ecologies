"""Game config: k ordered actions (level order A_0 < ... < A_{k-1}), payoff
table(s), minimax action per role, ROLE flag, optional rejection table."""
import os
import numpy as np
import yaml


class Game:
    def __init__(self, cfg, name=None):
        self.name = name or cfg.get('name', 'game')
        acts = list(cfg['actions'])          # in level order
        self.actions = acts
        self.k = len(acts)
        self.role = bool(cfg.get('role', False))
        self.nroles = 2 if self.role else 1
        u1 = np.array([[cfg['payoffs'][a][b] for b in acts] for a in acts], float)
        if 'payoffs2' in cfg:
            u2 = np.array([[cfg['payoffs2'][a][b] for b in acts] for a in acts], float)
        else:
            u2 = u1
        self.pay = np.stack([u1, u2])      # pay[r][a][b]: role-r player plays level a vs level b
        mm1 = cfg['minimax_action']
        mm2 = cfg.get('minimax_action2', mm1)
        self.minimax = np.array([acts.index(mm1), acts.index(mm2)], int)
        self.symmetric = 'payoffs2' not in cfg
        self.reject = None
        if 'reject' in cfg:                 # reject[a][b]: 1 if (role-0 plays a, role-1 plays b) is a rejection
            self.reject = np.array([[cfg['reject'][a][b] for b in acts] for a in acts], float)

    @classmethod
    def load(cls, path):
        with open(path) as f:
            cfg = yaml.safe_load(f)
        return cls(cfg, name=os.path.splitext(os.path.basename(path))[0])

    def payoff(self, Vi, Vj, r=0):
        """Expected payoff of a role-r player with level distribution Vi
        (..., k) against an opponent with distribution Vj (..., k)."""
        Vi = np.asarray(Vi, float); Vj = np.asarray(Vj, float)
        return np.einsum('...a,ab,...b->...', Vi, self.pay[r], Vj)

    def efficient_symmetric(self):
        """max over level profiles of the role-averaged payoff sum / 2."""
        best = -np.inf
        for a in range(self.k):
            for b in range(self.k):
                best = max(best, 0.5 * (self.pay[0][a][b] + self.pay[1][b][a]))
        return best
