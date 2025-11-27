// ===== FUNÇÕES DO DIÁRIO =====// JS simples para adicionar/remover itens de checklist dinamicamente

document.addEventListener('DOMContentLoaded', function(){

// Adicionar tarefa ao checklistconst addCheckBtn = document.getElementById('add-check')

function adicionarTarefa() {const list = document.getElementById('checklist-list')

    const container = document.getElementById('checklist-container');if(addCheckBtn){

    if (!container) return;addCheckBtn.addEventListener('click', ()=>{

    const idx = list.querySelectorAll('.check-item').length

    const item = document.createElement('div');const div = document.createElement('div')

    item.className = 'checklist-item';div.className = 'check-item'

    item.innerHTML = `div.innerHTML = `<input type="checkbox" name="check_${idx}"><input type="text" name="check_item"><button type="button" class="remove-check">Remover</button>`

        <input type="text" name="tarefa_texto" placeholder="Descreva uma tarefa...">list.appendChild(div)

        <button type="button" class="btn-remove-tarefa" onclick="this.parentElement.remove();">})

            <i class="fas fa-trash"></i>}

        </button>document.addEventListener('click', function(e){

    `;if(e.target && e.target.classList.contains('remove-check')){

    container.appendChild(item);e.target.closest('.check-item').remove()

}}

})

// Validar formulário antes de enviar})
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.diario-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('Formulário do diário enviado');
        });
    }

    // Auto-dismiss das notificações após 5 segundos
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.display = 'none';
        }, 5000);
    });

    // Carregar foto preview em tempo real
    const photoInput = document.getElementById('photo_url');
    if (photoInput) {
        photoInput.addEventListener('change', function() {
            // Lógica para preview da foto (opcional)
        });
    }
});

// Fechar notificações quando clicar no X
document.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('flash-close')) {
        e.target.parentElement.style.display = 'none';
    }
});

// Toggle do checklist
function toggleChecklist(dia, index) {
    fetch(`/diario/${dia}/checklist/toggle/${index}`, {method: 'GET'})
    .then(r => { if(r.ok) location.reload(); })
    .catch(console.error);
}

// ---------- Gerenciamento de Emoções e Habilidades via AJAX ----------
async function apiFetch(url, method='GET', data=null){
    const opts = {method, headers: {'Content-Type':'application/json'}};
    if(data) opts.body = JSON.stringify(data);
    const res = await fetch(url, opts);
    if(!res.ok) throw new Error('Erro na requisição');
    return res.json();
}

// Emoções
async function adicionarEmocao(){
    const emoji = prompt('Insira o emoji (por exemplo: 😊):');
    if(!emoji) return;
    try{
        const res = await apiFetch('/api/emocoes','POST',{emoji});
        alert('Emoção adicionada. Atualize a página para ver.');
        location.reload();
    }catch(e){alert('Erro ao adicionar emoção');}
}

async function editarEmocao(key, current){
    const novo = prompt('Atualize o emoji:', current);
    if(novo===null) return;
    try{ await apiFetch(`/api/emocoes/${encodeURIComponent(key)}`,'PUT',{emoji:novo}); location.reload(); }
    catch(e){ alert('Erro ao atualizar emoção'); }
}

async function deletarEmocao(key){
    if(!confirm('Deseja realmente excluir esta emoção?')) return;
    try{ await apiFetch(`/api/emocoes/${encodeURIComponent(key)}`,'DELETE'); location.reload(); }
    catch(e){ alert('Erro ao deletar'); }
}

// Habilidades
async function adicionarHabilidade(){
    const nome = prompt('Nome da habilidade (ex: Programação):');
    if(!nome) return;
    const icone = prompt('Ícone (texto ou emoji) opcional:', '💡') || '';
    try{ await apiFetch('/api/habilidades','POST',{nome, icone}); location.reload(); }
    catch(e){ alert('Erro ao adicionar habilidade'); }
}

async function editarHabilidade(key, currentNome, currentIcon){
    const nome = prompt('Nome da habilidade:', currentNome);
    if(nome===null) return;
    const icone = prompt('Ícone (emoji/texto):', currentIcon||'') || '';
    try{ await apiFetch(`/api/habilidades/${encodeURIComponent(key)}`,'PUT',{nome, icone}); location.reload(); }
    catch(e){ alert('Erro ao atualizar habilidade'); }
}

async function deletarHabilidade(key){
    if(!confirm('Deseja realmente excluir esta habilidade?')) return;
    try{ await apiFetch(`/api/habilidades/${encodeURIComponent(key)}`,'DELETE'); location.reload(); }
    catch(e){ alert('Erro ao deletar'); }
}
