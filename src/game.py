"""Game config: two actions, payoff table(s), minimax action, ROLE flag."""
import numpy as np
import yaml


class Game:
    def __init__(self, cfg, name=None):
        self.name = name or cfg.get('name', 'game')
        acts = cfg['actions']
        assert len(acts) == 2, 'DSL is binary: exactly two actions'
        self.actions = acts
        self.role = bool(cfg.get('role', False))
        self.nroles = 2 if self.role else 1
        u1 = np.array([[cfg['payoffs'][a][b] for b in acts] for a in acts], float)
        if 'payoffs2' in cfg:
            u2 = np.array([[cfg['payoffs2'][a][b] for b in acts] for a in acts], float)
        else:
            u2 = u1
        self.pay = np.stack([u1, u2])      # pay[r][a][b]: role-r player plays a vs b
        mm1 = cfg['minimax_action']
        mm2 = cfg.get('minimax_action2', mm1)
        self.minimax_C = np.array([mm1 == acts[0], mm2 == acts[0]], bool)
        self.symmetric = 'payoffs2' not in cfg

    @classmethod
    def load(cls, path):
        with open(path) as f:
            cfg = yaml.safe_load(f)
        import os
        return cls(cfg, name=os.path.splitext(os.path.basename(path))[0])

    def payoff(self, Vi, Vj, r=0):
        """Expected payoff of a role-r player with P(action0)=Vi against an
        opponent with P(action0)=Vj.  Vectorised over arrays."""
        Vi = np.asarray(Vi, float); Vj = np.asarray(Vj, float)
        p = self.pay[r]
        return (p[0, 0] * Vi * Vj + p[0, 1] * Vi * (1 - Vj)
                + p[1, 0] * (1 - Vi) * Vj + p[1, 1] * (1 - Vi) * (1 - Vj))

    def efficient_symmetric(self):
        """max over action profiles of the role-averaged payoff sum / 2."""
        best = -np.inf
        for a in range(2):
            for b in range(2):
                v = 0.5 * (self.pay[0][a][b] + self.pay[1][b][a])
                best = max(best, v)
        return best
