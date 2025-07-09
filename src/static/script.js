// Função para mostrar/esconder tabs
function MainShowTab(event, tabId) {
    // Remove "active" de todos conteúdos e abas
    document.querySelectorAll('.main-tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.main-tab').forEach(el => el.classList.remove('active'));
    // Ativa aba e conteúdo clicado
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}


// Função para mostrar/esconder tabs
function showTab(event, tabId) {
    // Remove "active" de todos conteúdos e abas
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    // Ativa aba e conteúdo clicado
    document.getElementById(tabId).classList.add('active');
    event.currentTarget.classList.add('active');
}

// Função para atualizar alerts
async function atualizarAlerts() {
    const btn = document.getElementById('refresh-alerts-btn');
    const alertsList = document.getElementById('alerts-list');
    
    // Mostra loading no botão
    btn.classList.add('loading');
    btn.textContent = 'Carregando...';
    btn.disabled = true;
    
    try {
        // Faz requisição para buscar novos alerts
        const response = await fetch('/alerts');
        const data = await response.json();
        
        if (data.success) {
            // Limpa a lista atual
            alertsList.innerHTML = '';
            
            // Adiciona os novos alerts
            if (data.alerts && data.alerts.length > 0) {
                data.alerts.forEach(alert => {
                    const alertItem = document.createElement('li');
                    alertItem.className = 'alert-item';
                    alertItem.innerHTML = `
                        <strong>${alert.alert}</strong>
                        <div class="alert-customer-id">${alert.customer_id}</div>
                        <div class="alert-customer-name">${alert.customer_name}</div>
                        <div class="alert-date">${alert.date}</div>
                    `;
                    alertsList.appendChild(alertItem);
                });
            } else {
                // Se não há alerts
                const emptyItem = document.createElement('li');
                emptyItem.className = 'alert-item empty';
                emptyItem.textContent = 'Nenhum alerta encontrado.';
                alertsList.appendChild(emptyItem);
            }
            
            console.log('✅ Alerts atualizados com sucesso!');
        } else {
            console.error('❌ Erro ao buscar alerts:', data.error);
            alert('Erro ao atualizar alerts: ' + data.error);
        }
    } catch (error) {
        console.error('❌ Erro na requisição:', error);
        alert('Erro ao conectar com o servidor');
    } finally {
        // Remove loading do botão
        btn.classList.remove('loading');
        btn.textContent = 'Atualizar';
        btn.disabled = false;
    }
}

// Função para toggle do input de depósito
function toggleDepositInput() {
    const checkbox = document.getElementById("valor-aleatorio-deposito");
    const input = document.getElementById("deposit-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
        } else {
            input.disabled = false;
        }
    }
}

// Função para toggle do input de saque
function toggleSaqueInput() {
    const checkbox = document.getElementById("valor-aleatorio-saque");
    const input = document.getElementById("saque-input");
    
    if (checkbox && input) {
        if (checkbox.checked) {
            input.value = "";
            input.disabled = true;
        } else {
            input.disabled = false;
        }
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Configurar eventos para depósito
    const checkboxDeposito = document.getElementById("valor-aleatorio-deposito");
    if (checkboxDeposito) {
        toggleDepositInput(); // Estado inicial
        checkboxDeposito.addEventListener("change", toggleDepositInput);
    }
    
    // Configurar eventos para saque
    const checkboxSaque = document.getElementById("valor-aleatorio-saque");
    if (checkboxSaque) {
        toggleSaqueInput(); // Estado inicial
        checkboxSaque.addEventListener("change", toggleSaqueInput);
    }
});

// Opcional: Atualizar alerts automaticamente a cada 30 segundos
// setInterval(atualizarAlerts, 30000);