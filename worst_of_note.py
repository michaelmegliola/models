import QuantLib as ql
import numpy as np
import pandas as pd
from riskops_citi.models.structured_notes.structured_note import StructuredNote


class WorstOfNote(StructuredNote):
        
    def calc(self, paths, cfs):
        # calculation for worst performing underlying asset
        def asset_performance(initial, final): return 1 + ((final - initial) / initial)
        init_pxs = np.array(self.terms['pxs'])
        contingent_pxs = init_pxs * 0.50
        barrier_pxs = init_pxs * 0.55

        for j in range(self.scheduled_cash_flows['n']):
            fwd_pxs = paths[:, j]
            # early redemption
            if all(fwd_pxs >= init_pxs):
                cfs[j] = 1045.00
                break
            # conditional coupon payments
            elif all(fwd_pxs >= contingent_pxs):
                cfs[j] = 45.00
            # redemption amount at maturity
            if j == self.scheduled_cash_flows['n'] - 1:
                if any(fwd_pxs <= barrier_pxs):
                    cfs[j] += 1000.00 * min(asset_performance(init_pxs, fwd_pxs))
                else:
                    cfs[j] += 1000.00
