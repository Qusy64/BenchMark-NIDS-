import ast
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
SPLIT_DIR = NOTEBOOKS / "split"


SPECS = {
    "01_CICIDS2017_PyTorch.ipynb": {
        "prefix": "CICIDS2017_PyTorch",
        "framework": "pytorch",
        "cse": False,
        "models": {
            "MLP": {
                "definition": "MLPBaseline",
                "builder": "MLPBaseline",
                "name": '"MLP baseline"',
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "MLP baseline",
            },
            "CNN": {
                "definition": "CNNBaseline",
                "builder": "CNNBaseline",
                "name": '"CNN baseline"',
                "epochs": 3,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CNN baseline",
            },
            "INSOMNIA": {
                "definition": "FrameworkStyleMLP",
                "builder": "FrameworkStyleMLP",
                "name": "FRAMEWORK_STYLE_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "INSOMNIA-style MLP",
            },
            "ImprovedMLP": {
                "definition": "ImprovedMLP",
                "builder": "ImprovedMLP",
                "name": "IMPROVED_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=7e-4, use_class_weights=True, threshold_tuning=True, early_stopping=True, scheduler_enabled=True",
                "title": "Improved MLP",
            },
        },
    },
    "02_CICIDS2017_TensorFlow.ipynb": {
        "prefix": "CICIDS2017_TensorFlow",
        "framework": "tensorflow",
        "cse": False,
        "models": {
            "MLP": {
                "definition": "build_mlp_baseline",
                "builder": "build_mlp_baseline",
                "name": '"MLP baseline"',
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "MLP baseline",
            },
            "CNN": {
                "definition": "build_cnn_baseline",
                "builder": "build_cnn_baseline",
                "name": '"CNN baseline"',
                "epochs": 3,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CNN baseline",
            },
            "INSOMNIA": {
                "definition": "build_framework_style_mlp",
                "builder": "build_framework_style_mlp",
                "name": "FRAMEWORK_STYLE_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "INSOMNIA-style MLP",
            },
            "ImprovedMLP": {
                "definition": "build_improved_mlp",
                "builder": "build_improved_mlp",
                "name": "IMPROVED_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=7e-4, use_class_weights=True, threshold_tuning=True, early_stopping=True, scheduler_enabled=True",
                "title": "Improved MLP",
            },
        },
    },
    "03_CSE_CIC_IDS2018_PyTorch.ipynb": {
        "prefix": "CSE_CIC_IDS2018_PyTorch",
        "framework": "pytorch",
        "cse": True,
        "models": {
            "MLP": {
                "definition": "MLPBaseline",
                "builder": "MLPBaseline",
                "name": '"MLP baseline"',
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "MLP baseline",
            },
            "CNN": {
                "definition": "CNNBaseline",
                "builder": "CNNBaseline",
                "name": '"CNN baseline"',
                "epochs": 3,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CNN baseline",
            },
            "CADE": {
                "definition": "FrameworkStyleMLP",
                "builder": "FrameworkStyleMLP",
                "name": "FRAMEWORK_STYLE_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CADE-style MLP",
            },
            "ImprovedMLP": {
                "definition": "ImprovedMLP",
                "builder": "ImprovedMLP",
                "name": "IMPROVED_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=7e-4, use_class_weights=True, threshold_tuning=True, early_stopping=True, scheduler_enabled=True",
                "title": "Improved MLP",
            },
        },
    },
    "04_CSE_CIC_IDS2018_TensorFlow.ipynb": {
        "prefix": "CSE_CIC_IDS2018_TensorFlow",
        "framework": "tensorflow",
        "cse": True,
        "models": {
            "MLP": {
                "definition": "build_mlp_baseline",
                "builder": "build_mlp_baseline",
                "name": '"MLP baseline"',
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "MLP baseline",
            },
            "CNN": {
                "definition": "build_cnn_baseline",
                "builder": "build_cnn_baseline",
                "name": '"CNN baseline"',
                "epochs": 3,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CNN baseline",
            },
            "CADE": {
                "definition": "build_framework_style_mlp",
                "builder": "build_framework_style_mlp",
                "name": "FRAMEWORK_STYLE_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=1e-3",
                "title": "CADE-style MLP",
            },
            "ImprovedMLP": {
                "definition": "build_improved_mlp",
                "builder": "build_improved_mlp",
                "name": "IMPROVED_MODEL_NAME",
                "epochs": 5,
                "batch_size": 512,
                "kwargs": "lr=7e-4, use_class_weights=True, threshold_tuning=True, early_stopping=True, scheduler_enabled=True",
                "title": "Improved MLP",
            },
        },
    },
}


