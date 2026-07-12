"""Mini Git 엔트리 포인트.

과제 명세의 실행 방법(`python main.py`)을 그대로 따른다. 실제 로직은
전부 mini_git/ 패키지 안에 모듈별로 분리되어 있고, 이 파일은 그 패키지를
불러와 REPL을 시작하는 역할만 한다.
"""
from mini_git.cli import run

if __name__ == "__main__":
    run()
