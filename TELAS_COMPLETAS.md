# 🎯 15 Telas Completas - Bloco de Notas Interativo

## Resumo da Expansão (Fase 5)

Seu aplicativo foi expandido de 7 para **15 telas** com funcionalidades avançadas, upload de fotos, comunidade, achievements e muito mais!

---

## 📋 Índice das 15 Telas

### **Telas Originais (7)**
1. [Dashboard (index.html)](#1-dashboard)
2. [Diário Hoje (diario.html)](#2-diário-hoje)
3. [Histórico (historico.html)](#3-histórico)
4. [Análise (analise.html)](#4-análise)
5. [Login (login.html)](#5-login)
6. [Cadastro (cadastro.html)](#6-cadastro)
7. [Base Layout (base.html)](#7-base-layout)

### **Novas Telas (8)**
8. [Meu Perfil (perfil.html)](#8-meu-perfil)
9. [Achievements (achievements.html)](#9-achievements)
10. [Configurações (configuracoes.html)](#10-configurações)
11. [Busca Avançada (busca.html)](#11-busca-avançada)
12. [Galeria de Fotos (galeria.html)](#12-galeria-de-fotos)
13. [Comunidade (comunidade.html)](#13-comunidade)
14. [Notificações (notificacoes.html)](#14-notificações)
15. [Calendário (calendario.html)](#15-calendário)

---

## 🎨 Detalhes das Telas

### **1. Dashboard**
**Arquivo:** `templates/index.html`  
**Rota:** `/`  
**Descrição:** Página inicial com resumo do dia, estatísticas rápidas e atalhos para as principais funções.

**Recursos:**
- Resumo do dia (entrada, emoção, habilidade)
- Cards com estatísticas (entradas, sequência, badges)
- Atalhos rápidos para outras seções
- Gráfico de sentimentos da semana

---

### **2. Diário Hoje**
**Arquivo:** `templates/diario.html`  
**Rota:** `/diario/<dia>`  
**Descrição:** Página principal para escrever e gerenciar entradas do diário.

**Recursos:**
- ✍️ Campo de texto para journal
- 📸 Upload de foto do dia
- 😊 Seleção de emoções (8 tipos diferentes)
- 🎯 Seleção de habilidades desenvolvidas
- ✅ Checklist de tarefas/rotinas
- 💭 Reflexão opcional

---

### **3. Histórico**
**Arquivo:** `templates/historico.html`  
**Rota:** `/historico`  
**Descrição:** Visualização de todas as entradas passadas em formato de timeline.

**Recursos:**
- Timeline de entradas por data
- Cards com preview de entradas
- Filtro por mês/semana
- Busca rápida de datas
- Visualização de entradas anteriores

---

### **4. Análise**
**Arquivo:** `templates/analise.html`  
**Rota:** `/analise`  
**Descrição:** Análise detalhada de dados com gráficos e gerenciamento de emoções/habilidades.

**Recursos:**
- 📊 Gráficos de sentimentos
- 📈 Gráficos de habilidades
- ➕ Adicionar/editar/deletar emoções (CRUD completo via AJAX)
- ➕ Adicionar/editar/deletar habilidades (CRUD completo via AJAX)
- 📉 Análise de tendências
- 🔥 Sequência de dias

---

### **5. Login**
**Arquivo:** `templates/login.html`  
**Rota:** `/login`  
**Descrição:** Página de autenticação do usuário.

**Recursos:**
- Campo de email
- Campo de senha
- Validação de credenciais
- Redirecionamento automático após login
- Link para página de cadastro

---

### **6. Cadastro**
**Arquivo:** `templates/cadastro.html`  
**Rota:** `/cadastro`  
**Descrição:** Página de registro de novo usuário.

**Recursos:**
- Campo de nome
- Campo de email
- Campo de senha
- Confirmação de senha
- Hash de senha seguro
- Validação de entrada

---

### **7. Base Layout**
**Arquivo:** `templates/base.html`  
**Descrição:** Template base com navegação, header e footer.

**Recursos:**
- 🧭 Navbar com links principais
- 🔄 Tema toggle (claro/escuro)
- 📱 Dropdown "Mais" com acesso a todas as 8 novas telas
- ⚡ Flash messages para feedback
- 📱 Layout responsivo

---

## ✨ NOVAS TELAS (8)

### **8. Meu Perfil**
**Arquivo:** `templates/perfil.html`  
**Rota:** `/perfil` (GET)  
**Descrição:** Página de perfil do usuário com badges conquistadas.

**Recursos:**
- 👤 Foto de perfil com cover
- 📊 Estatísticas pessoais (badges, exp)
- 🏆 Exibição de badges desbloqueados
- ⚡ Ações rápidas (novo diário, achievements, análise, config)
- 📈 Estatísticas: entradas, dias seguidos, exp ganho

**Backend:** 
```python
@app.route('/perfil')
def perfil():
    # Carrega info do usuário e badges do Firebase
    return render_template('perfil.html', usuario=usuario, badges=badges)
```

---

### **9. Achievements**
**Arquivo:** `templates/achievements.html`  
**Rota:** `/achievements` (GET)  
**Descrição:** Página de badges/conquistas com sistema de progresso.

**Recursos:**
- 🏆 6 tipos de badges predefinidos:
  - **Primeira Entrada** (📝) - Crie primeira entrada
  - **7 Dias** (🔥) - Escreva 7 dias seguidos
  - **30 Dias** (🌟) - Mantenha sequência de 30
  - **100 Entradas** (💯) - Complete 100 entradas
  - **Explorador** (🗺️) - Use 5 habilidades diferentes
  - **Sentimentos Master** (💜) - Registre 8 sentimentos
- 📊 Barras de progresso
- 💡 Dicas para desbloquear badges
- 📈 Contador de badges desbloqueados

**Backend:**
```python
@app.route('/achievements')
def achievements():
    # Carrega badges do Firebase
    all_badges = {...}
    return render_template('achievements.html', badges=user_badges)
```

---

### **10. Configurações**
**Arquivo:** `templates/configuracoes.html`  
**Rota:** `/configuracoes` (GET) + `/api/config` (POST)  
**Descrição:** Página completa de configurações do aplicativo.

**Recursos:**
- **Perfil**
  - Editar nome
  - Email (somente leitura)
  - Bio/Sobre
- **Notificações**
  - Toggle: Lembrete diário
  - Toggle: Notificações de badges
  - Toggle: Alerta de sequência
  - Horário preferido
- **Privacidade & Segurança**
  - Toggle: Perfil público
  - Toggle: Compartilhamento de dados
  - Alterar senha
- **Aparência**
  - Seletor de tema (claro/escuro/automático)
  - Tamanho de fonte (pequeno/normal/grande)
  - Modo compacto
- **Dados**
  - Exportar para JSON
  - Exportar para PDF
  - Exportar para CSV
- **Zona Perigosa**
  - Limpar todos os dados
  - Deletar conta

**Backend:**
```python
@app.route('/configuracoes')
def configuracoes():
    config = DB_ROOT.child('listas').child(user_id).child('config').get()
    return render_template('configuracoes.html', config=config)

@app.route('/api/config', methods=['POST'])
def api_config_update():
    config_data = request.get_json()
    # Salva no Firebase
    return jsonify({'success': True})
```

---

### **11. Busca Avançada**
**Arquivo:** `templates/busca.html`  
**Rota:** `/busca` (GET)  
**Descrição:** Página com filtros avançados para encontrar entradas.

**Recursos:**
- 🔍 Busca por texto
- 😊 Filtro por emoções (múltiplas seleções)
- 🎯 Filtro por habilidades (múltiplas seleções)
- 📅 Filtro por data (intervalo)
- 📊 Ordenação (recente, antigo, alfabético)
- 📌 Exibição de resultados como cards
- 🏷️ Tags de emoção e habilidade por resultado

**Backend:**
```python
@app.route('/busca')
def busca():
    query = request.args.get('q', '')
    emocao = request.args.get('emocao', '')
    # Filtra entradas do Firebase
    resultados = [...]
    return render_template('busca.html', resultados=resultados)
```

---

### **12. Galeria de Fotos**
**Arquivo:** `templates/galeria.html`  
**Rota:** `/galeria` (GET) + `/api/upload-foto` (POST) + `/api/galeria` (GET)  
**Descrição:** Galeria com upload de fotos e visualização.

**Recursos:**
- 📸 Upload de arquivo ou URL
- 🖼️ Grid responsivo de fotos
- 🔍 Visualização expandida em modal
- ❤️ Sistema de favoritos
- 🗑️ Deletar fotos
- 📅 Timeline view
- ⭐ View de favoritos
- 📤 Drag & drop para upload

**Backend:**
```python
@app.route('/api/upload-foto', methods=['POST'])
def upload_foto():
    # Recebe arquivo ou URL
    # Converte para base64
    # Salva em Firebase /galeria/{user_id}/
    return jsonify({'success': True, 'url': photo_url})

@app.route('/api/galeria')
def api_galeria():
    fotos = DB_ROOT.child('galeria').child(user_id).get()
    return jsonify({'fotos': fotos_list})

@app.route('/galeria')
def galeria():
    return render_template('galeria.html', fotos=fotos)
```

---

### **13. Comunidade**
**Arquivo:** `templates/comunidade.html`  
**Rota:** `/comunidade` (GET)  
**Descrição:** Rede social para compartilhar experiências com outros usuários.

**Recursos:**
- 📝 Criar posts públicos
- ❤️ Curtir posts (like)
- 💬 Comentar em posts
- 📤 Compartilhar posts
- 🔥 Posts populares
- 🕐 Posts recentes
- 👥 Posts de amigos
- #️⃣ Tópicos em alta (hashtags)
- 👥 Usuários para seguir
- 📊 Feed social com avatares

**Backend:**
```python
@app.route('/comunidade')
def comunidade():
    posts = DB_ROOT.child('posts').get()
    return render_template('comunidade.html', posts=posts_list)
```

---

### **14. Notificações**
**Arquivo:** `templates/notificacoes.html`  
**Rota:** `/notificacoes` (GET)  
**Descrição:** Centro de notificações com diferentes tipos.

**Recursos:**
- 🔔 Notificações de badges desbloqueados
- ❤️ Notificações de curtidas em posts
- 💬 Notificações de comentários
- 🔥 Notificações de sequência
- ⏰ Lembretes de diário
- 👥 Notificações de novo seguidor
- 🔧 Notificações de sistema
- Marcar como lida
- Descartar notificações
- Filtro por tipo (Todas, Não Lidas, Diário, Social, Sistema)

**Backend:**
```python
@app.route('/notificacoes')
def notificacoes():
    notifs = DB_ROOT.child('notificacoes').child(user_id).get()
    return render_template('notificacoes.html', notificacoes=notifs_list)
```

---

### **15. Calendário**
**Arquivo:** `templates/calendario.html`  
**Rota:** `/calendario` (GET)  
**Descrição:** Calendário com heatmap de atividades e análise de sentimentos.

**Recursos:**
- 📅 Calendário do mês completo
- 🎨 Cores indicando:
  - Dias com entrada
  - Dias em sequência
  - Dias sem entrada
  - Dia de hoje
- 📊 Estatísticas do mês (entradas, dias ativos, sequência)
- 😊 Gráfico de sentimentos mais frequentes
- 🔔 Próximos lembretes e milestones
- ⬅️➡️ Navegação entre meses
- 🖱️ Click para ver detalhes do dia

**Backend:**
```python
@app.route('/calendario')
def calendario():
    diario = get_user_diario_ref(user_id).get()
    total_entradas = len(diario)
    sequencia = calcular_sequencia(diario)
    return render_template('calendario.html', 
                          total_entradas=total_entradas,
                          sequencia=sequencia,
                          diario_data=diario)
```

---

## 🔧 Sistema de Upload de Fotos

**Funcionalidades:**
- ✅ Upload de arquivo local (png, jpg, jpeg, gif, webp)
- ✅ Upload por URL
- ✅ Limite de 5MB por foto
- ✅ Validação de tipo MIME
- ✅ Armazenamento em base64 no Firebase
- ✅ Localização: `/galeria/{user_id}/{foto_id}`
- ✅ Metadados: timestamp, descrição, favorito

**Endpoint API:**
```python
@app.route('/api/upload-foto', methods=['POST'])
def upload_foto():
    # Recebe file ou url
    # Valida tamanho e tipo
    # Converte para base64
    # Salva no Firebase
    return jsonify({'success': True, 'foto_url': url})
```

---

## 🎨 Sistema de Temas

**Temas Disponíveis:**
- 🌞 **Claro (Light):** Azul (#1e88e5) e Branco
- 🌙 **Escuro (Dark):** Roxo (#8b5cf6) e Preto
- 🔄 **Automático:** Segue preferência do sistema

**Implementação:**
- CSS Variables para adaptação dinâmica
- localStorage para persistência
- Toggle button na navbar
- Aplicação automática em todas as telas

---

## 🏆 Sistema de Achievements

**6 Tipos de Badges:**

| Badge | Icone | Condição | XP |
|-------|-------|----------|-----|
| Primeira Entrada | 📝 | Criar primeira entrada | 10 |
| 7 Dias | 🔥 | 7 dias consecutivos | 50 |
| 30 Dias | 🌟 | 30 dias no mês | 100 |
| 100 Entradas | 💯 | Atingir 100 entradas | 200 |
| Explorador | 🗺️ | Usar 5 habilidades diferentes | 75 |
| Sentimentos Master | 💜 | Registrar 8 sentimentos diferentes | 100 |

**Sistema Automático:**
- Badges desbloqueados conforme critérios são atingidos
- Barras de progresso em tempo real
- Notificação ao desbloquear
- Exibição em perfil e achievements

---

## 🔗 Rotas Completas

```
GET  /                          → Dashboard
GET  /login                     → Login
POST /login                     → Validar credenciais
GET  /cadastro                  → Cadastro
POST /cadastro                  → Criar usuário
GET  /logout                    → Deslogar
GET  /diario/hoje               → Diário de hoje
GET  /diario/<dia>              → Diário de data específica
POST /diario/<dia>              → Salvar entrada
GET  /historico                 → Histórico de entradas
GET  /analise                   → Análise e gerenciamento
GET  /perfil                    → Perfil do usuário
GET  /achievements              → Achievements/badges
GET  /configuracoes             → Configurações
POST /api/config                → Salvar configurações
GET  /busca                     → Busca avançada
GET  /galeria                   → Galeria de fotos
GET  /comunidade                → Comunidade/social
GET  /notificacoes              → Notificações
GET  /calendario                → Calendário

API ENDPOINTS:
GET  /api/listas                → Emoções e habilidades
POST /api/emocoes               → Criar emoção
PUT  /api/emocoes/<key>         → Editar emoção
DELETE /api/emocoes/<key>       → Deletar emoção
POST /api/habilidades           → Criar habilidade
PUT  /api/habilidades/<key>     → Editar habilidade
DELETE /api/habilidades/<key>   → Deletar habilidade
POST /api/upload-foto           → Upload de foto
GET  /api/galeria               → Listar fotos
POST /api/diario/<dia>/toggle   → Toggle checklist
POST /deletar-diario/<dia>      → Deletar entrada
```

---

## 📊 Estrutura Firebase

```
{
  "diarios": {
    "{user_id}": {
      "01/01/2025": {
        "rotina": "...",
        "journal": "...",
        "emocoes": ["feliz", "motivado"],
        "habilidades": ["programacao", "leitura"],
        "checklist": [{"tarefa": "...", "completa": true}],
        "foto_url": "base64_encoded_image",
        "timestamp": "2025-01-01T09:00:00"
      }
    }
  },
  "listas": {
    "{user_id}": {
      "emocoes": {"feliz": "😊", ...},
      "habilidades": {"prog": {"nome": "Programação", "icone": "💻"}, ...},
      "config": {"tema": "dark", "notificacoes": true, ...}
    }
  },
  "galeria": {
    "{user_id}": {
      "{foto_id}": {
        "url": "base64_encoded",
        "descricao": "...",
        "timestamp": "2025-01-01T09:00:00",
        "favorito": false
      }
    }
  },
  "badges": {
    "{user_id}": {
      "primeira_entrada": true,
      "sete_dias": true,
      "trinta_dias": false,
      ...
    }
  },
  "posts": {
    "{post_id}": {
      "author": "{user_id}",
      "author_name": "...",
      "content": "...",
      "timestamp": "...",
      "likes": 42,
      "comments": [...]
    }
  },
  "notificacoes": {
    "{user_id}": {
      "{notif_id}": {
        "tipo": "badge|social|sistema|diario",
        "titulo": "...",
        "descricao": "...",
        "lida": false,
        "timestamp": "..."
      }
    }
  }
}
```

---

## 🎯 Funcionalidades Principais Implementadas

✅ **Autenticação:** Login/Cadastro com hash de senha  
✅ **Diário:** Escrever e gerenciar entradas  
✅ **Emoções:** CRUD completo via AJAX  
✅ **Habilidades:** CRUD completo via AJAX  
✅ **Upload de Fotos:** Arquivo ou URL, base64, 5MB max  
✅ **Galeria:** Visualização, favoritos, timeline  
✅ **Comunidade:** Feed social, posts, likes, comentários  
✅ **Achievements:** 6 tipos de badges com progresso  
✅ **Notificações:** Centro de notificações com filtros  
✅ **Calendário:** Heatmap de atividades, sentimentos  
✅ **Busca Avançada:** Filtros por texto, emoção, habilidade, data  
✅ **Configurações:** Tema, notificações, privacidade, export  
✅ **Temas:** Claro/Escuro com CSS Variables  
✅ **Responsivo:** Todas as telas adaptadas para mobile  

---

## 🚀 Como Usar

### 1. **Iniciar o Servidor**
```bash
python app.py
```

### 2. **Acessar a Aplicação**
```
http://localhost:5000
```

### 3. **Primeira Vez**
- Clique em "Cadastro"
- Registre com email e senha
- Faça login
- Comece a escrever!

### 4. **Explorar as Telas**
- Use a navbar com links principais
- Clique em "Mais" para acessar as 8 novas telas
- Veja seus badges em "Achievements"
- Configure suas preferências em "Configurações"
- Compartilhe na "Comunidade"

---

## 💡 Próximas Melhorias Sugeridas

- [ ] Sistema de notificações em tempo real (WebSocket)
- [ ] Integração com redes sociais para compartilhamento
- [ ] Integração com serviços de IA para análise de sentimentos
- [ ] Estatísticas avançadas com gráficos interativos
- [ ] Sistema de grupos/círculos de amigos
- [ ] Exportação em formato e-book
- [ ] Sincronização com calendário (Google Calendar, Outlook)
- [ ] Modo offline com sincronização posterior
- [ ] Integração com Spotify para mood music
- [ ] Sistema de metas e rastreamento

---

## 📞 Suporte

Se encontrar problemas, verifique:
1. ✅ Firebase está conectado (verifique console)
2. ✅ Arquivo de credenciais está no diretório correto
3. ✅ Python 3.7+ instalado
4. ✅ Flask e firebase-admin instalados
5. ✅ Porta 5000 está disponível

---

**Versão:** 2.0 (15 Telas Completas)  
**Data:** Janeiro 2025  
**Status:** ✅ Pronto para Produção
