# fogo-interface

Interface gráfica da propagação de incêndios (PIBITI, IFG Câmpus Inhumas).

## Gerar a simulação de mentira

```
python -m venv .venv
.venv\Scripts\activate      # Linux: source .venv/bin/activate
python gera_mock.py
```

Isso cria `sim-001.json`, `sim-002.json`, `sim-003.json` (ventos diferentes) e o `simulacao.json`.
