# cython: cdivision=True
# cython: boundscheck=False
# cython: wraparound=False

# Author: Mathieu Blondel, Tom Dupre la Tour
# License: BSD 3 clause
# Adapted by Frederic Marcotte to consider bayesian constraint update rules
# python setup.py build_ext --inplace

from cython cimport floating
from libc.math cimport fabs


def _update_w_fast(floating[:, ::1] W, floating[:, :] HHt,
                   floating[:, :] XHt):
    cdef:
        floating violation = 0
        Py_ssize_t n_components = W.shape[1]
        Py_ssize_t n_samples = W.shape[0]
        floating grad, pg, hess
        Py_ssize_t i, r, s

    with nogil:
        for s in range(n_components):

            for i in range(n_samples):

                # gradient = GW[i, s] where GW = np.dot(W, HHt) - XHt
                grad = -XHt[i, s]

                for r in range(n_components):
                    grad += W[i, r] * HHt[r, s]

                # projected gradient
                pg = min(0., grad) if W[i, s] == 0 else grad
                violation += fabs(pg)

                # Hessian
                hess = HHt[s, s]

                if hess != 0:
                    W[i, s] = max(W[i, s] - grad / hess, 0.)

    return violation


def _update_h_fast(floating[:, ::1] Ht, floating[:, :] WtW,
                   floating[:, :] XtW, floating[:, ::1] Hpt,
                   floating beta):
    cdef:
        floating violation = 0
        Py_ssize_t n_components = Ht.shape[1]
        Py_ssize_t n_features = Ht.shape[0]
        floating grad, pg, hess
        Py_ssize_t i, r, s

    with nogil:
        for s in range(n_components):

            for i in range(n_features):

                # gradient = GW[i, s] where GW = np.dot(Ht, WtW) - XtW + beta * (Ht- Hpt)
                grad = -XtW[i, s]

                for r in range(n_components):
                    grad += Ht[i, r] * WtW[r, s]

                grad += beta * (Ht[i, s] - Hpt[i, s])

                # projected gradient
                pg = min(0., grad) if Ht[i, s] == 0 else grad
                violation += fabs(pg)

                # Hessian
                hess = WtW[s, s] + beta

                if hess != 0:
                    Ht[i, s] = max(Ht[i, s] - grad / hess, 0.)

    return violation