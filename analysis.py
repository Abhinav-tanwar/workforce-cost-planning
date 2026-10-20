import numpy as np
from scipy.optimize import milp, linprog, Bounds, LinearConstraint
from utils import save


def weekly_coverage():
    demand = np.array([6, 6, 6, 6, 10, 10, 8])
    A = np.array(
        [[int((day - start) % 7 < 5) for start in range(7)] for day in range(7)]
    )
    result = milp(
        np.ones(7),
        integrality=np.ones(7),
        bounds=Bounds(0, np.inf),
        constraints=LinearConstraint(A, demand, np.inf),
    )
    assert result.success
    x = np.rint(result.x).astype(int)
    assert np.all(A @ x >= demand)
    return dict(
        starts_by_day=x.tolist(),
        coverage=(A @ x).tolist(),
        demand=demand.tolist(),
        headcount=int(x.sum()),
        mip_gap=float(result.mip_gap),
    )


def overtime_scenarios():
    labor = np.array([20, 30, 10, 25])
    matA = np.array([160, 100, 200, 75])
    matB = np.array([30, 35, 60, 80])
    p1 = np.array([35, 45, 70, 0])
    p2 = np.array([55, 42, 0, 90])
    A = np.array([matA, matB, labor, -p1, -p2])
    b = np.array([8000, 4000, 1000, -2100, -1800])
    c = 3 * matA + 7 * matB
    result = {}
    for overtime in [False, True]:
        matrix = np.column_stack([A, [0, 0, -1, 0, 0]]) if overtime else A
        cost = np.r_[c, 30] if overtime else c
        bounds = [(0, None)] * 4 + ([(0, 200)] if overtime else [])
        r = linprog(cost, A_ub=matrix, b_ub=b, bounds=bounds, method="highs")
        entry = dict(success=bool(r.success), solver_status=int(r.status))
        if r.success:
            entry.update(
                cost=float(r.fun),
                process_hours=r.x[:4].tolist(),
                overtime_hours=float(r.x[4]) if overtime else 0,
                max_constraint_violation=float(max(0, np.max(matrix @ r.x - b))),
            )
        result["with_overtime" if overtime else "base_hours"] = entry
    return result


def run():
    return save(
        dict(
            weekly_coverage=weekly_coverage(),
            process_planning=overtime_scenarios(),
            scope="illustrative demand and cost inputs; fixed base labor cost excluded from both scenarios",
        )
    )


if __name__ == "__main__":
    run()
