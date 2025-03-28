# Playdown

Bem-vindo ao Playdown, um aplicativo moderno para baixar vídeos e playlists do YouTube. Com uma interface gráfica elegante e recursos avançados, o Playdown permite que você baixe conteúdo do YouTube facilmente para consumo offline.

![Playdown Screenshot](screenshot.png)

## Recursos Principais

- **Interface moderna e intuitiva** com tema escuro
- **Suporte para vídeos e playlists** do YouTube
- **Opções de formato** - escolha entre MP3 (áudio) ou MP4 (vídeo)
- **Download de playlist com seleção** - escolha quais vídeos baixar
- **Barra de progresso** para acompanhar o status do download
- **Multithreading** - interface responsiva durante o download
- **Escolha do diretório** para salvar os arquivos

## Como usar

1. Inicie o aplicativo
2. Cole a URL do vídeo ou playlist do YouTube
3. Clique em "Fetch Info" para obter as informações
4. Escolha o formato desejado (MP3 ou MP4)
5. Selecione o diretório onde deseja salvar
6. Para playlists, selecione quais vídeos você deseja baixar
7. Clique em "Download" e aguarde a conclusão

## Requisitos

Para usar o Playdown com todas as funcionalidades, você precisa:

- Python 3.6 ou superior
- As bibliotecas listadas em `requirements.txt`
- FFmpeg instalado no seu sistema (necessário para conversão para MP3)

**Nota sobre FFmpeg**: Se o FFmpeg não estiver instalado, o Playdown ainda funcionará, mas com as seguintes limitações:
- A opção de conversão para MP3 estará desativada
- Os downloads serão apenas em formato MP4
- A qualidade pode ser ligeiramente menor devido à impossibilidade de mesclar streams de áudio e vídeo

Para baixar o FFmpeg, visite [ffmpeg.org/download](https://ffmpeg.org/download.html) ou use um gerenciador de pacotes como Chocolatey (Windows), Homebrew (macOS) ou apt (Linux).

## Instalação

```bash
# Clone o repositório
git clone https://github.com/tago-dev/playdown.git
cd playdown

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
python playdown.py
```

## Download

Baixe a versão mais recente do Playdown [clicando aqui](https://github.com/tago-dev/playdown/releases/latest).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar o Playdown.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.