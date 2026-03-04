# AI-CLI (Python Edition)

> 🌐 [English](README.md) | [中文](README.zh.md) | [日本語](README.ja.md) | **Deutsch**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** ist ein plattformübergreifender Terminal-Launcher zur Verwaltung mehrerer KI-Coding-Assistenten. Wechseln Sie nahtlos zwischen Tools wie Kiro CLI, Claude Code, Cursor Agent und mehr.

## ✨ Hauptfunktionen

### 🌍 Plattformübergreifende Unterstützung
- **Windows**: Native Unterstützung + WSL-Integration ✅ Vollständig getestet
- **Linux**: Vollständige Unterstützung für alle wichtigen Distributionen ⚠️ **Nicht vollständig getestet - es können Probleme auftreten**
- **macOS**: Unterstützung für Terminal.app und iTerm2 ⚠️ **Nicht vollständig getestet - es können Probleme auftreten**

### 🔄 Tiefe WSL-Integration
- Automatische WSL-Umgebungserkennung
- Automatische Windows ↔ WSL-Pfadkonvertierung
- WSL-Tools von Windows aus starten
- Windows-Tools von WSL aus starten

### 📁 Projektverwaltung
- **Baumstruktur**: Projekte in Ordnern organisieren
- **Git Worktree**: Automatische Erkennung und Auswahl von Git-Worktrees
- **Umgebungsvariablen**: Projektspezifische Umgebungsvariablen konfigurieren
- **Pfadnormalisierung**: Automatische Handhabung verschiedener Plattform-Pfadformate

### ⚡ Tool-Erkennung & Verwaltung
- **Asynchrone Erkennung**: Parallele Tool-Erkennung mit async/await
- **Intelligentes Caching**: Hintergrunderkennung mit Ergebnis-Caching
- **Ein-Klick-Installation**: Drücken Sie `I` zum Installieren fehlender Tools
- **Manuelle Aktualisierung**: Drücken Sie `R` zum Aktualisieren der Tool-Liste
- **Umgebungserkennung**: Automatische Erkennung von Windows, WSL, Linux, macOS

### 🎨 Benutzeroberfläche
- **Rich UI**: Schöne Terminal-Oberfläche mit Rich-Bibliothek
- **Tastaturnavigation**: Vollständige Tastenkombinationen-Unterstützung
- **Echtzeit-Feedback**: Anzeige von Tool-Erkennung und Installationsfortschritt
- **Theme-Unterstützung**: Anpassbare Farbthemen

### 🌐 Internationalisierung
- **Mehrsprachig**: Englisch, Chinesisch, Japanisch, Deutsch
- **Automatische Erkennung**: Automatische Auswahl basierend auf Systemsprache
- **Konfigurierbar**: Manuelle Sprachauswahl in Konfigurationsdatei oder CLI-Parameter

## 🚀 Schnellstart

### Installation

#### Methode 1: Installation von PyPI (Empfohlen)

```bash
# Mit pip
pip install ai-cli-launcher

# Oder mit pipx (isolierte Umgebung)
pipx install ai-cli-launcher
```

#### Methode 2: Ein-Zeilen-Installationsskript

**Windows**:
```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

**Linux/macOS**:
```bash
curl -fsSL https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.sh | bash
```

Das Skript führt automatisch aus:
- Überprüfung der Python-Installation (Python 3.8+ erforderlich)
- Installation von AI-CLI von PyPI
- Initialisierung der Konfiguration
- Erstellung einer Desktop-Verknüpfung (Windows)

#### Methode 3: Installation aus Quellcode (Für Entwickler)

```bash
# Repository klonen
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Im Entwicklungsmodus installieren
pip install -e ".[dev]"
```

### Konfiguration initialisieren

```bash
ai-cli --init
```

Dies erstellt eine Standard-Konfigurationsdatei mit gängigen KI-Tool-Konfigurationen.

### Ausführen

```bash
ai-cli
```

### Deinstallation

**Vollständige Deinstallation (Empfohlen)**:

Windows (PowerShell):
```powershell
ai-cli --uninstall; pip uninstall ai-cli-launcher
```

Linux/macOS:
```bash
ai-cli --uninstall && pip uninstall ai-cli-launcher
```

**Schrittweise Deinstallation**:
```bash
# Schritt 1: Verknüpfungen bereinigen und Konfigurationsspeicherort anzeigen
ai-cli --uninstall

