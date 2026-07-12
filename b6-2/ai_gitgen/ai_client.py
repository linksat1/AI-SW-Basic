"""Anthropic Claude API 연동. 공식 anthropic SDK만 사용한다."""

import os

import anthropic

from .errors import ApiCallError, NoApiKeyError

DEFAULT_MODEL = "claude-opus-4-8"
DEFAULT_MAX_TOKENS = 1024


def _resolve_api_key() -> str:
    # 과제 예시(AI_API_KEY)를 우선하고, 표준 ANTHROPIC_API_KEY도 허용한다.
    key = os.environ.get("AI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise NoApiKeyError()
    return key


def generate(system_prompt: str, user_prompt: str, model: str, max_tokens: int, temperature) -> str:
    """Claude API를 호출해 텍스트 응답을 반환한다.

    temperature가 None이면 요청에 포함하지 않는다 (Opus 4.7+/Sonnet 5 계열은
    비-기본값 temperature/top_p/top_k를 아예 거부하므로, 사용자가 명시적으로
    지정했을 때만 전달한다).
    """
    api_key = _resolve_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    kwargs = dict(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    if temperature is not None:
        kwargs["temperature"] = temperature

    try:
        response = client.messages.create(**kwargs)
    except anthropic.AuthenticationError as exc:
        raise ApiCallError(f"API 키 인증에 실패했습니다. 키 값을 다시 확인하세요. ({exc})") from exc
    except anthropic.RateLimitError as exc:
        raise ApiCallError(f"요청 한도를 초과했습니다. 잠시 후 다시 시도하세요. ({exc})") from exc
    except anthropic.BadRequestError as exc:
        msg = str(exc)
        if "temperature" in msg.lower():
            raise ApiCallError(
                f"모델 '{model}'은(는) temperature 옵션을 지원하지 않습니다. "
                f"-temperature 없이 다시 실행하거나 다른 모델을 지정하세요. ({exc})"
            ) from exc
        raise ApiCallError(f"잘못된 요청입니다: {exc}") from exc
    except anthropic.APIConnectionError as exc:
        raise ApiCallError(f"네트워크 연결에 실패했습니다: {exc}") from exc
    except anthropic.APIStatusError as exc:
        raise ApiCallError(f"API 오류 (status={exc.status_code}): {exc}") from exc

    if response.stop_reason == "refusal":
        raise ApiCallError("모델이 안전 정책상 이 요청에 대한 응답을 거부했습니다.")

    for block in response.content:
        if block.type == "text":
            return block.text

    raise ApiCallError("API 응답에 텍스트 블록이 없습니다.")
