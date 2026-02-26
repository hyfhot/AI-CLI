🌐 [English](SCOOP-PUBLISH.md) | [中文](SCOOP-PUBLISH.zh.md) | [日本語](SCOOP-PUBLISH.ja.md)

# Publishing to Scoop Tutorial

## Option 1: Publish to Official Scoop Bucket (Recommended but Strict Review)

### 1. Preparation

**Create GitHub Release:**
```bash
# 1. Ensure code is committed
git add .
git commit -m "Release v2.2.0"
git push

# 2. Create and push tag
git tag -a v2.2.0 -m "Release version 2.2.0"
git push origin v2.2.0

# 3. Create Release on GitHub web page
# Visit: https://github.com/hyfhot/AI-CLI/releases/new
# - Tag: v2.2.0
# - Title: AI-CLI v2.2.0
# - Description: Add version update notes
# - Click "Publish release"
```

**Calculate File Hash:**
```powershell
# Download release archive
$url = "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v2.2.0.zip"
Invoke-WebRequest -Uri $url -OutFile "ai-cli-v2.2.0.zip"

# Calculate SHA256
Get-FileHash "ai-cli-v2.2.0.zip" -Algorithm SHA256 | Select-Object -ExpandProperty Hash
```

**Update manifest hash field:**
```json
{
    "hash": "calculated SHA256 value"
}
```

### 2. Submit to Official Bucket

```bash
# Fork Scoop official bucket
# Visit: https://github.com/ScoopInstaller/Main
# Click "Fork" in the top right corner

# Clone your fork
git clone https://github.com/your-username/Main.git scoop-main
cd scoop-main

# Create new branch
git checkout -b add-ai-cli

# Copy manifest
cp /path/to/ai-cli.json bucket/ai-cli.json

# Commit
git add bucket/ai-cli.json
git commit -m "Add ai-cli: AI CLI Launcher for coding tools"
git push origin add-ai-cli

# Create Pull Request on GitHub
# Visit your fork page, click "Compare & pull request"
```

**Note:** Official bucket has strict review, may require:
- Tool has certain popularity
- High code quality
- Complete documentation
- May need to wait several days to weeks

---

## Option 2: Create Your Own Bucket (Recommended, Quick Launch)

### 1. Create Bucket Repository

```bash
# Create new repository on GitHub
# Repository name: scoop-bucket (or any name)
# Description: Scoop bucket for AI-CLI
# Public repository

# Clone to local
git clone https://github.com/hyfhot/scoop-bucket.git
cd scoop-bucket

# Copy manifest
cp /path/to/ai-cli.json ./ai-cli.json

# Create README
cat > README.md << 'EOF'
# Scoop Bucket for AI-CLI

AI CLI Launcher - Unified terminal launcher for AI coding tools.

## Installation

```powershell
# Add this bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# Install AI-CLI
scoop install ai-cli
```

## Usage

```powershell
ai-cli          # Start interactive launcher
ai-cli --help   # Show help
ai-cli --init   # Initialize configuration
```

## Links

- [GitHub Repository](https://github.com/hyfhot/AI-CLI)
- [Documentation](https://github.com/hyfhot/AI-CLI/blob/master/README.md)
EOF

# Commit and push
git add .
git commit -m "Initial commit: Add ai-cli manifest"
git push origin main
```

### 2. User Installation

Users just need to run:
```powershell
# Add your bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# Install
scoop install ai-cli

# Use
ai-cli
```

### 3. Update Version

```bash
# 1. Update main project and create new tag
cd AI-CLI
git tag v2.3.0
git push origin v2.3.0

# 2. Update manifest in bucket
cd scoop-bucket
# Edit ai-cli.json, update version and hash
git add ai-cli.json
git commit -m "Update ai-cli to v2.3.0"
git push

# User update
scoop update ai-cli
```

---

## Option 3: Submit to Community Bucket (Compromise Solution)

Scoop has some community-maintained buckets with more lenient review:

### Extras Bucket (Recommended)
Suitable for GUI tools and non-mainstream CLI tools:

```bash
# Fork https://github.com/ScoopInstaller/Extras
git clone https://github.com/your-username/Extras.git
cd Extras

git checkout -b add-ai-cli
cp /path/to/ai-cli.json bucket/ai-cli.json

git add bucket/ai-cli.json
git commit -m "ai-cli: Add AI CLI Launcher"
git push origin add-ai-cli

# Create PR to ScoopInstaller/Extras
```

---

## Test Manifest

Test locally before publishing:

```powershell
# Method 1: Install directly from local
scoop install /path/to/ai-cli.json

# Method 2: Install from URL
scoop install https://raw.githubusercontent.com/hyfhot/scoop-bucket/main/ai-cli.json

# Test uninstall
scoop uninstall ai-cli

# Test update
scoop update ai-cli
```

---

## Recommended Process

**Phase 1 (Do Immediately):**
1. Create your own bucket (Option 2)
2. Add Scoop installation instructions in README.md
3. Users can use it immediately

**Phase 2 (After Project Matures):**
1. Submit to Extras bucket (Option 3)
2. Get more exposure

**Phase 3 (Optional):**
1. If the tool is popular enough, submit to Main bucket (Option 1)

---

## Add Installation Instructions in README

Add this to your `README.md`:

```markdown
### Install via Scoop (Recommended)

```powershell
# Add bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# Install
scoop install ai-cli

# Use
ai-cli
```

### Install via Installation Script

```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```
```

---

## Automated Update (Optional)

Create GitHub Action to automatically update hash:

```yaml
# .github/workflows/update-scoop.yml
name: Update Scoop Manifest

on:
  release:
    types: [published]

jobs:
  update:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: hyfhot/scoop-bucket
          token: ${{ secrets.SCOOP_TOKEN }}

      - name: Update manifest
        run: |
          $version = "${{ github.event.release.tag_name }}".TrimStart('v')
          $url = "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v$version.zip"
          $hash = (Invoke-WebRequest $url | Get-FileHash).Hash

          $manifest = Get-Content ai-cli.json | ConvertFrom-Json
          $manifest.version = $version
          $manifest.hash = $hash
          $manifest | ConvertTo-Json -Depth 10 | Set-Content ai-cli.json

          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add ai-cli.json
          git commit -m "Update ai-cli to v$version"
          git push
```

---

Need help with which step to execute?
