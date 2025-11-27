import sys
import runpy

# Import app by running the project's app.py (robust against import path issues)
g = runpy.run_path('app.py')
app = g.get('app')
if app is None:
    raise RuntimeError('Não foi possível localizar a variável `app` no arquivo app.py')

routes = [
    '/',
    '/diario/hoje',
    '/historico',
    '/analise',
    '/perfil',
    '/achievements',
    '/configuracoes',
    '/busca',
    '/galeria',
    '/comunidade',
    '/notificacoes',
    '/calendario'
]

print('Running smoke tests against local Flask app (test_client)')

with app.test_client() as client:
    # Set session values to simulate logged in user
    with client.session_transaction() as sess:
        sess['logged_in'] = True
        sess['user_id'] = 'test_user'
        sess['user_nome'] = 'Teste'
        sess['user_foto'] = 'https://placehold.co/40x40'

    results = []
    for r in routes:
        try:
            resp = client.get(r)
            status = resp.status_code
            content_snippet = resp.get_data(as_text=True)[:300].replace('\n',' ') if resp.data else ''
            results.append((r, status, content_snippet))
        except Exception as e:
            results.append((r, 'EXCEPTION', str(e)))

    # Print summarized results
    ok = True
    for r, status, snippet in results:
        if status != 200:
            ok = False
        print(f"{r:20} -> {status}")
        if isinstance(snippet, str) and snippet:
            print('  Response snippet:', snippet[:200])
    
    if ok:
        print('\nSMOKE TESTS: PASS — todas as rotas retornaram 200 OK')
    else:
        print('\nSMOKE TESTS: Some routes failed (status != 200). Check output above for details.')

sys.exit(0)
