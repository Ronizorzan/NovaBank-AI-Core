from __future__ import annotations

import argparse
import asyncio
import csv
from pathlib import Path
from statistics import mean, median
from time import perf_counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from app import doc_vectorstore, faq_engine, llm_rag, prompt_template


DEFAULT_FAQ_QUERIES = [
    "Como alterar a senha de acesso do aplicativo?",
    "Esqueci minha senha do app. O que devo fazer para recuperar?",
    "Como ativar a autenticação de dois fatores para maior segurança?",
    "Qual o limite diário padrão para transferências (TED/Pix)?",
    "Como configurar alertas e notificações de transações na minha conta?",
    "O que é o PIX e como posso começar a usar no NovaBank?",
    "Como fazer portabilidade de salário para o NovaBank?",
    "Onde encontro meu Informe de Rendimentos para Declaração de Imposto de Renda?",
]


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    idx = max(0, min(len(ordered) - 1, int((pct / 100) * len(ordered))))
    return ordered[idx]


def benchmark_cache_hits(queries: list[str], iterations: int = 20) -> pd.DataFrame:
    rows: list[dict] = []
    for query in queries:
        values: list[float] = []
        for _ in range(iterations):
            start = perf_counter()
            answer = faq_engine.check_cache(query)
            elapsed_ms = (perf_counter() - start) * 1000
            values.append(elapsed_ms)
            if answer is None:
                raise ValueError(f"Consulta sem hit no FAQ: {query}")
        rows.append(
            {
                "query": query,
                "avg_ms": round(mean(values), 2),
                "median_ms": round(median(values), 2),
                "p95_ms": round(_percentile(values, 95), 2),
                "min_ms": round(min(values), 2),
                "max_ms": round(max(values), 2),
            }
        )
    return pd.DataFrame(rows)


async def _rag_fallback_latency(query: str) -> float:
    retriever = doc_vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6, "lambda_mult": 0.10, "fetch_k": 15},
    )

    start = perf_counter()
    docs = await asyncio.to_thread(retriever.invoke, query)
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = prompt_template.format_messages(
        context=context,
        chat_history=[],
        secure_query=query,
    )
    await asyncio.to_thread(llm_rag.invoke, messages)
    return (perf_counter() - start) * 1000


async def benchmark_rag_fallback(queries: list[str], iterations: int = 3) -> pd.DataFrame:
    rows: list[dict] = []
    for query in queries:
        values: list[float] = []
        for _ in range(iterations):
            values.append(await _rag_fallback_latency(query))
        rows.append(
            {
                "query": query,
                "avg_ms": round(mean(values), 2),
                "median_ms": round(median(values), 2),
                "p95_ms": round(_percentile(values, 95), 2),
                "min_ms": round(min(values), 2),
                "max_ms": round(max(values), 2),
            }
        )
    return pd.DataFrame(rows)


def summarize_results(cache_df: pd.DataFrame, rag_df: pd.DataFrame) -> pd.DataFrame:
    cache_avg = cache_df["avg_ms"].mean()
    cache_p95 = cache_df["p95_ms"].mean()
    rag_avg = rag_df["avg_ms"].mean()
    rag_p95 = rag_df["p95_ms"].mean()

    delta_avg = rag_avg - cache_avg
    speedup = rag_avg / cache_avg if cache_avg > 0 else float("inf")
    p95_gain = rag_p95 - cache_p95
    return pd.DataFrame(
        [
            {
                "scenario": "Cache semântico (FAQ hit)",
                "avg_ms": round(cache_avg, 2),
                "p95_ms": round(cache_p95, 2),
                "improvement_vs_rag": "base",
            },
            {
                "scenario": "RAG completo (fallback)",
                "avg_ms": round(rag_avg, 2),
                "p95_ms": round(rag_p95, 2),
                "improvement_vs_rag": "base",
            },
            {
                "scenario": "Ganhos médios",
                "avg_ms": round(delta_avg, 2),
                "p95_ms": round(p95_gain, 2),
                "improvement_vs_rag": f"{speedup:.1f}x mais rápido",
            },
        ]
    )


