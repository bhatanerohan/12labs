# 12labs — Claude Code Context

## Project
Twelve Labs video understanding hackathon project.
Repo: git@github.com:bhatanerohan/12labs.git

## Stack
- Python 3.11, uv package manager
- `twelvelabs` SDK for video indexing, search, and generation
- `python-dotenv` for env vars

## Twelve Labs SDK Patterns
```python
from twelvelabs import TwelveLabs
client = TwelveLabs(api_key=os.getenv("TWELVE_LABS_API_KEY"))

client.indexes.list()                          # list indexes
client.indexes.create(name="...", models=[])   # create index
client.search.query(index_id, query)           # search videos
client.generate.text(video_id, prompt)         # generate text from video
```

## Running Code
```bash
uv run python main.py       # run a script
uv add <package>            # add a dependency
```

## Git Workflow
- Always work on a feature branch: `git checkout -b feature/<description>`
- Never push directly to `main`
- Stage specific files only — never `git add -A` or `git add .`
- Never commit `.env`
- Commit message format: imperative, e.g. "add video search module"
- After pushing, report the branch name and commit hash
