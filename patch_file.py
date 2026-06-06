with open('pyproject.toml', 'r') as f:
    lines = f.readlines()
with open('pyproject.toml', 'w') as f:
    for line in lines:
        if "--cov" in line or "--cov-report" in line:
            continue
        f.write(line)
