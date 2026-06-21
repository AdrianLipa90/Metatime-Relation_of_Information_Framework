#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


NOISE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
}


def is_noise(path: Path) -> bool:
    name = path.name
    if "__pycache__" in path.parts:
        return True
    if name == ".DS_Store" or name == "Thumbs.db":
        return True
    if name.endswith(".synctex.gz"):
        return True
    if any(name.endswith(suf) for suf in {".tmp", ".bak", ".backup"}):
        return True
    if path.suffix.lower() in NOISE_SUFFIXES:
        return True
    if ".ipynb_checkpoints" in path.parts:
        return True
    return False


class Importer:
    def __init__(self, src_root: Path, repo_root: Path) -> None:
        self.src_root = src_root
        self.repo_root = repo_root
        self.manifest_path = repo_root / "CLEAN_IMPORT_MANIFEST.json"
        self.entries: list[dict[str, str]] = []
        if self.manifest_path.exists():
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            self.entries = data.get("entries", [])

    def save_manifest(self) -> None:
        payload = {
            "source_root": str(self.src_root),
            "repository_root": str(self.repo_root),
            "entries": sorted(
                self.entries,
                key=lambda item: (
                    item.get("old_path", ""),
                    item.get("new_path", ""),
                    item.get("status", ""),
                ),
            ),
        }
        self.manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add_entry(
        self,
        old_path: Path,
        status: str,
        new_path: Path | None = None,
        dropped_reason: str | None = None,
        document_class: str | None = None,
    ) -> None:
        entry = {
            "old_path": str(old_path.relative_to(self.src_root)),
            "status": status,
        }
        if new_path is not None:
            entry["new_path"] = str(new_path.relative_to(self.repo_root))
        if dropped_reason is not None:
            entry["dropped_reason"] = dropped_reason
        if document_class is not None:
            entry["document_class"] = document_class
        self.entries.append(entry)

    def doc_class(self, src: Path, dst: Path) -> str | None:
        suffix = src.suffix.lower()
        if suffix == ".tex":
            return "source"
        if suffix == ".pdf":
            return "rendered-output"
        if suffix == ".md":
            if "validation" in dst.parts:
                return "validation-report"
            if "archive" in dst.parts:
                return "archive-record"
            return "explanatory-doc"
        if "archive" in dst.parts:
            return "archive-record"
        return None

    def copy_file(self, src: Path, dst: Path) -> None:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        self.add_entry(src, "moved", dst, document_class=self.doc_class(src, dst))

    def drop(self, src: Path, reason: str) -> None:
        self.add_entry(src, "dropped", dropped_reason=reason)

    def import_tree(self, src_dir: Path, dst_dir: Path) -> None:
        for path in sorted(src_dir.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(src_dir)
            if is_noise(path):
                self.drop(path, "build-noise")
                continue
            self.copy_file(path, dst_dir / rel)

    def import_core(self) -> None:
        root = self.src_root / "00_original_metatime" / "Metatime-main"
        self.copy_file(root / "LICENSE", self.repo_root / "LICENSE")
        self.drop(root / "LICENSE.txt", "duplicate")
        self.copy_file(root / "README.md", self.repo_root / "docs/overview/original_metatime_readme.md")
        self.copy_file(root / "AGENT5.md", self.repo_root / "docs/overview/AGENT5.md")
        self.copy_file(root / "AGENT6.md", self.repo_root / "docs/overview/AGENT6.md")
        self.copy_file(root / "MetaTheory_260218_073120.txt", self.repo_root / "theory/metatime/MetaTheory_260218_073120.txt")
        self.copy_file(root / "Metatime framework summary.pdf", self.repo_root / "docs/framework/Metatime_framework_summary.pdf")
        self.copy_file(root / "file_0000000074ac720aa48d13b55bb80b5c.png", self.repo_root / "docs/figures/original_metatime/file_0000000074ac720aa48d13b55bb80b5c.png")
        self.copy_file(root / "cielnofft.py", self.repo_root / "core/src/cielnofft.py")
        self.copy_file(root / ".github/FUNDING.yml", self.repo_root / ".github/FUNDING.yml")
        self.import_tree(root / "NoParamSM", self.repo_root / "core/src/NoParamSM")
        self.import_tree(root / "ResChem", self.repo_root / "core/src/ResChem")
        self.import_tree(root / "simulations", self.repo_root / "core/scripts/simulations")
        self.import_tree(root / "data", self.repo_root / "core/data_minimal/original_metatime_data")
        self.import_tree(root / "registries", self.repo_root / "core/configs")
        self.import_tree(root / "reports", self.repo_root / "docs/framework/original_reports")
        self.import_tree(root / "documents", self.repo_root / "docs/publications/original_metatime_documents")

    def import_docs_theory(self) -> None:
        self.copy_file(self.src_root / "README.md", self.repo_root / "docs/overview/source_bundle_readme.md")
        self.copy_file(self.src_root / "CURRENT_STATUS.md", self.repo_root / "docs/overview/source_bundle_current_status.md")
        for extra in ["HYGIENE_REPORT_v4_1.md", "HYGIENE_REPORT_v4_2.md"]:
            src = self.src_root / extra
            if src.exists():
                self.copy_file(src, self.repo_root / "docs/overview" / extra)
        self.import_tree(
            self.src_root / "01_foundational_formal_notes",
            self.repo_root / "theory/metatime/foundational_formal_notes",
        )

    def import_archive(self) -> None:
        for path in sorted(self.src_root.iterdir()):
            if not path.is_dir():
                continue
            name = path.name
            if name in {"00_original_metatime", "01_foundational_formal_notes", "90_manifests", "99_validation"}:
                continue
            if name[:2].isdigit() or name.startswith("60B_"):
                self.import_tree(path, self.repo_root / "archive/lineage" / name)

    def import_validation(self) -> None:
        manifests = self.src_root / "90_manifests"
        for path in sorted(manifests.rglob("*")):
            if path.is_dir():
                continue
            if is_noise(path):
                self.drop(path, "build-noise")
                continue
            self.copy_file(path, self.repo_root / "validation/manifests" / path.relative_to(manifests))

        reports = self.src_root / "99_validation"
        for path in sorted(reports.rglob("*")):
            if path.is_dir():
                continue
            if is_noise(path):
                self.drop(path, "build-noise")
                continue
            dest_base = self.repo_root / "validation/reports"
            if path.suffix.lower() == ".json":
                dest_base = self.repo_root / "validation/provenance"
            if "DEBT_REGISTER" in path.name:
                dest_base = self.repo_root / "validation/debt_register"
            self.copy_file(path, dest_base / path.name)

        debt63 = self.src_root / "63_master_debt_register_closure_queue_v6_3"
        for name in [
            "MASTER_DEBT_REGISTER_v6_3.json",
            "MASTER_DEBT_REGISTER_v6_3.md",
            "validate_v6_3_debt_register.py",
        ]:
            self.copy_file(debt63 / name, self.repo_root / "validation/debt_register" / name)

        debt69 = self.src_root / "69_sealed_charged_lepton_reconstruction_benchmark_v6_9"
        self.copy_file(
            debt69 / "data/MASTER_DEBT_REGISTER_DELTA_v6_9.json",
            self.repo_root / "validation/debt_register/MASTER_DEBT_REGISTER_DELTA_v6_9.json",
        )
        self.copy_file(
            debt69 / "scripts/validate_v6_9_sealed_charged_lepton_reconstruction.py",
            self.repo_root / "tools/validators/validate_v6_9_sealed_charged_lepton_reconstruction.py",
        )
        self.copy_file(
            debt69 / "schemas/SEALED_CHARGED_LEPTON_RECONSTRUCTION_BENCHMARK_SCHEMA_v6_9.json",
            self.repo_root / "validation/provenance/SEALED_CHARGED_LEPTON_RECONSTRUCTION_BENCHMARK_SCHEMA_v6_9.json",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument(
        "--phase",
        required=True,
        choices=["core", "docs_theory", "archive", "validation"],
    )
    args = parser.parse_args()

    importer = Importer(Path(args.source_root), Path(args.repo_root))
    getattr(importer, f"import_{args.phase}")()
    importer.save_manifest()


if __name__ == "__main__":
    main()
