# AI CLI Tools Referenz

> 🌐 [English](TOOLS.md) | [中文](TOOLS.zh.md) | [日本語](TOOLS.ja.md) | **Deutsch**

Dieses Dokument listet die von AI-CLI unterstützten Mainstream-KI-Programmiertools zusammen mit ihren Installations- und Konfigurationsinformationen auf.

---

## 🤖 Liste der unterstützten Tools

### 1. Kiro CLI (AWS)
- **Offizielle Website**: https://kiro.dev/cli/
- **Entwickler**: Amazon Web Services
- **Funktionen**:
  - Spezifikationsgetriebene Entwicklungsplattform
  - Unterstützt agentenbasierte Workflows
  - Integrierte AWS-Dienste
  - Unterstützt Model Context Protocol (MCP)
- **Installation**:
  - **Linux/macOS/WSL**: `curl -fsSL https://cli.kiro.dev/install | bash`
  - **Windows**: `winget install kiro-cli` (falls verfügbar)
- **Überprüfung**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **Offizielle Website**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **Entwickler**: Anthropic
- **Funktionen**:
  - Agentenbasierter Coding-Assistent
  - Natürlichsprachliche Code-Generierung
  - Kontextbewusste Vorschläge
- **Installation**:
  - **Alle Plattformen**: `npm install -g @anthropic-ai/claude-code`
- **Überprüfung**: `claude-code --version`

---

### 3. Cursor Agent
- **Offizielle Website**: https://cursor.sh
- **Entwickler**: Cursor Team
- **Funktionen**:
  - KI-gestützter Code-Editor
  - Inline-Code-Vorschläge
  - Chat-basierte Coding-Unterstützung
- **Installation**:
  - **Windows**: `winget install Cursor`
  - **macOS**: `brew install --cask cursor`
  - **Linux**: Von offizieller Website herunterladen
- **Überprüfung**: `cursor --version`

---

### 4. GitHub Copilot CLI
- **Offizielle Website**: https://githubnext.com/projects/copilot-cli
- **Entwickler**: GitHub
- **Funktionen**:
  - Kommandozeilen-KI-Assistent
  - Shell-Befehlsvorschläge
  - Git-Workflow-Unterstützung
- **Installation**:
  - **Alle Plattformen**: `npm install -g @githubnext/github-copilot-cli`
- **Überprüfung**: `github-copilot-cli --version`

---

### 5. Aider
- **Offizielle Website**: https://aider.chat
- **Entwickler**: Aider Team
- **Funktionen**:
  - KI-Pair-Programming im Terminal
  - Git-Integration
  - Unterstützung mehrerer LLMs
- **Installation**:
  - **Alle Plattformen**: `pip install aider-chat`
- **Überprüfung**: `aider --version`

---

## 📝 Konfigurationsbeispiel

Tools zu Ihrer `config.json` hinzufügen:

```json
{
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
    },
    {
      "name": "cursor",
      "displayName": "Cursor Agent",
      "windowsInstall": "winget install Cursor",
      "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
      "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
      "macosInstall": "brew install --cask cursor",
      "checkCommand": "cursor --version",
      "url": "https://cursor.sh"
    },
    {
      "name": "aider",
      "displayName": "Aider",
      "windowsInstall": "pip install aider-chat",
      "wslInstall": "pip install aider-chat",
      "linuxInstall": "pip install aider-chat",
      "macosInstall": "pip install aider-chat",
      "checkCommand": "aider --version",
      "url": "https://aider.chat"
    }
  ]
}
```

---

## 🔧 Benutzerdefinierte Tools hinzufügen

Um ein neues Tool hinzuzufügen:

1. **Installationsbefehle finden** für jede Plattform
2. **Überprüfungsbefehl bestimmen** zur Verifizierung der Installation
3. **Zu config.json hinzufügen** gemäß dem obigen Format

### Erforderliche Felder

- `name`: Befehlsname (für Erkennung verwendet)
- `displayName`: Anzeigename in der Benutzeroberfläche
- `checkCommand`: Befehl zur Überprüfung der Installation

### Plattformspezifische Installationsbefehle

- `windowsInstall`: Windows-native Installation
- `wslInstall`: WSL-Umgebungsinstallation
- `linuxInstall`: Linux-Installation
- `macosInstall`: macOS-Installation

### Optionale Felder

- `url`: Offizielle Website (in Tool-Liste angezeigt)

---

## 💡 Tipps

1. **Verwenden Sie Paketmanager** wenn möglich (winget, brew, apt, etc.)
2. **Testen Sie Überprüfungsbefehle** um sicherzustellen, dass sie korrekt funktionieren
3. **Halten Sie URLs aktuell** zur Benutzerreferenz
4. **Dokumentieren Sie Voraussetzungen** wenn Tools spezifische Abhängigkeiten benötigen

---

Weitere Informationen finden Sie in der [Haupt-README](../README.de.md).