def cell_source(cell):
    return "".join(cell.get("source", []))


def with_source(cell, source):
    updated = copy.deepcopy(cell)
    updated["source"] = source.splitlines(keepends=True)
    updated["outputs"] = []
    updated["execution_count"] = None
    return updated


def clear_outputs(cell):
    updated = copy.deepcopy(cell)
    if updated.get("cell_type") == "code":
        updated["outputs"] = []
        updated["execution_count"] = None
    return updated


def prune_definition_cell(cell, definition_name):
    source = cell_source(cell)
    tree = ast.parse(source)
    chunks = []
    for node in tree.body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == definition_name:
            chunks.append(ast.get_source_segment(source, node))
    if not chunks:
        raise ValueError(f"Definition {definition_name!r} not found")
    return with_source(cell, "\n\n".join(chunks) + "\n")


def patch_constants(source, new_filename):
    lines = []
    for line in source.splitlines():
        if line.startswith("NOTEBOOK_FILENAME ="):
            lines.append(f'NOTEBOOK_FILENAME = "{new_filename}"')
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def patch_kaggle_working_dirs(source):
    legacy_root = "/" + "content"
    return (
        source.replace(f'DATA_DIR = Path("{legacy_root}/data")', 'DATA_DIR = Path("/kaggle/working/data")')
        .replace(f'RESULTS_DIR = Path("{legacy_root}/results")', 'RESULTS_DIR = Path("/kaggle/working/results")')
    )


def patch_run_helper(source, framework):
    source = source.replace("epochs: int = 10", "epochs: int = 5")
    source = source.replace("batch_size: int = 64", "batch_size: int = 512")
    append_helpers = """

import gc

def append_result_row(row: dict, csv_path: Path) -> None:
    row_to_save = row.copy()
    for col in ["confusion_matrix", "classification_report"]:
        if col in row_to_save:
            row_to_save[col] = json.dumps(row_to_save[col])
    pd.DataFrame([row_to_save]).to_csv(
        csv_path,
        mode="a",
        index=False,
        header=not csv_path.exists(),
    )

def cleanup_after_run() -> None:
    gc.collect()
"""
    if framework == "pytorch":
        append_helpers += "    torch.cuda.empty_cache()\n"
        train_name = "train_torch_model"
    else:
        append_helpers += "    tf.keras.backend.clear_session()\n"
        train_name = "train_tf_model"
    old = f"""            rows.append(
                {train_name}(
                    model_builder=model_builder,
                    model_name=model_name,
                    training_seed=training_seed,
                    weight_init_name=weight_init_name,
                    weight_init_tuple=weight_init_tuple,
                    **train_kwargs,
                )
            )"""
    new = f"""            row = {train_name}(
                model_builder=model_builder,
                model_name=model_name,
                training_seed=training_seed,
                weight_init_name=weight_init_name,
                weight_init_tuple=weight_init_tuple,
                **train_kwargs,
            )
            rows.append(row)
            append_result_row(row, RESULTS_CSV_PATH)
            cleanup_after_run()"""
    if old not in source:
        raise ValueError("Could not patch run_model_experiment append block")
    source = source.replace(old, new)
    marker = "\ndef run_model_experiment("
    source = source.replace(marker, append_helpers + marker)
    return source


