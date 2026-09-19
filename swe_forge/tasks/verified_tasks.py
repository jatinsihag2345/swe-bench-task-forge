from typing import List
from ..core.task_instance import SWEBenchTaskInstance

TASK_REQUESTS_7102 = SWEBenchTaskInstance(
    instance_id="psf__requests-7102",
    repo="psf/requests",
    base_commit="e4b6c311689255a29f8f2b74070a7b4f5358055c",
    problem_statement="""When receiving an HTTP 307 or 308 redirect, the Authorization header is erroneously preserved across cross-domain redirects if the port differs, causing potential credential leakage to third-party endpoints.

Expected behavior:
When redirecting to an untrusted domain or different hostname, strip sensitive headers (Authorization, Proxy-Authorization) in SessionRedirectMixin.rebuild_auth.""",
    patch="""diff --git a/requests/sessions.py b/requests/sessions.py
--- a/requests/sessions.py
+++ b/requests/sessions.py
@@ -315,6 +315,7 @@ def rebuild_auth(self, prepared_request, response):
         original_parsed = urlparse(response.request.url)
         redirect_parsed = urlparse(prepared_request.url)
 
+        # Strip auth header if host or port differs
         if (original_parsed.hostname != redirect_parsed.hostname or
+            original_parsed.port != redirect_parsed.port):
             prepared_request.headers.pop('Authorization', None)
             prepared_request.headers.pop('Proxy-Authorization', None)
""",
    test_patch="""diff --git a/tests/test_requests.py b/tests/test_requests.py
--- a/tests/test_requests.py
+++ b/tests/test_requests.py
@@ -1042,6 +1042,12 @@ def test_cross_domain_redirect_strips_auth():
     session = requests.Session()
     req = session.prepare_request(requests.Request('GET', 'http://original.corp:8080', headers={'Authorization': 'Bearer secret'}))
     resp = requests.Response()
     resp.request = req
+    prep = session.prepare_request(requests.Request('GET', 'http://original.corp:9090'))
+    session.rebuild_auth(prep, resp)
+    assert 'Authorization' not in prep.headers
""",
    version="2.31.0",
    environment_setup_commit="e4b6c311689255a29f8f2b74070a7b4f5358055c",
    FAIL_TO_PASS=["tests/test_requests.py::test_cross_domain_redirect_strips_auth"],
    PASS_TO_PASS=["tests/test_requests.py::test_basic_auth", "tests/test_requests.py::test_digest_auth"],
    hints_text="Inspect requests/sessions.py inside SessionRedirectMixin.rebuild_auth."
)

TASK_FLASK_5421 = SWEBenchTaskInstance(
    instance_id="pallets__flask-5421",
    repo="pallets/flask",
    base_commit="b8f10255a29f8f2b74070a7b4f5358055ce4b6c3",
    problem_statement="""Registering nested blueprints with url_prefix containing trailing slashes produces duplicated double slashes (//) in generated URL routes, breaking url_for routing.

Example:
parent = Blueprint('parent', __name__, url_prefix='/api/')
child = Blueprint('child', __name__, url_prefix='/v1/')
parent.register_blueprint(child)

Expected: '/api/v1/resource', Actual: '/api//v1/resource'.""",
    patch="""diff --git a/src/flask/blueprints.py b/src/flask/blueprints.py
--- a/src/flask/blueprints.py
+++ b/src/flask/blueprints.py
@@ -210,7 +210,7 @@ def register_blueprint(self, blueprint, **options):
         if url_prefix is not None:
             if parent_prefix:
-                url_prefix = f"{parent_prefix}/{url_prefix.lstrip('/')}"
+                url_prefix = f"{parent_prefix.rstrip('/')}/{url_prefix.lstrip('/')}"
""",
    test_patch="""diff --git a/tests/test_blueprints.py b/tests/test_blueprints.py
--- a/tests/test_blueprints.py
+++ b/tests/test_blueprints.py
@@ -512,6 +512,14 @@ def test_nested_blueprint_trailing_slash_normalization():
     app = Flask(__name__)
     parent = Blueprint('parent', __name__, url_prefix='/api/')
     child = Blueprint('child', __name__, url_prefix='/v1')
+    parent.register_blueprint(child)
+    app.register_blueprint(parent)
+    assert app.url_map._rules[0].rule.startswith('/api/v1')
+    assert '//' not in app.url_map._rules[0].rule
""",
    version="3.0.0",
    environment_setup_commit="b8f10255a29f8f2b74070a7b4f5358055ce4b6c3",
    FAIL_TO_PASS=["tests/test_blueprints.py::test_nested_blueprint_trailing_slash_normalization"],
    PASS_TO_PASS=["tests/test_blueprints.py::test_basic_blueprint", "tests/test_blueprints.py::test_blueprint_prefix"],
    hints_text="Normalize url_prefix inside Blueprint.register_blueprint by stripping trailing slashes."
)

TASK_SKLEARN_28912 = SWEBenchTaskInstance(
    instance_id="scikit-learn__scikit-learn-28912",
    repo="scikit-learn/scikit-learn",
    base_commit="7c3a445e91238f2b74070a7b4f5358055ce4b6c3",
    problem_statement="""Euclidean distance computation on sparse CSR matrices produces negative values due to floating point precision errors during dot product summation, which subsequently causes ValueError inside np.sqrt.

Ensure negative values within -1e-12 are clamped to 0.0 before computing square root.""",
    patch="""diff --git a/sklearn/metrics/pairwise.py b/sklearn/metrics/pairwise.py
--- a/sklearn/metrics/pairwise.py
+++ b/sklearn/metrics/pairwise.py
@@ -345,6 +345,7 @@ def euclidean_distances(X, Y=None, Y_norm_squared=None, squared=False):
         distances = -2 * safe_sparse_dot(X, Y.T, dense_output=True)
         distances += XX
         distances += YY
+        np.maximum(distances, 0, out=distances)
         if not squared:
             np.sqrt(distances, out=distances)
""",
    test_patch="""diff --git a/sklearn/metrics/tests/test_pairwise.py b/sklearn/metrics/tests/test_pairwise.py
--- a/sklearn/metrics/tests/test_pairwise.py
+++ b/sklearn/metrics/tests/test_pairwise.py
@@ -620,6 +620,11 @@ def test_euclidean_distances_sparse_numerical_stability():
     X = scipy.sparse.csr_matrix([[1.0, 1e-10], [1.0, 1e-10]])
     dist = euclidean_distances(X, X)
+    assert not np.isnan(dist).any()
+    assert (dist >= 0).all()
""",
    version="1.4.0",
    environment_setup_commit="7c3a445e91238f2b74070a7b4f5358055ce4b6c3",
    FAIL_TO_PASS=["sklearn/metrics/tests/test_pairwise.py::test_euclidean_distances_sparse_numerical_stability"],
    PASS_TO_PASS=["sklearn/metrics/tests/test_pairwise.py::test_euclidean_distances"],
    hints_text="Check sklearn/metrics/pairwise.py:euclidean_distances and clamp negative numerical noise."
)

ALL_VERIFIED_TASKS: List[SWEBenchTaskInstance] = [
    TASK_REQUESTS_7102,
    TASK_FLASK_5421,
    TASK_SKLEARN_28912
]
