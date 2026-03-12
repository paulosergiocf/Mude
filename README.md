# Mude

Aplicação para apoiar na formação de hábitos, gerencia as metas por
um tempo longo suficiente para fazer coisas significativas e curto suficiente para ter senso de urgência. 

Implementação de metodo discutido no video: [Como Mudar Sua Vida Em 6 Meses](https://www.youtube.com/watch?v=togozCEmK6A)


## Como usar

### Usuários Linux

Download da aplicação [Mude-x86_64.AppImage](https://github.com/paulosergiocf/Mude/releases)

```sh
    # Atribui permissão
    chmod +x Mude-x86_64.AppImage
    # Executar
    ./Mude-x86_64.AppImage

```

A base de dados da aplicação estará localizada no diretorio ```/home/$USER/.mude/data/```.

Para customizar o tema criar ```/home/$USER/.mude/theme/style.css``` (Obs. configurar de acordo com [tema padrão](https://github.com/paulosergiocf/Mude/blob/main/css/style.css)).

### Usuários Windows.

> Em progresso, aguarde atualizações.

## Screenshot
![Logo](https://raw.githubusercontent.com/paulosergiocf/Mude/refs/heads/3-correcao-de-paths/img/screeshot.png)

## Objetivo

Esta aplicação gerencia metas específicas semanais, dividindo-as automaticamente em ciclos de 12 semanas. Cada semana representa um ciclo de produtividade, ao final do qual você avalia seu desempenho em relação às metas estabelecidas.

### Sistema de Avaliação

Ao final de cada ciclo você avalia quantas ações planejou e quantas realizou:

|Porcentagem| Descrição|
|:-:|:-:|
|Entre **90%** e **100%**|Indica que suas metas podem estar subdimensionadas. Considere aumentar o nível de desafio.|
|Entre **80%** e **90%**|É o ponto ideal. Demonstra um equilíbrio saudável entre ambição e realização, mantendo a motivação e o progresso constante.|
|Abaixo de **80%** |Sugere que as metas podem não ter sido realistas. Reavalie e ajuste para um patamar mais atingível.|


**Recomendação:** Use essa métrica semanalmente para calibrar suas expectativas e otimizar seu planejamento, garantindo um crescimento sustentável.



## Licença

Este projeto está licenciado sob a **GNU General Public License v3.0** (GPL-3.0). Veja o arquivo [LICENSE](LICENSE) para o texto completo da licença.
