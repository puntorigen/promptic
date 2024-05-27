# promptic

`promptic` is a lightweight, decorator-based Python library that simplifies the process of interacting with large language models (LLMs) using `litellm`. With `promptic`, you can effortlessly create prompts, handle input arguments, and receive structured outputs from LLMs, all in under 100 lines of code.

## Features

- **Decorator-based API**: Easily define prompts using function docstrings and decorate them with `@promptic`.
- **Argument interpolation**: Automatically interpolate function arguments into the prompt using `{argument_name}` placeholders.
- **Pydantic model support**: Specify the expected output structure using Pydantic models, and `promptic` will ensure the LLM's response conforms to the defined schema.
- **Streaming support**: Receive LLM responses in real-time by setting `stream=True` when calling the decorated function.
- **Simplified LLM interaction**: No need to remember the exact shape of the OpenAPI response object or other LLM-specific details. `promptic` abstracts away the complexities, allowing you to focus on defining prompts and receiving structured outputs.

## Installation

```bash
pip install promptic
```

## Usage

Here are a few examples of how to use `promptic`:

### Simple Prompt

```python
from promptic import promptic

@promptic
def us_president(year):
    """Who was the President of the United States in {year}?"""

print(us_president(2000))
# The President of the United States in 2000 was Bill Clinton until January 20th, when George W. Bush was inaugurated as the 43rd President.
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel
from promptic import promptic

class Capital(BaseModel):
    country: str
    capital: str

@promptic
def get_capital(country) -> Capital:
    """What's the capital of {country}?"""

print(get_capital("France"))
# country='France' capital='Paris'
```

### Streaming Response

```python
from promptic import promptic

@promptic(
    # keyword args are passed to litellm.completion
    stream=True,
)
def haiku(subject: str, adjective: str, verb: str) -> str:
    """Write a haiku about {subject} that is {adjective} and {verb}."""

print("".join(haiku("nature", "beautiful", "inspires")))
# Vibrant green leaves sway
# Birds sing melodies of joy
# Nature's perfect dance
```

## Why promptic?

`promptic` is designed to be simple, functional, and robust, providing exactly what you need 90% of the time when working with LLMs. It eliminates the need to remember the specific shapes of OpenAPI response objects or other LLM-specific details, allowing you to focus on creating prompts and receiving structured outputs.

With its legible and concise codebase, `promptic` is easy to understand and extend. It leverages the power of `litellm` under the hood, ensuring compatibility with a wide range of LLMs.

## License

`promptic` is open-source software licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