def save_csv(output_dir: Path, df: pd.DataFrame, filename: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    df.to_csv(path, index=False)
    return path


def render_chart(cache_df: pd.DataFrame, rag_df: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 5))

    labels = ["FAQ hit", "RAG fallback"]
    avg_values = [cache_df["avg_ms"].mean(), rag_df["avg_ms"].mean()]
    p95_values = [cache_df["p95_ms"].mean(), rag_df["p95_ms"].mean()]

    x = range(len(labels))
    ax.bar(x, avg_values, width=0.45, color=["#16a34a", "#f59e0b"], alpha=0.9, label="Tempo médio")
    ax.plot(x, p95_values, color="#1d4ed8", marker="o", linewidth=2.5, label="P95")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Tempo (ms)")
    ax.set_title("Impacto do cache semântico no tempo de resposta")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend()

    for xi, yi in zip(x, avg_values):
        ax.text(xi, yi + max(avg_values) * 0.04, f"{yi:.0f} ms", ha="center", va="bottom", fontsize=9)

    path = output_dir / "semantic_cache_benchmark.png"
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def write_markdown_report(output_dir: Path, cache_df: pd.DataFrame, rag_df: pd.DataFrame, speedup: float) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = [
        "## Benchmark do cache semântico",
        "",
        f"- Média de resposta com cache semântico: {cache_df['avg_ms'].mean():.1f} ms",
        f"- Média de resposta sem cache (RAG completo): {rag_df['avg_ms'].mean():.1f} ms",
        f"- Aumento de velocidade: {speedup:.1f}x",
        f"- Redução do tempo médio: {((rag_df['avg_ms'].mean() - cache_df['avg_ms'].mean()) / rag_df['avg_ms'].mean()) * 100:.1f}%",
        "",
        "| Cenário | Tempo médio (ms) | P95 (ms) |",
        "|---|---:|---:|",
        f"| Cache semântico (FAQ hit) | {cache_df['avg_ms'].mean():.1f} | {cache_df['p95_ms'].mean():.1f} |",
        f"| RAG completo (fallback) | {rag_df['avg_ms'].mean():.1f} | {rag_df['p95_ms'].mean():.1f} |",
        "",
        "![Benchmark de cache semântico](semantic_cache_benchmark.png)",
        "",
        "### Interpretação para stakeholders",
        "",
        "- O cache semântico elimina a necessidade de executar busca e geração no LLM para perguntas recorrentes.",
        "- Em cenários de FAQ, a latência cai de centenas de ms para dezenas de ms, melhorando a experiência do cliente e reduzindo custo operacional.",
        "- Isso aumenta escalabilidade e melhora a previsibilidade da operação em picos de demanda.",
    ]
    path = output_dir / "semantic_cache_benchmark.md"
    path.write_text("\n".join(summary), encoding="utf-8")
    return path


async def main():
    parser = argparse.ArgumentParser(description="Benchmark do cache semântico da API NovaBank")
    parser.add_argument("--queries", nargs="*", default=DEFAULT_FAQ_QUERIES, help="Perguntas usadas para medir o hit do FAQ")
    parser.add_argument("--cache-iterations", type=int, default=20, help="Número de repetições para o hit do FAQ")
    parser.add_argument("--fallback-iterations", type=int, default=3, help="Número de repetições para o fallback via RAG")
    parser.add_argument("--output-dir", type=str, default="reports", help="Diretório para salvar CSV, PNG e markdown")
    args = parser.parse_args()

    cache_df = benchmark_cache_hits(args.queries, iterations=args.cache_iterations)
    rag_df = await benchmark_rag_fallback(args.queries, iterations=args.fallback_iterations)

    output_dir = Path(args.output_dir)
    cache_csv = save_csv(output_dir, cache_df, "semantic_cache_hits.csv")
    rag_csv = save_csv(output_dir, rag_df, "semantic_cache_rag_fallback.csv")
    chart_path = render_chart(cache_df, rag_df, output_dir)

    cache_avg = cache_df["avg_ms"].mean()
    rag_avg = rag_df["avg_ms"].mean()
    speedup = rag_avg / cache_avg if cache_avg > 0 else float("inf")
    report_path = write_markdown_report(output_dir, cache_df, rag_df, speedup)

    print("\n=== Benchmark do cache semântico ===")
    print(f"Cache semântico (FAQ hit): {cache_avg:.2f} ms")
    print(f"RAG completo (fallback): {rag_avg:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Redução de tempo: {((rag_avg - cache_avg) / rag_avg * 100):.1f}%")
    print(f"\nArquivos gerados: {cache_csv}, {rag_csv}, {chart_path}, {report_path}")

    print("\nTabela em markdown:")
    print("| Cenário | Tempo médio (ms) | P95 (ms) |")
    print("|---|---:|---:|")
    print(f"| Cache semântico (FAQ hit) | {cache_df['avg_ms'].mean():.1f} | {cache_df['p95_ms'].mean():.1f} |")
    print(f"| RAG completo (fallback) | {rag_df['avg_ms'].mean():.1f} | {rag_df['p95_ms'].mean():.1f} |")


if __name__ == "__main__":
    asyncio.run(main())
