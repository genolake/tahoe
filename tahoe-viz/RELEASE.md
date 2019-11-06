- To release a new version of genolake.tahoe.pileup on PyPI:

Update version in _version.py (set release version, remove 'dev')
Update version in genolake/tahoe/pileup/js/package.json
make clean
make sdist
git add and git commit
make sdist
twine upload dist/*.tar.gz
git tag -a X.X.X -m 'comment'

Update _version.py (add 'dev' and increment minor)
git add and git commit
git push
git push --tags