# Schritt 2: Paket deinstallieren
pip uninstall ai-cli-launcher
```

**Schnelle Deinstallation**:
```bash
# Nur Paket deinstallieren (Verknüpfungen bleiben erhalten)
pip uninstall ai-cli-launcher
```

**Manuelle Bereinigung** (falls erforderlich):
- Windows: `%APPDATA%\AI-CLI\` und Desktop-Verknüpfung löschen
- Linux: `~/.config/ai-cli/` löschen
- macOS: `~/Library/Application Support/ai-cli/` löschen

### Ausführen

```bash
ai-cli
```

## 📖 Verwendung

### Kommandozeilenoptionen

```bash
ai-cli                    # Interaktive Oberfläche starten
ai-cli --init             # Konfigurationsdatei initialisieren
ai-cli --config           # Konfigurationsdatei bearbeiten
ai-cli --lang zh          # Mit Chinesisch starten
ai-cli --lang ja          # Mit Japanisch starten
ai-cli --uninstall        # AI-CLI deinstallieren
ai-cli --version          # Versionsinformationen anzeigen
ai-cli --help             # Hilfeinformationen anzeigen
```

**Sprachoptionen** (`--lang` / `-l`):
- `auto` - Systemsprache automatisch erkennen (Standard)
- `en` - Englisch
- `zh` - Chinesisch (中文)
- `ja` - Japanisch (日本語)
- `de` - Deutsch

**Hinweis**: CLI-Sprachparameter hat Vorrang vor Konfigurationsdatei-Einstellungen.

### Tastenkombinationen

#### Projektauswahl-Bildschirm

| Taste | Funktion |
|-------|----------|
| `↑` / `↓` | Nach oben/unten navigieren |
| `Enter` | Projekt auswählen / Ordner öffnen |
| `Esc` | Zurück zum übergeordneten Ordner |
| `N` | Neues Projekt oder Ordner erstellen |
| `D` | Ausgewähltes Projekt oder Ordner löschen |
| `Q` | Anwendung beenden |

#### Tool-Auswahl-Bildschirm

| Taste | Funktion |
|-------|----------|
| `↑` / `↓` | Nach oben/unten navigieren |
| `Enter` | Tool starten (neues Fenster) |
| `Ctrl+Enter` | Tool starten (neuer Tab) |
| `I` | Fehlende Tools installieren |
| `R` | Tool-Liste aktualisieren |
| `Esc` | Zurück zur Projektauswahl |
| `Q` | Anwendung beenden |

### Arbeitsablauf

1. **Starten**: `ai-cli` ausführen
2. **Projekt auswählen**: Mit Pfeiltasten Projekt auswählen, `Enter` zum Bestätigen
3. **Tool auswählen**: Das gewünschte KI-Tool auswählen
4. **Arbeiten beginnen**: Tool startet in neuem Fenster oder Tab

## 🔧 Konfigurationsanleitung

### Speicherort der Konfigurationsdatei

- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### Struktur der Konfigurationsdatei

```json
{
  "projects": [
    {
      "type": "folder",
      "name": "Meine Projekte",
      "children": [
        {
          "type": "project",
          "name": "Web App",
          "path": "/pfad/zum/projekt",
          "env": {
            "API_KEY": "ihr-api-schlüssel",
            "DEBUG": "true"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "windowsInstall": "winget install kiro-cli",
      "wslInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "macosInstall": "brew install kiro-cli",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    }
  ],
  "settings": {
    "language": "auto",
    "terminalEmulator": "default",
    "theme": "default"
  }
}
```

### Projektkonfiguration

#### Projekttypen

**Ordner**:
```json
{
  "type": "folder",
  "name": "Projektgruppen-Name",
  "children": [...]
}
```

**Projekt**:
```json
{
  "type": "project",
  "name": "Projektname",
  "path": "/absoluter/pfad/zum/projekt",
  "env": {
    "SCHLÜSSEL": "wert"
  }
}
```

#### Umgebungsvariablen

Konfigurieren Sie unabhängige Umgebungsvariablen für jedes Projekt:

```json
{
  "type": "project",
  "name": "API-Projekt",
  "path": "/pfad/zur/api",
  "env": {
    "API_KEY": "sk-xxx",
    "API_BASE_URL": "https://api.example.com",
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

### Tool-Konfiguration

#### Erforderliche Felder

- `name`: Tool-Befehlsname (für Erkennung verwendet)
- `displayName`: Anzeigename
- `checkCommand`: Befehl zur Überprüfung der Tool-Installation

#### Installationsbefehle (nach Plattform)

- `windowsInstall`: Windows-nativer Installationsbefehl
- `wslInstall`: WSL-Umgebungs-Installationsbefehl
- `linuxInstall`: Linux-Installationsbefehl
- `macosInstall`: macOS-Installationsbefehl

#### Optionale Felder

- `url`: Offizielle Website des Tools (in Tool-Liste angezeigt)

#### Beispielkonfiguration

```json
{
  "name": "cursor",
  "displayName": "Cursor Agent",
  "windowsInstall": "winget install Cursor",
  "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
  "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
  "macosInstall": "brew install --cask cursor",
  "checkCommand": "cursor --version",
  "url": "https://cursor.sh"
}
```

### Einstellungsoptionen

#### language

- `auto`: Systemsprache automatisch erkennen (Standard)
- `en`: Englisch
- `zh`: Chinesisch
- `ja`: Japanisch
- `de`: Deutsch

#### terminalEmulator

- `default`: System-Standard-Terminal verwenden (Standard)
- `wt`: Windows Terminal (nur Windows)
- `iterm`: iTerm2 (nur macOS)
- `gnome-terminal`: GNOME Terminal (nur Linux)
- `konsole`: Konsole (nur Linux)

#### theme

- `default`: Standard-Dunkles-Theme
- Weitere Themes in zukünftigen Versionen

## 🏗️ Projektarchitektur

### Verzeichnisstruktur

```
ai_cli/
├── __init__.py        # Paketinitialisierung
├── cli.py             # CLI-Einstiegspunkt
├── app.py             # Hauptanwendungslogik
├── models.py          # Datenmodelle
├── config.py          # Konfigurationsverwaltung
├── utils.py           # Pfadkonvertierungs-Utilities
├── core/              # Kernfunktionalitätsmodule
│   ├── __init__.py
│   ├── tools.py       # Tool-Erkennung
│   ├── projects.py    # Projektverwaltung
│   ├── git.py         # Git-Integration
│   └── installer.py   # Tool-Installation
├── ui/                # Benutzeroberflächen-Module
│   ├── __init__.py
│   ├── theme.py       # Theme-Konfiguration
│   ├── menu.py        # Menü-Rendering
│   └── input.py       # Tastatureingabe-Handhabung
├── platform/          # Plattform-Adapter-Module
│   ├── __init__.py
│   ├── base.py        # Abstrakte Basisklasse
│   ├── windows.py     # Windows-Adapter
│   ├── linux.py       # Linux-Adapter
│   ├── macos.py       # macOS-Adapter
│   └── factory.py     # Plattform-Factory
└── i18n/              # Internationalisierungs-Module
    ├── __init__.py
    └── manager.py     # Sprach-Manager
```

## 🔍 Erweiterte Funktionen

### Git Worktree-Unterstützung

Wenn ein Projektpfad ein Git-Worktree ist, wird AI-CLI:

1. Alle Worktrees automatisch erkennen
2. Branch und Status für jeden Worktree anzeigen
3. Auswahl des zu verwendenden Worktrees ermöglichen
4. Voraus-/Zurück-Commit-Anzahl für Branches anzeigen

### WSL-Pfadkonvertierung

AI-CLI behandelt automatisch die Pfadkonvertierung zwischen Windows und WSL:

- Windows-Pfad: `C:\Users\username\project`
- WSL-Pfad: `/mnt/c/Users/username/project`

Konvertierung ist bidirektional und unterstützt:
- WSL-Tools von Windows aus starten
- Windows-Tools von WSL aus starten

### Asynchrone Tool-Erkennung

Tool-Erkennung verwendet asynchrone Parallelverarbeitung:

1. **Beim Start**: Oberfläche schnell anzeigen, Tools im Hintergrund erkennen
2. **Caching**: Erkennungsergebnisse werden gecacht, um wiederholte Prüfungen zu vermeiden
3. **Aktualisieren**: Drücken Sie `R`, um Cache zu löschen und neu zu erkennen

### Umgebungsvariablen-Injektion

Für jedes Projekt konfigurierte Umgebungsvariablen werden beim Starten von Tools injiziert:

```json
{
  "type": "project",
  "name": "API-Projekt",
  "path": "/pfad/zur/api",
  "env": {
    "API_KEY": "sk-xxx",
    "DEBUG": "true"
  }
}
```

Beim Starten eines Tools werden diese Umgebungsvariablen zur Laufzeitumgebung des Tools hinzugefügt.

## 🧪 Tests

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Spezifische Testdatei ausführen
pytest tests/test_models.py

# Spezifischen Test ausführen
pytest tests/test_models.py::TestConfig::test_from_dict

# Ausführliche Ausgabe anzeigen
pytest -v

# Print-Ausgabe anzeigen
pytest -s
```

### Test-Abdeckung

```bash
# Tests mit Abdeckungsbericht ausführen
pytest --cov=ai_cli

# HTML-Abdeckungsbericht generieren
pytest --cov=ai_cli --cov-report=html

# Bericht anzeigen
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 📝 Entwicklungsanleitung

### Anforderungen

- **Python**: 3.8 oder höher
- **Abhängigkeiten**:
  - `rich`: Terminal-UI-Rendering
  - `prompt-toolkit`: Tastatureingabe-Handhabung
  - `click`: CLI-Framework
  - `platformdirs`: Plattformübergreifende Pfade

### Entwicklungsumgebung einrichten

```bash
# 1. Repository klonen
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 2. Python-Version Worktree erstellen (falls erforderlich)
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 3. Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv

# Virtuelle Umgebung aktivieren
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Entwicklungsabhängigkeiten installieren
pip install -e ".[dev]"

# 5. Tests ausführen, um Umgebung zu überprüfen
pytest
```

### Code-Stil

Projekt folgt PEP 8-Stilrichtlinien:

```bash
# Code-Prüfwerkzeuge installieren
pip install flake8 black mypy

# Code-Prüfungen ausführen
flake8 ai_cli tests

# Code automatisch formatieren
black ai_cli tests

# Typprüfung
mypy ai_cli
```

## 🐛 Fehlerbehebung

### Windows-Probleme

**Problem**: Windows Terminal kann nicht erkannt werden
```bash
# Lösung: Sicherstellen, dass Windows Terminal installiert ist
winget install Microsoft.WindowsTerminal
```

**Problem**: WSL-Tool-Erkennung schlägt fehl
```bash
# Lösung: Sicherstellen, dass WSL aktiviert ist
wsl --install
```

### Linux-Probleme

**Problem**: Terminal-Emulator-Erkennung schlägt fehl
```bash
# Lösung: Unterstütztes Terminal installieren
sudo apt install gnome-terminal  # Ubuntu/Debian
sudo dnf install gnome-terminal  # Fedora
```

### macOS-Probleme

**Problem**: iTerm2 nicht erkannt
```bash
# Lösung: Sicherstellen, dass iTerm2 installiert ist
brew install --cask iterm2
```

### Allgemeine Probleme

**Problem**: Konfigurationsdatei beschädigt
```bash
# Lösung: Konfiguration neu initialisieren
ai-cli --init
```

**Problem**: Tool-Erkennungs-Cache veraltet
```bash
# Lösung: R-Taste im Tool-Auswahl-Bildschirm drücken, um zu aktualisieren
```

## 🤝 Mitwirken

Wir begrüßen alle Formen der Mitwirkung!

### Möglichkeiten zur Mitwirkung

1. **Fehler melden**: Issues auf [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues) einreichen
2. **Feature-Anfragen**: Neue Feature-Ideen vorschlagen
3. **Code-Beiträge**: Pull Requests einreichen
4. **Dokumentation**: Dokumentation und Beispiele verbessern
5. **Übersetzungen**: Neue Sprachunterstützung hinzufügen

### Pull-Request-Prozess

1. Projekt forken
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Zu Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request öffnen

### Commit-Konvention

[Conventional Commits](https://www.conventionalcommits.org/) folgen:

```
feat: Neue Funktion hinzufügen
fix: Fehler beheben
docs: Dokumentation aktualisieren
style: Code-Formatierung
refactor: Code-Refactoring
test: Test-bezogen
chore: Build/Toolchain-Updates
```

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE)-Datei für Details.

## 🔗 Verwandte Links

- **Original-Projekt**: [AI-CLI (PowerShell Edition)](https://github.com/hyfhot/AI-CLI)
- **Dokumentation**: [docs/](docs/)
- **Issue-Tracker**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## 🙏 Danksagungen

Dank an diese Open-Source-Projekte:

- [Rich](https://github.com/Textualize/rich) - Leistungsstarke Terminal-UI-Bibliothek
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interaktive Kommandozeilen-Tools
- [Click](https://github.com/pallets/click) - Python-CLI-Framework
- [platformdirs](https://github.com/platformdirs/platformdirs) - Plattformübergreifende Verzeichnispfade

## 📊 Projektstatus

- **Version**: Beta
- **Python-Version**: 3.8+
- **Plattformen**: Windows, Linux, macOS
- **Wartung**: Aktiv entwickelt

## 🗺️ Roadmap

- [ ] Mehr KI-Tools unterstützen
- [ ] Plugin-System
- [ ] Konfigurationsdatei-Validierung
- [ ] Mehr Theme-Optionen
- [ ] Tool-Nutzungsstatistiken
- [ ] Cloud-Konfigurations-Synchronisation
- [ ] Projektvorlagen-Unterstützung

---

**Mit ❤️ erstellt vom AI-CLI-Team**
