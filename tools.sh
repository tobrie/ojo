#!/bin/bash
style() {
  watch -n 5 pycodestyle --max-line-length=100 ojo/*.py
}

todo() {
  git grep -r 'TODO' | less
}

setup() {
  rm -rf ojo/venv
  virtualenv -p python3 ojo/venv
  source ojo/venv/bin/activate
  pip install -r ojo/requirements.txt
}
