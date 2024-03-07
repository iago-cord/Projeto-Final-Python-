from plyer import notification

# Criando a notificação de importacao das bases
def alerta(base, data, url):
    if base.status_code == 200:
        notification.notify(
            title = f'Atenção',
            message = f'Extração de dados realizada com sucesso em {data} da base {url}',
            timeout = 5
        )
    else:
        notification.notify(
            title = f'Atenção',
            message = f'Extração de dados não realizada, código do erro: {base.status_code} ',
            timeout = 5
        )