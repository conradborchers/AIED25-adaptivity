# AIED25-adaptivity

Code repository for AIED25 paper: Can Large Language Models Match Tutoring System Adaptivity? A Benchmarking Study

## Repo structure
```
.
├── README.md
├── experiment.ipynb                           # main experiment procedure source code
├── llm_recommendation_proxy                   # python package for prompting various LLMs hosted on OpenAI API and AWS
│   ├── __init__.py
│   ├── llm_client
│   │   ├── __init__.py
│   │   ├── abstract_llm_client.py
│   │   ├── aws_bedrock_llm_client.py
│   │   ├── inference_settings.py
│   │   └── openai_llm_client.py
│   ├── prompt_formatter.py                    # demonstrates LLM prompt template used in this study
│   ├── router.py
│   ├── tutor_settings
│   │   ├── __init__.py
│   │   ├── few_shot_example_statements.py
│   │   ├── knowledge_components.py
│   │   ├── persona_statements.py
│   │   └── tutor_id.py
│   └── util.py
├── openai.key                                 # stores OpenAI API key, please supply your key here to run prompting
├── pyproject.toml
└── requirements.txt
```

## Getting started to run our code

Please have a Python environment ready, and any Python 3.8+ version should suffice. Please run `pip install -r requirements.txt` to install necessary dependencies. Run `pip install .` to install the local `llm_recommendation_proxy` package. If you wish to execute code in the jupyter notebook, install `ipykernel` with `pip install ipykernel`.

If you wish to use our package to prompt LLMs:

- Supply and save your OpenAI API key in the `openai.key` file.
- [Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and configure `aws-cli` on your machine with AWS API keys in order to gain access to Llama models hosted on AWS.
