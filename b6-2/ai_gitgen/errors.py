class AiGitGenError(Exception):
    """이 도구에서 발생하는 모든 예외의 기반 클래스."""


class NoApiKeyError(AiGitGenError):
    def __init__(self):
        super().__init__(
            "AI_API_KEY(또는 ANTHROPIC_API_KEY) 환경변수가 설정되지 않았습니다.\n"
            "  export AI_API_KEY=\"YOUR_KEY\"\n"
            "위 명령으로 API 키를 설정한 뒤 다시 실행하세요."
        )


class NoChangesError(AiGitGenError):
    def __init__(self, hint: str):
        super().__init__(hint)


class NotAGitRepoError(AiGitGenError):
    def __init__(self):
        super().__init__("현재 디렉터리는 git 저장소가 아닙니다. 'git init' 또는 저장소 루트에서 실행하세요.")


class ApiCallError(AiGitGenError):
    def __init__(self, reason: str):
        super().__init__(f"AI API 호출에 실패했습니다: {reason}")


class OutputValidationError(AiGitGenError):
    def __init__(self, problems: list):
        self.problems = problems
        detail = "\n".join(f"  - {p}" for p in problems)
        super().__init__(f"생성된 결과가 검증 규칙을 만족하지 않습니다:\n{detail}")
