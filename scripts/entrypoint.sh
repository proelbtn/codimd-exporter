#!/bin/bash

[ "${CODIMD_DEBUG}" != "" ] && set -ex

git config --global user.email "${CODIMD_EMAIL}"
git config --global user.name "${CODIMD_NAME}"

if [ ! -d /var/run/codimd-exporter/repo ]; then
  git clone ${CODIMD_REPOSITORY} /var/run/codimd-exporter/repo
else
  cd /var/run/codimd-exporter/repo
  git pull origin ${CODIMD_BRANCH}
  cd -
fi

rm -rf /var/run/codimd-exporter/repo/*.md
python3 fetcher.py > /tmp/archive.zip
unzip /tmp/archive.zip -d /var/run/codimd-exporter/repo

cd /var/run/codimd-exporter/repo
if [ "$(git status -s)" != "" ]; then
  git add .
  git commit -m "updated"
  git push origin ${CODIMD_BRANCH}
fi
