# Dog Training Companion

A small command-line app that guides you through essential dog training exercises and tracks your sessions locally.

## Features
- Curated starter exercises with clear goals and step-by-step instructions.
- Session logging with duration, mood, treats used, and personal notes.
- Progress summaries that show per-exercise consistency and total time invested.
- Quick training tips to keep sessions fun and effective.

## Installation
The app only depends on the Python standard library. Clone the repository and run commands with Python 3.11+:

```bash
python -m dog_training_app.app --help
```

For convenience you can create an alias:

```bash
alias dog-trainer="python -m dog_training_app.app"
```

## Usage
List available exercises:

```bash
python -m dog_training_app.app exercises --details
```

Record a training session:

```bash
python -m dog_training_app.app start "Sit" --duration 5 --treats 3 --mood calm --notes "Held focus indoors"
```

Review your progress:

```bash
python -m dog_training_app.app progress
```

Show quick tips:

```bash
python -m dog_training_app.app tips
```

Data is stored by default in `~/.dog_training_app/training_data.json`. You can override the location with `--data-file` on any command.

## Development
Run tests with pytest:

```bash
pytest
```
