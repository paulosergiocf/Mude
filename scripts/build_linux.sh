#!/bin/bash

echo '=== Build AppImage para Mude ==='

check_root_files() {
    if [ ! -f 'App.py' ]; then
        echo 'ERRO: Execute do diretório raiz do projeto'
        exit 1
    fi
}

check_venv() {
    if [ ! -d "$ENV" ]; then
        echo 'ERRO: Ambiente virtual '"$ENV"' não encontrado'
        exit 1
    fi
}

set_config() {
    APP='Mude'
    ARCH='x86_64'
    ENV='.venv'
    BUILD='./build'
    DIST='./dist'
    APPDIR="$BUILD/AppDir"
    OUTPUT="$DIST/$APP-$ARCH.AppImage"
}

prepare_dirs() {
    echo '1. Preparando diretórios...'
    rm -rf "$BUILD" "$DIST"
    mkdir -p "$APPDIR" "$DIST"
}

copy_project_files() {
    echo '2. Copiando arquivos...'
    cp App.py "$APPDIR/"
    cp requirements.txt "$APPDIR/"
    cp -r css img src "$APPDIR/"
    echo '3. Copiando ambiente virtual...'
    cp -r "$ENV" "$APPDIR/"
}

# ==================== CRIAÇÃO DE ARQUIVOS ====================

create_apprun() {
    echo '4. Criando AppRun...'
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
cd "$HERE"

# Ativar ambiente virtual
export PATH="$HERE/.venv/bin:$PATH"

# Executar app passando o diretório de dados como variável
exec "$HERE/.venv/bin/python3" App.py "$@"
EOF
    chmod +x "$APPDIR/AppRun"
}

create_desktop_file() {
    echo '5. Criando arquivo .desktop...'
    printf "[Desktop Entry]\nName=Mude\nComment=Gestão de hábitos e metas\nExec=/home/$USER/.mude/Mude-x86_64.AppImage\nIcon=mude\nType=Application\nCategories=Utility;\nStartupNotify=true\nTerminal=false\nStartupWMClass=mude\n" > "$APPDIR/$APP.desktop"
    cp "$APPDIR/$APP.desktop" $DIST



}

copy_icon() {
    if [ -f 'img/mude.png' ]; then
        cp 'img/mude.png' "$APPDIR/mude.png"
    fi
}

get_appimagetool() {
    echo '6. Verificando appimagetool...'
    local venv_tool="./$ENV/appimagetool"
    if [ -x "$venv_tool" ]; then
        echo 'Usando appimagetool do ambiente virtual...'
        TOOL="$venv_tool"
    elif which appimagetool >/dev/null 2>&1; then
        echo 'Usando appimagetool do sistema...'
        TOOL='appimagetool'
    else
        echo 'Baixando appimagetool para '"$ENV"'...'
        wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-$ARCH.AppImage" -O "$venv_tool"
        chmod +x "$venv_tool"
        TOOL="$venv_tool"
    fi
}

build_appimage() {
    echo '7. Criando AppImage...'
    local abs_output="$(realpath "$OUTPUT")"
    local abs_appdir="$(realpath "$APPDIR")"
    ARCH="$ARCH" $TOOL "$abs_appdir" "$abs_output"
}

cleanup_build() {
    echo '8. Limpando diretório de build...'
    rm -rf "$BUILD"
}

show_result() {
    if [ -f "$OUTPUT" ]; then
        chmod +x "$OUTPUT"
        echo ''
        echo '=== SUCESSO ==='
        echo "AppImage criado: $OUTPUT"
        echo "Tamanho: $(du -h "$OUTPUT" | cut -f1)"
        
    else
        echo 'ERRO: Falha ao criar AppImage'
        exit 1
    fi
}

copy_app_for_system() {

    cp "$DIST/$APP.desktop" ~/.local/share/applications/
    sudo cp img/logo.png /usr/share/icons/hicolor/48x48/apps/mude.png
    sudo update-icon-caches /usr/share/icons/hicolor/

    cp "/home/$USER/$APP.desktop" ~/.local/share/applications/
    cp "$DIST/$APP-x86_64.AppImage" ~/.mude/


}


main() {
    set_config
    check_root_files
    check_venv
    prepare_dirs
    copy_project_files
    create_apprun
    create_desktop_file
    copy_icon
    get_appimagetool
    build_appimage
    cleanup_build
    show_result
    copy_app_for_system
}

echo "🔐 Autenticação necessária para instalação..."
sudo -v  

while true; do
    sudo -n true 
    sleep 60
    kill -0 "$$" 2>/dev/null || exit 
done &
SUDO_KEEPALIVE_PID=$!

main