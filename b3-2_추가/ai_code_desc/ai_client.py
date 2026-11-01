"""AI API(Anthropic Messages API) 호출과 예외 처리.

API Key는 환경변수 AI_API_KEY 또는 ANTHROPIC_API_KEY에서만 읽는다.
"""

import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_MAX_TOKENS = 16000
DEFAULT_EFFORT = "low"
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
# 정책 거절(refusal) 시 서버가 권장 모델로 자동 재시도하도록 하는 옵션
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class AIError(RuntimeError):
    """AI API 호출 실패. 메시지에 원인과 대처 방법을 담는다."""


@dataclass
class ModelSettings:
    model: str = DEFAULT_MODEL
    max_tokens: int = DEFAULT_MAX_TOKENS
    effort: str = DEFAULT_EFFORT
    temperature: Optional[float] = None


def get_api_key() -> str:
    """환경변수에서 API Key를 읽는다. 없으면 AIError."""
    key = os.environ.get("AI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise AIError(
            "AI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            '## 예) export AI_API_KEY="YOUR_KEY"\n'
            "## API 없이 흐름만 확인하려면 --mock 옵션을 사용하세요.")
    return key


def ensure_ready() -> None:
    """API 호출 전에 API Key와 SDK 설치 여부를 확인한다."""
    get_api_key()
    try:
        import anthropic  # noqa: F401
    except ImportError as exc:
        raise AIError("anthropic 패키지가 설치되지 않았습니다. "
                      "`python3 -m pip install -r requirements.txt`를 실행하세요.") from exc


def call_model(system_prompt: str, user_prompt: str, settings: ModelSettings) -> str:
    """Messages API를 1회 호출하고 응답 텍스트를 반환한다."""
    ensure_ready()
    import anthropic

    api_key = get_api_key()

    client = anthropic.Anthropic(api_key=api_key, timeout=120.0, max_retries=2)
    kwargs = {
        "model": settings.model,
        "max_tokens": settings.max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
        "output_config": {"effort": settings.effort},
        "betas": [FALLBACK_BETA],
        "fallbacks": "default",
    }
    if settings.temperature is not None:
        # 최신 API 버전은 temperature를 받지 않는다. 지정 시 그대로 전달하고 400 응답을 안내한다.
        kwargs["extra_body"] = {"temperature": settings.temperature}

    try:
        response = client.beta.messages.create(**kwargs)
    except anthropic.AuthenticationError as exc:
        raise AIError(f"인증 실패(401): API Key가 올바른지 확인하세요. ({_detail(exc)})") from exc
    except anthropic.PermissionDeniedError as exc:
        raise AIError(f"권한 없음(403): 이 키로 모델 '{settings.model}'을 사용할 수 없습니다. ({_detail(exc)})") from exc
    except anthropic.NotFoundError as exc:
        raise AIError(f"모델을 찾을 수 없음(404): --model 값 '{settings.model}'을 확인하세요. ({_detail(exc)})") from exc
    except anthropic.RateLimitError as exc:
        raise AIError(f"요청 한도 초과(429): 잠시 후 다시 실행하세요. ({_detail(exc)})") from exc
    except anthropic.BadRequestError as exc:
        hint = " --temperature는 현재 모델/API 버전에서 지원되지 않으니 빼고 실행하세요." \
            if settings.temperature is not None else ""
        raise AIError(f"잘못된 요청(400):{hint} ({_detail(exc)})") from exc
    except anthropic.APIStatusError as exc:
        raise AIError(f"API 서버 오류({exc.status_code}): 잠시 후 다시 실행하세요. ({_detail(exc)})") from exc
    except anthropic.APITimeoutError as exc:
        raise AIError("응답 시간 초과: 네트워크 상태를 확인하거나 --max-tokens를 줄여 보세요.") from exc
    except anthropic.APIConnectionError as exc:
        raise AIError(f"네트워크 오류: API 서버에 연결할 수 없습니다. ({exc})") from exc

    if response.stop_reason == "refusal":
        raise AIError("모델이 요청을 거절했습니다(refusal). diff 내용을 확인하거나 --safe-mode를 사용하세요.")
    text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
    if not text.strip():
        raise AIError(f"AI 응답에 텍스트가 없습니다 (stop_reason={response.stop_reason}).")
    if response.stop_reason == "max_tokens":
        print(f"[WARN] max_tokens({settings.max_tokens}) 한도에 도달해 응답이 잘렸을 수 있습니다.")
    return text


def _detail(exc) -> str:
    """SDK 예외에서 사람이 읽을 수 있는 원인 문자열을 꺼낸다."""
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        err = body.get("error", {})
        if isinstance(err, dict) and err.get("message"):
            return err["message"]
    return str(exc)
