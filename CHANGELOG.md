# CHANGELOG



## v0.2.0 (2023-11-16)

### Chore

* chore(actions): fix build_command in poetry

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`fcb5e5e`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/fcb5e5e0c3a003e751843f35c971824325489ace))

* chore(actions): bump relekang/python-semantic-release to v8.3.0

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`6db63c9`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/6db63c90311117dfb10bfd879bcc097387d909c7))

* chore(deps): update dependencies

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`78b7b1a`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/78b7b1a3d56a149a5819e892edf1f310f5ebffcf))

* chore: upgrade poetry and github actions

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`671f9f0`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/671f9f0a0a98a084de3bb79dc2f4a18fa0dd4543))

### Feature

* feat(evaluate): implement evaluate

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`09ca8ec`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/09ca8ec22a7de20b4e360ebf9f69fd0078ce0f36))

* feat: update retraining (#1)

* fix: remove --no-cache from build command

* fix: add scikit-learn instead of sklearn

* feat(retraining): update retraining script to use urls instead of volumes

BREAKING CHANGE: users need to change the way the output files are written and get the paths from envvars

---------

Co-authored-by: Nourhan Khaled &lt;nourhan.kh02@gmail.com&gt; ([`aab0507`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/aab0507eda373b9ea1f3dfbba2bc1db507236ceb))


## v0.1.8 (2022-12-15)

### Fix

* fix(actions): bump relekang/python-semantic-release to 7.32.2

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`0a5161d`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/0a5161d04a0b990a0c7f1e0182eefbf6de43d901))


## v0.1.7 (2022-12-15)

### Fix

* fix(retraining): throw error on failure

Signed-off-by: Mohamed Tawfik &lt;mtawfik@synapse-analytics.io&gt; ([`7aeebb9`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/7aeebb9a4e42f6630508f53896e525e3848c58bc))


## v0.1.6 (2022-11-02)

### Chore

* chore(serving): update script to handle errors ([`77161bd`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/77161bda923f30ec93a55c2f1501bfac615e88d3))

### Fix

* fix(retraining): change logging into printing ([`95a7e55`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/95a7e559f645db6e305442b8d7d901a8d6b32302))


## v0.1.5 (2022-11-02)

### Fix

* fix(retraining): rename the ground_truth column ([`aa03292`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/aa032922ff849ee1c59c4a5e7492edbea3087a15))


## v0.1.4 (2022-11-01)

### Chore

* chore(actions): update github actions ([`6b669b7`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/6b669b755154b2ee44b232a6e45f6de3a0c3504f))

### Fix

* fix(retraining): fix some error checking ([`5c09b22`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/5c09b22df11699d58d63d0e42a56bfb0e1e9304d))

* fix(retraining): fix retraining root path ([`664eb93`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/664eb93ef35858900bf2057ccb08c911ac6b0974))

### Refactor

* refactor(retraining): add some logging messages ([`68a5d85`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/68a5d8534fb72773ea4ad325aae7c222808121bc))

### Style

* style(retraining): remove some empty spaces ([`a38d85b`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/a38d85bf2c1d637d82e2cc0e9a3381ed03c0a53d))


## v0.1.3 (2022-09-08)

### Fix

* fix(actions): fix using poetry ([`0c6fc69`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/0c6fc69b2ae6a9e1aab342d55b158da11dfb8ac6))


## v0.1.2 (2022-09-08)

### Chore

* chore(actions): fix some actions ([`4c1391d`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/4c1391dc5dd6c6667f3aae7990a7d7526e233d9b))

### Fix

* fix(actions): fix build action ([`f5e5bf1`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/f5e5bf13b4861efc5dd75a760aa9ffc10ab4f7dd))


## v0.1.1 (2022-09-03)

### Chore

* chore(license): add MIT license ([`87dde0b`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/87dde0baf18d6bdf78e0b80e2ba3b1eb60d1ab33))

* chore(titanic): rename root folder ([`37dcc80`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/37dcc80137342198d6167cf507706811eb462862))

### Documentation

* docs(readme): fix readme typo ([`3a5bad8`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/3a5bad8e947c8702ed8fafdf2027b64f82bea901))

### Fix

* fix(serving): fix serving data format ([`ced5349`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/ced53496d80d1d2cec94adae2a37626ab2c718a2))

### Style

* style: add flake8 and fix linting ([`364bf93`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/364bf93cd41a7c527a3e7c2c3cca861a9d594743))

### Unknown

* initial commit ([`c08372f`](https://github.com/SynapseAnalytics/konan-titanic-model/commit/c08372f05d8c4f580c590a3cc0cadd90e9ed8cc4))
