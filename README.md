# 📔 Bloco de Notas Interativo - Guia de Uso

## ✅ Projeto Completado!

Seu site de "Bloco de Notas Interativo" estilo Notion foi criado com sucesso! A aplicação está pronta para funcionar.

---

## 🚀 Como Usar

### 1. **Iniciar o Servidor**
```bash
python app.py
```
O servidor rodará em `http://127.0.0.1:5000`

### 2. **Criar Conta**
- Acesse `/cadastro`
- Preencha: Nome, E-mail, Senha (2x para confirmar)
- Clique em "Criar Conta"

### 3. **Fazer Login**
- Use suas credenciais criadas
- Você será redirecionado para o Dashboard

### 4. **Funcionalidades Principais**

#### 📅 **Dashboard**
- Visualiza a última entrada do seu diário
- Mostra as 8 entradas mais recentes
- Acesso rápido aos recursos principais

#### ✍️ **Diário Hoje** / **Diário [Data]**
Registre seu dia com as seguintes seções:

1. **📷 Foto do Dia** - URL de uma foto do seu dia
2. **📋 Rotina** - Descreva sua rotina diária
3. **📖 Diário (Reflexão)** - Escreva sobre como foi seu dia
4. **😊 Emoções** - Selecione as emoções vividas:
   - Feliz, Triste, Ansioso, Calmo, Motivado, Cansado, Frustrado, Grato
5. **⭐ Habilidades (Solo Leveling)** - Marque quais habilidades você desenvolveu:
   - Programação, Criatividade, Comunicação, Liderança
   - Fitness, Meditação, Leitura, Música
   - Culinária, Desenho (e mais)
6. **✅ Checklist de Tarefas** - Liste as tarefas do dia
   - Adicione quantas quiser
   - Remova as que não quer

#### 📚 **Histórico**
- Veja todas as suas entradas anteriores
- Clique em uma data para editar
- Veja um resumo de cada dia (emoções, habilidades, tarefas)
- Delete entradas se necessário

#### 📊 **Análise**
Veja estatísticas e insights:
- **Dias Registrados** - Total de dias com entradas
- **Tarefas Concluídas** - Quantas tarefas você completou
- **Taxa de Conclusão** - Percentual de tarefas feitas
- **Habilidades Desenvolvidas** - Gráfico de quais habilidades você mais trabalhou
- **Emoções Mais Frequentes** - Quais emoções você mais sentiu
- **Insights Automáticos** - Sugestões baseadas nos seus dados

---

## 🎨 Design & Interface

### Cores
- **Primária**: Azul-roxo (#667eea)
- **Secundária**: Roxo (#764ba2)
- **Fundo**: Cinza claro (#f8f9fa)

### Componentes
- ✨ Cards elegantes com shadows
- 🎯 Botões interativos com hover effects
- 📱 Design responsivo (funciona em mobile)
- 🔔 Notificações automáticas (flash messages)

---

## 🗄️ Estrutura do Banco de Dados (Firebase)

```
firebase_root/
├── usuarios/
│   └── {user_id}
│       ├── nome
│       ├── email
│       ├── senha_hash
│       ├── data_registro
│       └── foto_perfil_url
│
└── diarios/
    └── {user_id}
        └── {data: YYYY-MM-DD}
            ├── rotina
            ├── journal
            ├── emocoes []
            ├── habilidades []
            ├── checklist []
            │   └── {texto, feito}
            ├── photo_url
            └── timestamp
```

---

## 🔧 Arquivos Principais

### Backend
- **app.py** - Servidor Flask com todas as rotas
- Firebase Realtime Database para armazenamento

### Frontend
- **templates/base.html** - Template base (navegação, header, footer)
- **templates/index.html** - Dashboard
- **templates/diario.html** - Página de edição do diário
- **templates/historico.html** - Histórico de entradas
- **templates/analise.html** - Análise e estatísticas
- **templates/login.html** - Página de login
- **templates/cadastro.html** - Página de cadastro

### Assets
- **static/style.css** - Estilos CSS (layout, cores, responsividade)
- **static/diario.js** - Scripts JavaScript (interatividade)

---

## 🎯 Funcionalidades Implementadas

✅ **Autenticação**
- Cadastro com validação
- Login seguro com hash de senha
- Logout com limpeza de sessão

✅ **Diário**
- Criar entrada do dia
- Editar entrada existente
- Deletar entrada
- Foto do dia
- Rotina do dia
- Reflexão do dia

✅ **Emoções & Habilidades**
- 8 emoções predefinidas com emojis
- 10 habilidades (Solo Leveling)
- Marcar múltiplas seleções

✅ **Checklist**
- Adicionar/remover tarefas dinamicamente
- Marcar tarefas como concluídas
- Calcular taxa de conclusão

✅ **Histórico**
- Visualizar todas as entradas
- Editar qualquer entrada passada
- Deletar entradas

✅ **Análise**
- Estatísticas de dias registrados
- Taxa de conclusão de tarefas
- Emoções mais frequentes
- Habilidades mais desenvolvidas
- Insights automáticos

---

## 🌐 URLs da Aplicação

| Rota | Descrição |
|------|-----------|
| `/` | Dashboard (home) |
| `/login` | Página de login |
| `/cadastro` | Página de cadastro |
| `/logout` | Fazer logout |
| `/diario/hoje` | Abrir diário de hoje |
| `/diario/<data>` | Abrir diário de um dia específico |
| `/historico` | Ver histórico completo |
| `/analise` | Ver análises e estatísticas |
| `/diario/<data>/checklist/toggle/<index>` | Marcar tarefa como feita |
| `/deletar-diario/<data>` | Deletar uma entrada |

---

## 💡 Dicas de Uso

1. **Foto do Dia**: Use URLs de imagens. Pode ser de qualquer plataforma (Imgur, Unsplash, etc.)

2. **Emoções**: Você pode selecionar múltiplas emoções do mesmo dia

3. **Habilidades**: Track seu progresso em até 10 habilidades diferentes

4. **Checklist**: Adicione quantas tarefas quiser. Elas são salvas automaticamente

5. **Análise**: Quanto mais dados, melhor os insights! Mantenha a rotina de registrar

6. **Histórico**: Você pode visualizar, editar e deletar qualquer entrada anterior

---

## 🐛 Troubleshooting

### "Erro de conexão com Firebase"
- Verifique se o arquivo `ttk2k-642d6-firebase-adminsdk-fbsvc-e3c9e51e2b.json` está no diretório raiz
- Certifique-se que a URL do Firebase está correta em `app.py`

### Página em branco
- Certifique-se de estar logado
- Verifique o console do navegador (F12) para erros JavaScript
- Verifique o console do Flask para erros Python

### CSS não carregando
- Limpe o cache do navegador (Ctrl+Shift+Del)
- Certifique-se que o arquivo `/static/style.css` existe

---

## 📝 Próximos Passos (Melhorias Futuras)

- [ ] Upload de fotos diretamente (sem usar URL)
- [ ] Exportar diário em PDF
- [ ] Compartilhar entradas com amigos
- [ ] Temas customizáveis
- [ ] Sincronização com Google Drive
- [ ] Aplicativo mobile
- [ ] Notificações diárias
- [ ] Backup automático

---

## 📧 Suporte

Se encontrar problemas, verifique:
1. Conexão com internet
2. Arquivo de credenciais do Firebase
3. Permissões do banco de dados (Firebase Rules)
4. Versão do Python (3.8+)
5. Bibliotecas instaladas: `pip install -r requirements.txt`

---

**Desenvolvido com ❤️ para você!**

Data: 27 de novembro de 2025