def execution_cell(model, cse):
    args = (
        f"{model['builder']}, {model['name']}, "
        f"epochs={model['epochs']}, batch_size={model['batch_size']}, {model['kwargs']}"
    )
    if cse:
        return f"""if RESULTS_CSV_PATH.exists():
    RESULTS_CSV_PATH.unlink()

model_results_frames = []
for held_out_attack in HELD_OUT_ATTACKS:
    print(f"\\n=== Held-out attack: {{held_out_attack}} ===")
    prepare_cse_held_out_experiment(held_out_attack)
    result_frame = run_model_experiment({args})
    print("Per-attack aggregate results:")
    display(aggregate_results(result_frame))
    model_results_frames.append(result_frame)

per_run_results = pd.concat(model_results_frames, ignore_index=True)
per_run_results.head()
"""
    return f"""if RESULTS_CSV_PATH.exists():
    RESULTS_CSV_PATH.unlink()

per_run_results = run_model_experiment({args})
per_run_results.head()
"""


def result_paths_cell(output_name):
    return f"""RESULTS_CSV_PATH = RESULTS_DIR / "{output_name}_results.csv"
AGGREGATED_RESULTS_CSV_PATH = RESULTS_DIR / "{output_name}_aggregated_results.csv"

print("Per-run results CSV:", RESULTS_CSV_PATH)
print("Aggregated results CSV:", AGGREGATED_RESULTS_CSV_PATH)
"""


def aggregate_cell():
    return """aggregated_results = aggregate_results(per_run_results)
overall_comparison_table = aggregated_results[
    aggregated_results["held_out_attack"].eq("OVERALL")
].copy() if "held_out_attack" in aggregated_results.columns else aggregated_results.copy()

aggregated_results.to_csv(AGGREGATED_RESULTS_CSV_PATH, index=False)
print("Saved aggregated results to:", AGGREGATED_RESULTS_CSV_PATH)
"""


def comparison_cell():
    return """comparison_table = overall_comparison_table.copy()
print("Final comparison table:")
display(comparison_table)
print("=== DONE ===")
"""


def markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code_like(template_cell, source):
    return with_source(template_cell, source)


def build_notebook(source_path, spec, model_key, model):
    nb = json.loads(source_path.read_text(encoding="utf-8"))
    output_name = f"{spec['prefix']}_{model_key}"
    new_filename = f"{output_name}.ipynb"
    cells = [clear_outputs(c) for c in nb["cells"][:24]]

    cells[0] = markdown(f"# {output_name}\\n\\nSplit Kaggle notebook generated from `{source_path.name}`. This notebook runs only the {model['title']} model.\\n")
    cells[4] = with_source(cells[4], patch_constants(cell_source(cells[4]), new_filename))
    cells[7] = markdown("## 4. Create data and Kaggle results folders\\n\\nGenerated CSV results are written to `/kaggle/working/results/`.\\n")
    cells[8] = with_source(cells[8], patch_kaggle_working_dirs(cell_source(cells[8])))
    cells.insert(9, code_like(cells[8], result_paths_cell(output_name)))
    # Inserting a cell shifts original index 21 to 22 and original model definitions to 24.
    cells[22] = with_source(cells[22], patch_run_helper(cell_source(cells[22]), spec["framework"]))
    cells[24] = prune_definition_cell(cells[24], model["definition"])

    template_code_cell = nb["cells"][25]
    cells.extend(
        [
            markdown(f"## Train and evaluate {model['title']}\\n\\nThis split notebook executes only this model with the configured seed and initialization grid.\\n"),
            code_like(template_code_cell, execution_cell(model, spec["cse"])),
            markdown("## Aggregate and save results\\n\\nThe per-run CSV is appended after every seed and initialization run. The aggregated CSV is saved at the end.\\n"),
            code_like(template_code_cell, aggregate_cell()),
            markdown("## Final comparison table\\n"),
            code_like(template_code_cell, comparison_cell()),
        ]
    )
    new_nb = copy.deepcopy(nb)
    new_nb["cells"] = cells
    return new_filename, new_nb


def main():
    SPLIT_DIR.mkdir(parents=True, exist_ok=True)
    created = []
    for filename, spec in SPECS.items():
        source_path = NOTEBOOKS / filename
        for model_key, model in spec["models"].items():
            new_filename, new_nb = build_notebook(source_path, spec, model_key, model)
            out_path = SPLIT_DIR / new_filename
            out_path.write_text(json.dumps(new_nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            created.append(out_path.relative_to(ROOT))
    print("Created notebooks:")
    for path in created:
        print(path)


if __name__ == "__main__":
    main()
