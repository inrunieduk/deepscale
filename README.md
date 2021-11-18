# Sobre o projeto
Esse repositório contém código necessário para rodar uma API que utiliza inteligência artificial para redimensionar imagens.

O funcionamento da rede neural é descrito [nesse artigo](https://arxiv.org/pdf/1609.04802.pdf).

O modelo foi treinado com 600.000 imagens do dataset [OpenImages V4](https://storage.googleapis.com/openimages/web/index.html).

# Como funciona      
 O usuário deve enviar uma imagem, esta imagem será tratada por uma rede neural, que irá aumentar a densidade de pixels da mesma e melhorar sua qualidade.

# Tecnologias utilizadas 
- Python

# Pré-requisitos
- Docker([instruções de instalação](https://docs.docker.com/install/))
- Visual Studio Code([instruções de instalação](https://code.visualstudio.com/download))

# Como executar o projeto
## 1. Clone o repositório
```
git clone https://github.com/inrunieduk/deepscale.git
```

## 2. Vá até o diretório raiz
```
cd deepscale
```

## 3. Execute o script build_and_run.sh
```
./build_and_run.sh
```

Após o fim da execução do script, a API estará disponível.

## 4. Abra a pasta raiz com VS Code
```
. code
```

## 5. Executar a pasta /web com LiveServer
Acessar http://127.0.0.1:5500/web/index.html para interagir com a aplicação.

# Próximos objetivos

- [x] Adicionar webservice
- [x] Adicionar webapp
- [x] Recorte de imagem no webapp

# Autores
[Igor Rossetti](https://github.com/inrunieduk) <br>
[Bruno Canisella](https://github.com/BrunoCanisella)
