# Guia de Contribuição

Agradecemos seu interesse em contribuir para este projeto! Para garantir um processo eficiente e colaborativo, siga estas diretrizes:

## 🛠 Configuração do Ambiente

1. **Crie um Ambiente Virtual**:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/macOS
   # ou
    env/Scripts/Activate  # Windows
   ```

2. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Pré-commit** (opcional):
   ```bash
   pre-commit install
   ```

## 🌿 Estratégia de Branches

- **Branch Base**: Use `main` ou `develop` como base
- **Padrão de Nomes**:
  ```bash
  feature/nome-da-feature
  fix/nome-da-correcao
  hotfix/descricao-urgente
  ```

## ✏️ Convenção de Commits

Siga o padrão **[Conventional Commits](https://www.conventionalcommits.org/)**:
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

## 🔄 Processo de Pull Request

1. Sincronize sua branch com a branch base
2. Garanta que todos os testes passem:
   ```bash
   pytest --cov
   ```
3. Atualize a documentação relevante
4. Descreva no PR:
   - Motivação das mudanças
   - Impacto técnico
   - Relação com issues (ex: Closes #123)

### Validação

- [ ] Script `Handtracking.py ou HandMotion.py` executado com sucesso
- [ ] Screenshot do rastreamento em ação (anexada no PR)
- [ ] Teste manual na interface do Flask (se aplicável)

## 🐛 Reportando Issues

Inclua:
1. Versão do projeto
2. Passos para reproduzir
3. Comportamento esperado vs atual
4. Capturas de tela (se aplicável)

## 📜 Guia do Produto

Para saver como o produto funciona siga [Guia do Usuario](UserGuide.rst).

## 📄 Licenciamento

Ao contribuir, você concorda em licenciar sua contribuição sob os termos da [LICENÇA](../LICENSE) do projeto.

---

Obrigado por contribuir! 💚