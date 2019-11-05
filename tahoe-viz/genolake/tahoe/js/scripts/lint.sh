#!/bin/bash

# Check that all .js files have an @flow comment.
noflow=$(git ls-files | egrep '^(src|test).*\.js$' | grep -v '/data-canvas.js' | xargs grep --files-without-match '@flow')
if [ -n "$noflow" ]; then
  echo 'These files are missing @flow annotations:'
  echo "$noflow"
  exit 1
fi

# Run the usual linter
./node_modules/.bin/jsxhint --es6module --harmony 'src/main/**/*.js' 'src/test/**/*.js'
