#!/bin/bash -exu
echo "Update assets for ${VERSION}"
python manage.py collectstatic --noinput
git checkout gh-pages
cp -rn staticfiles/* assets/master/
set +e
git commit -m "Deploy ${VERSION} assets" && git push origin gh-pages
set -e
git checkout master