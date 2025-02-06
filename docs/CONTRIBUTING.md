# Contribution Guide

Thank you for your interest in contributing to this project! To ensure an efficient and collaborative process, follow these guidelines:

## 🛠 Environment Configuration

1. **Create a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/macOS
   # ou
    env/Scripts/Activate  # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Pre-commit** (Optional):
   ```bash
   pre-commit install
   ```

## 🌿 Branch Strategy

- **Branch Base**: Use `main` or `develop` as a basis
- **Padrão de Nomes**:
  ```bash
  feature/feature-name
  fix/fix-name
  hotfix/urgent-description
  ```

## ✏️ Commit Convention

Follow the pattern **[Conventional Commits](https://www.conventionalcommits.org/)**:
```bash
<type>[optional scope]: <description>
```

**Exemplo**:
```bash
feat(auth): add password recovery feature

- Implement recovery email flow
- Add related tests

Refs: #123
```

## 🔄 Pull Request Process

1. Sync your branch with the base branch
2. Ensure all tests pass:
   ```bash
   pytest --cov
   ```
3. Update relevant documentation
4. Describe in the PR:
   - Motivation for changes
   - Technical impact
   - Relationship with issues (e.g. Closes #123)

### Validation

- [ ] Script `Handtracking.py or HandMotion.py` executed successfully
- [ ] Screenshot of tracking in action (attached in PR)
- [ ] Manual testing in the Flask interface (if applicable)

## 🐛 Reporting Issues

Include:
1. Project version
2. Steps to reproduce
3. Expected vs current behavior
4. Screenshots (if applicable)

## 📜 Product Guide

To save how the product works follow [User Guide](UserGuide.rst).

## 📄 Licensing

By contributing, you agree to license your contribution under the terms of the project's [LICENSE](../LICENSE).

---

Thanks for contributing! 💚