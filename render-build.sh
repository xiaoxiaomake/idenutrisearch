#!/usr/bin/env bash
# Interrompe em caso de erro
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Baixando o Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
  cd $HOME/project/src # Retornar ao diretório original
else
  echo "...Usando o Chrome do cache"
fi

# Adicionar o caminho do Chrome ao PATH durante a execução
# export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome"
