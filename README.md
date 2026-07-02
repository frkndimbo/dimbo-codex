# Dimbo Codex

Konfigurasi Codex pribadi milik `frkndimbo`, dibuat supaya bisa diclone lalu diterapkan ke konfigurasi lokal Codex di Windows, macOS, atau Linux.

## Isi Repo

- `AGENTS.md`: instruksi global Codex.
- `RTK.md`, `WORKFLOW.md`, `VERIFY.md`, `SKILLS_POLICY.md`: aturan kerja tambahan.
- `SPEC_DESIGN.md`, `EVAL_DESIGN.md`, `DIFF_REVIEW.md`, `TOKENOMICS.md`: guardrail untuk pekerjaan non-trivial.
- `skills/`: skill aktif yang aman untuk dibawa.
- `config/config.toml.template`: template config tanpa rahasia.
- `scripts/install.sh`: installer macOS/Linux.
- `scripts/install.ps1`: installer Windows PowerShell.

File rahasia seperti `auth.json`, `config.toml` asli, database sqlite, log, history, session, cache, dan memory lokal tidak ikut dicommit.

## Install di macOS atau Linux

```bash
git clone https://github.com/frkndimbo/dimbo-codex.git
cd dimbo-codex
sh scripts/install.sh --dry-run
sh scripts/install.sh
```

Default installer:

- membuat folder `~/.codex` jika belum ada;
- backup file lama ke `~/.codex/backups/<timestamp>`;
- menyalin instruksi, policy docs, dan skill ke `~/.codex`;
- menyalin `config/config.toml.template` ke `~/.codex/config.toml.template`;
- tidak menimpa `~/.codex/config.toml` yang sudah ada.

Untuk mesin baru yang belum punya `config.toml`:

```bash
sh scripts/install.sh --force-config
```

## Install di Windows

Buka PowerShell di folder tujuan, lalu jalankan:

```powershell
git clone https://github.com/frkndimbo/dimbo-codex.git
cd dimbo-codex
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

Untuk mesin baru yang belum punya `config.toml`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -ForceConfig
```

## Setelah Install

Jalankan dari folder mana pun:

```bash
codex --version
```

Lalu buka session Codex baru. Instruksi global akan dibaca dari `~/.codex/AGENTS.md`.

## Ponytail

Plugin Ponytail tidak diaktifkan otomatis di template ini. Aktifkan manual hanya saat dibutuhkan lewat perintah/skill Ponytail dari Codex.

## Update

```bash
cd dimbo-codex
git pull
sh scripts/install.sh
```

Windows:

```powershell
cd dimbo-codex
git pull
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

## Rollback

Ambil file lama dari backup terakhir:

```bash
ls ~/.codex/backups
```

Salin kembali file yang diperlukan dari `~/.codex/backups/<timestamp>`.

