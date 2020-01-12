#!/bin/bash
style() {
  watch -n 5 pycodestyle --max-line-length=100 ojo/*.py
}

todo() {
  git grep -r 'TODO' | less
}
