## Project Structure

```
├── LICENSE
├── README.md
├── data
│   ├── data_temp
│   ├── ds1
│   ├── ds2
│   └── ds3
├── env_check.py
├── log
│   ├── ds1_model1_test.log
│   ├── ds1_model1_train.log
│   └── ds1_model1_val.log
├── model
└── output
    ├── ds1_model1.out
    └── ds1_model2.out
```

## Environment Configuration

- windows or linux
- cuda, cudnn, pytorch-gpu
- conda:
    - create new virtual Python environment
    - install required packages

```bash
conda create -n venv python=3.10
conda activate venv
pip install torch==2.0.1+cu117 -f https://download.pytorch.org/whl/torch_stable.html
```

## Model

Model details.

## Training & Validating & Testing

Process of model experiment.

## Visualization

Visualization of training process & model performance.

## Analysis

Analysis & Future work of experiment results.
